/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.ambari.view.hive.resources.jobs;

import com.google.inject.Inject;
import org.apache.ambari.view.ViewResourceHandler;
import org.apache.ambari.view.hive.BaseService;
import org.apache.ambari.view.hive.backgroundjobs.BackgroundJobController;
import org.apache.ambari.view.hive.client.Cursor;
import org.apache.ambari.view.hive.persistence.utils.ItemNotFound;
import org.apache.ambari.view.hive.resources.jobs.atsJobs.ATSRequestsDelegate;
import org.apache.ambari.view.hive.resources.jobs.atsJobs.ATSRequestsDelegateImpl;
import org.apache.ambari.view.hive.resources.jobs.atsJobs.ATSParser;
import org.apache.ambari.view.hive.resources.jobs.atsJobs.IATSParser;
import org.apache.ambari.view.hive.resources.jobs.viewJobs.*;
import org.apache.ambari.view.hive.utils.*;
import org.apache.ambari.view.hive.utils.HdfsApi;
import org.apache.commons.beanutils.PropertyUtils;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.json.simple.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.servlet.http.HttpServletResponse;
import javax.ws.rs.*;
import javax.ws.rs.core.*;
import java.io.*;
import java.lang.reflect.InvocationTargetException;
import java.util.*;
import java.util.concurrent.Callable;

/**
 * Servlet for queries
 * API:
 * GET /:id
 *      read job
 * POST /
 *      create new job
 *      Required: title, queryFile
 * GET /
 *      get all Jobs of current user
 */
public class JobService extends BaseService {
  @Inject
  ViewResourceHandler handler;

  protected JobResourceManager resourceManager;
  private IOperationHandleResourceManager opHandleResourceManager;
  protected final static Logger LOG =
      LoggerFactory.getLogger(JobService.class);

  protected synchronized JobResourceManager getResourceManager() {
    if (resourceManager == null) {
      SharedObjectsFactory connectionsFactory = getSharedObjectsFactory();
      resourceManager = new JobResourceManager(connectionsFactory, context);
    }
    return resourceManager;
  }

  private IOperationHandleResourceManager getOperationHandleResourceManager() {
    if (opHandleResourceManager == null) {
      opHandleResourceManager = new OperationHandleResourceManager(getSharedObjectsFactory());
    }
    return opHandleResourceManager;
  }

  /**
   * Get single item
   */
  @GET
  @Path("{jobId}")
  @Produces(MediaType.APPLICATION_JSON)
  public Response getOne(@PathParam("jobId") String jobId) {
    try {
      JobController jobController = getResourceManager().readController(jobId);

      JSONObject jsonJob = jsonObjectFromJob(jobController);

      return Response.ok(jsonJob).build();
    } catch (WebApplicationException ex) {
      throw ex;
    } catch (ItemNotFound itemNotFound) {
      throw new NotFoundFormattedException(itemNotFound.getMessage(), itemNotFound);
    } catch (Exception ex) {
      throw new ServiceFormattedException(ex.getMessage(), ex);
    }
  }

  private JSONObject jsonObjectFromJob(JobController jobController) throws IllegalAccessException, NoSuchMethodException, InvocationTargetException {
    Map createdJobMap = PropertyUtils.describe(jobController.getJob());
    createdJobMap.remove("class"); // no need to show Bean class on client

    JSONObject jobJson = new JSONObject();
    jobJson.put("job", createdJobMap);
    return jobJson;
  }

  /**
   * Get job results in csv format
   */
  @GET
  @Path("{jobId}/results/csv")
  @Produces("text/csv")
  public Response getResultsCSV(@PathParam("jobId") String jobId,
                                @Context HttpServletResponse response,
                                @QueryParam("columns") final String requestedColumns) {
    try {
      JobController jobController = getResourceManager().readController(jobId);
      final Cursor resultSet = jobController.getResults();
      resultSet.selectColumns(requestedColumns);

      StreamingOutput stream = new StreamingOutput() {
        @Override
        public void write(OutputStream os) throws IOException, WebApplicationException {
          Writer writer = new BufferedWriter(new OutputStreamWriter(os));
          CSVPrinter csvPrinter = new CSVPrinter(writer, CSVFormat.DEFAULT);
          try {
            while (resultSet.hasNext()) {
              csvPrinter.printRecord(resultSet.next().getRow());
              writer.flush();
            }
          } finally {
            writer.close();
          }
        }
      };

      return Response.ok(stream).build();
    } catch (WebApplicationException ex) {
      throw ex;
    } catch (ItemNotFound itemNotFound) {
      throw new NotFoundFormattedException(itemNotFound.getMessage(), itemNotFound);
    } catch (Exception ex) {
      throw new ServiceFormattedException(ex.getMessage(), ex);
    }
  }

