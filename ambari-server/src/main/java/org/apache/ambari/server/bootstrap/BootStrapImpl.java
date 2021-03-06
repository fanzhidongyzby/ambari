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

package org.apache.ambari.server.bootstrap;

import java.io.File;
import java.io.IOException;
import java.net.InetAddress;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.apache.ambari.server.api.services.AmbariMetaInfo;
import org.apache.ambari.server.bootstrap.BSResponse.BSRunStat;
import org.apache.ambari.server.configuration.Configuration;
import org.apache.ambari.server.controller.license.LicenseManager;
import org.apache.ambari.server.state.Host;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.google.inject.Inject;
import com.google.inject.Singleton;
import org.apache.ambari.server.controller.AmbariServer;

@Singleton
public class BootStrapImpl {
  public static final String DEV_VERSION = "${ambariVersion}";
  private File bootStrapDir;
  private String bootScript;
  private String bootSetupAgentScript;
  private String bootSetupAgentPassword;
  private BSRunner bsRunner;
  private String masterHostname;
  private String agentDefaultLoginUser;
  private String agentDefaultLoginPassword;
  long timeout;

  private static Log LOG = LogFactory.getLog(BootStrapImpl.class);

  /* Monotonically increasing requestid for the bootstrap api to query on */
  int requestId = 0;
  private FifoLinkedHashMap<Long, BootStrapStatus> bsStatus;
  private final String clusterOsType;
  private final String clusterOsFamily;
  private String projectVersion;
  private int serverPort;
  private String bootstrapSSHUser;

  @Inject
  public BootStrapImpl(Configuration conf, AmbariMetaInfo ambariMetaInfo) throws IOException {
    this.bootStrapDir = conf.getBootStrapDir();
    this.bootScript = conf.getBootStrapScript();
    this.bootSetupAgentScript = conf.getBootSetupAgentScript();
    this.bootSetupAgentPassword = conf.getBootSetupAgentPassword();
    this.bsStatus = new FifoLinkedHashMap<Long, BootStrapStatus>();
    this.masterHostname = conf.getMasterHostname(
        InetAddress.getLocalHost().getCanonicalHostName());
    this.clusterOsType = conf.getServerOsType();
    this.clusterOsFamily = conf.getServerOsFamily();
    this.projectVersion = ambariMetaInfo.getServerVersion();
    this.projectVersion = (this.projectVersion.equals(DEV_VERSION)) ? DEV_VERSION.replace("$", "") : this.projectVersion;
    this.serverPort = (conf.getApiSSLAuthentication())? conf.getClientSSLApiPort() : conf.getClientApiPort();
    this.agentDefaultLoginUser = conf.getAgentDefaultLoginUser();
    this.agentDefaultLoginPassword = conf.getAgentDefaultLoginPassword();
    this.bootstrapSSHUser = conf.getBootstrapSSHUser();
  }

  /**
   * Return {@link BootStrapStatus} for a given responseId.
   * @param requestId the responseId for which the status needs to be returned.
   * @return status for a specific response id. A response Id of -1 means the
   * latest responseId.
   */
  public synchronized BootStrapStatus getStatus(long requestId) {
    if (! bsStatus.containsKey(Long.valueOf(requestId))) {
      return null;
    }
    return bsStatus.get(Long.valueOf(requestId));
  }

  /**
   * update status of a request. Mostly called by the status collector thread.
   * @param requestId the request id.
   * @param status the status of the update.
   */
  synchronized void updateStatus(long requestId, BootStrapStatus status) {
    bsStatus.put(Long.valueOf(requestId), status);
  }


  public synchronized void init() throws IOException {
    if (!bootStrapDir.exists()) {
      boolean mkdirs = bootStrapDir.mkdirs();
      if (!mkdirs) throw new IOException("Unable to make directory for " +
          "bootstrap " + bootStrapDir);
    }
  }