  /**
   * Get job results in csv format
   */
  @GET
  @Path("{jobId}/results/csv/saveToHDFS")
  @Produces(MediaType.APPLICATION_JSON)
  public Response getResultsToHDFS(@PathParam("jobId") String jobId,
                                   @QueryParam("commence") String commence,
                                   @QueryParam("file") final String targetFile,
                                   @QueryParam("stop") final String stop,
                                   @QueryParam("columns") final String requestedColumns,
                                   @Context HttpServletResponse response) {
    try {
      final JobController jobController = getResourceManager().readController(jobId);

      String backgroundJobId = "csv" + String.valueOf(jobController.getJob().getId());
      if (commence != null && commence.equals("true")) {
        if (targetFile == null)
          throw new MisconfigurationFormattedException("targetFile should not be empty");
        BackgroundJobController.getInstance(context).startJob(String.valueOf(backgroundJobId), new Runnable() {
          @Override
          public void run() {

            try {
              Cursor resultSet = jobController.getResults();
              resultSet.selectColumns(requestedColumns);

              FSDataOutputStream stream = getSharedObjectsFactory().getHdfsApi().create(targetFile, true);
              Writer writer = new BufferedWriter(new OutputStreamWriter(stream));
              CSVPrinter csvPrinter = new CSVPrinter(writer, CSVFormat.DEFAULT);
              try {
                while (resultSet.hasNext() && !Thread.currentThread().isInterrupted()) {
                  csvPrinter.printRecord(resultSet.next().getRow());
                  writer.flush();
                }
              } finally {
                writer.close();
              }
              stream.close();

            } catch (IOException e) {
              throw new ServiceFormattedException("Could not write CSV to HDFS for job#" + jobController.getJob().getId(), e);
            } catch (InterruptedException e) {
              throw new ServiceFormattedException("Could not write CSV to HDFS for job#" + jobController.getJob().getId(), e);
            } catch (ItemNotFound itemNotFound) {
              throw new NotFoundFormattedException("Job results are expired", itemNotFound);
            }

          }
        });
      }

      if (stop != null && stop.equals("true")) {
        BackgroundJobController.getInstance(context).interrupt(backgroundJobId);
      }

      JSONObject object = new JSONObject();
      object.put("stopped", BackgroundJobController.getInstance(context).isInterrupted(backgroundJobId));
      object.put("jobId", jobController.getJob().getId());
      object.put("backgroundJobId", backgroundJobId);
      object.put("operationType", "CSV2HDFS");
      object.put("status", BackgroundJobController.getInstance(context).state(backgroundJobId).toString());

      return Response.ok(object).build();
    } catch (WebApplicationException ex) {
      throw ex;
    } catch (ItemNotFound itemNotFound) {
      throw new NotFoundFormattedException(itemNotFound.getMessage(), itemNotFound);
    } catch (Exception ex) {
      throw new ServiceFormattedException(ex.getMessage(), ex);
    }
  }

  /**
   * Get next results page
   */
  @GET
  @Path("{jobId}/results")
  @Produces(MediaType.APPLICATION_JSON)
  public Response getResults(@PathParam("jobId") String jobId,
                             @QueryParam("first") String fromBeginning,
                             @QueryParam("count") Integer count,
                             @QueryParam("searchId") String searchId,
                             @QueryParam("columns") final String requestedColumns) {
    try {
      final JobController jobController = getResourceManager().readController(jobId);

      return ResultsPaginationController.getInstance(context)
           .request(jobId, searchId, true, fromBeginning, count,
               new Callable<Cursor>() {
                 @Override
                 public Cursor call() throws Exception {
                   Cursor cursor = jobController.getResults();
                   cursor.selectColumns(requestedColumns);
                   return cursor;
                 }
               }).build();
    } catch (WebApplicationException ex) {
      throw ex;
    } catch (ItemNotFound itemNotFound) {
      throw new NotFoundFormattedException(itemNotFound.getMessage(), itemNotFound);
    } catch (Exception ex) {
      throw new ServiceFormattedException(ex.getMessage(), ex);
    }
  }

  /**
   * Renew expiration time for results
   */
  @GET
  @Path("{jobId}/results/keepAlive")
  public Response keepAliveResults(@PathParam("jobId") String jobId,
                             @QueryParam("first") String fromBeginning,
                             @QueryParam("count") Integer count) {
    try {
      if (!ResultsPaginationController.getInstance(context).keepAlive(jobId, ResultsPaginationController.DEFAULT_SEARCH_ID)) {
        throw new NotFoundFormattedException("Results already expired", null);
      }
      return Response.ok().build();
    } catch (WebApplicationException ex) {
      throw ex;
    } catch (Exception ex) {
      throw new ServiceFormattedException(ex.getMessage(), ex);
    }
  }

  /**
   * Delete single item
   */
  @DELETE
  @Path("{id}")
  public Response delete(@PathParam("id") String id,
                         @QueryParam("remove") final String remove) {
    try {
      JobController jobController;
      try {
        jobController = getResourceManager().readController(id);
      } catch (ItemNotFound itemNotFound) {
        throw new NotFoundFormattedException(itemNotFound.getMessage(), itemNotFound);
      }
      jobController.cancel();
      if (remove != null && remove.compareTo("true") == 0) {
        getResourceManager().delete(id);
      }
//      getResourceManager().delete(Integer.valueOf(queryId));
      return Response.status(204).build();
    } catch (WebApplicationException ex) {
      throw ex;
    } catch (ItemNotFound itemNotFound) {
      throw new NotFoundFormattedException(itemNotFound.getMessage(), itemNotFound);
    } catch (Exception ex) {
      throw new ServiceFormattedException(ex.getMessage(), ex);
    }
  }

  /**
   * Get all Jobs
   */
  @GET
  @Produces(MediaType.APPLICATION_JSON)
  public Response getList() {
    try {
      LOG.debug("Getting all job");
      ATSRequestsDelegate transport = new ATSRequestsDelegateImpl(context, "http://127.0.0.1:8188");
      IATSParser atsParser = new ATSParser(transport);
      Aggregator aggregator = new Aggregator(getResourceManager(), getOperationHandleResourceManager(), atsParser);
      List allJobs = aggregator.readAll(context.getUsername());

      JSONObject object = new JSONObject();
      object.put("jobs", allJobs);
      return Response.ok(object).build();
    } catch (WebApplicationException ex) {
      throw ex;
    } catch (Exception ex) {
      throw new ServiceFormattedException(ex.getMessage(), ex);
    }
  }

  /**
   * Create job
   */
  @POST
  @Consumes(MediaType.APPLICATION_JSON)
  public Response create(JobRequest request, @Context HttpServletResponse response,
                         @Context UriInfo ui) {
    try {
      Map jobInfo = PropertyUtils.describe(request.job);
      Job job = new JobImpl(jobInfo);
      getResourceManager().create(job);

      JobController createdJobController = getResourceManager().readController(job.getId());
      createdJobController.submit();

      response.setHeader("Location",
          String.format("%s/%s", ui.getAbsolutePath().toString(), job.getId()));

      JSONObject jobObject = jsonObjectFromJob(createdJobController);

      return Response.ok(jobObject).status(201).build();
    } catch (WebApplicationException ex) {
      throw ex;
    } catch (ItemNotFound itemNotFound) {
      throw new NotFoundFormattedException(itemNotFound.getMessage(), itemNotFound);
    } catch (Exception ex) {
      throw new ServiceFormattedException(ex.getMessage(), ex);
    }
  }

  /**
   * Wrapper object for json mapping
   */
  public static class JobRequest {
    public JobImpl job;
  }
}