  public  synchronized BSResponse runBootStrap(SshHostInfo info) {
    BSResponse response = new BSResponse();
    /* Run some checks for ssh host */
    LOG.info("BootStrapping hosts " + info.hostListAsString());
    if (bsRunner != null) {
      response.setLog("BootStrap in Progress: Cannot Run more than one.");
      response.setStatus(BSRunStat.ERROR);

      return response;
    }
    requestId++;

      //Added by junz for validating license key
      List<Host> hosts = AmbariServer.getController().getClusters().getHosts();
      LicenseManager licenseManager = AmbariServer.getController().getLicenseManager();
      String errMsg = null;

      int clusterLimit = licenseManager.getClusterLimit();
      if(hosts != null && info.getHosts().size() > clusterLimit) {
          if (clusterLimit == 1) {
              errMsg = "No license key is detected, only 1 server is supported!";
          } else {
              errMsg = "License allows " + clusterLimit + " hosts at maximum!";
          }
      }

      Date expirationDate = licenseManager.getExpirationDate();
      Date currentDate = new Date();
      if(expirationDate != null && currentDate.after(expirationDate)) {
          errMsg = "License expires with expiration date " + expirationDate;
      }

      if(errMsg != null){
          BootStrapStatus status = new BootStrapStatus();
          status.setLog(errMsg);
          List<BSHostStatus> bsHostStatuses = new ArrayList<BSHostStatus>();
          for(String hostName : info.getHosts()){
              BSHostStatus bsHostStatus = new BSHostStatus();
              bsHostStatus.setHostName(hostName);
              bsHostStatus.setStatus("FAILED");
              bsHostStatus.setStatusCode("1");
              bsHostStatus.setLog(errMsg);
              bsHostStatuses.add(bsHostStatus);
          }
          status.setHostsStatus(bsHostStatuses);
          status.setStatus(BootStrapStatus.BSStat.ERROR);
          updateStatus(requestId, status);

          response.setStatus(BSRunStat.OK);
          response.setRequestId(requestId);
          return response;
      }

    if (info.getHosts() == null || info.getHosts().isEmpty()) {
      BootStrapStatus status = new BootStrapStatus();
      status.setLog("Host list is empty.");
      status.setHostsStatus(new ArrayList<BSHostStatus>());
      status.setStatus(BootStrapStatus.BSStat.ERROR);
      updateStatus(requestId, status);

      response.setStatus(BSRunStat.OK);
      response.setLog("Host list is empty.");
      response.setRequestId(requestId);
      return response;
    } else {
      bsRunner = new BSRunner(this, info, bootStrapDir.toString(),
          bootScript, bootSetupAgentScript, bootSetupAgentPassword, requestId, 0L,
          this.masterHostname, info.isVerbose(), this.clusterOsFamily, this.projectVersion, this.serverPort);
      bsRunner.start();
      response.setStatus(BSRunStat.OK);
      response.setLog("Running Bootstrap now.");
      response.setRequestId(requestId);
      return response;
    }
  }

  /**
   * @param hosts
   * @return
   */
  public synchronized List<BSHostStatus> getHostInfo(List<String> hosts) {
    List<BSHostStatus> statuses = new ArrayList<BSHostStatus>();

    if (null == hosts || 0 == hosts.size() || (hosts.size() == 1 && hosts.get(0).equals("*"))) {
      for (BootStrapStatus status : bsStatus.values()) {
        if (null != status.getHostsStatus())
          statuses.addAll(status.getHostsStatus());
      }
    } else {
      // TODO make bootstrapping a bit more robust then stop looping
      for (BootStrapStatus status : bsStatus.values()) {
        for (BSHostStatus hostStatus : status.getHostsStatus()) {
          if (-1 != hosts.indexOf(hostStatus.getHostName())) {
            statuses.add(hostStatus);
          }
        }
      }
    }

    return statuses;
  }

  /**
   *
   */
  public synchronized void reset() {
    bsRunner = null;
  }
  
  public String getAgentDefaultLoginUser() {
	return this.agentDefaultLoginUser;
  }


  public String getAgentDefaultLoginPassword() {
	return this.agentDefaultLoginPassword;
  }

public String getBootstrapSSHUser() {
	return bootstrapSSHUser;
}

public String getClusterOsType() {
	return clusterOsType;
}
  


}
