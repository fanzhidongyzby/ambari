/*
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

package org.apache.ambari.server.audit;

import org.apache.ambari.server.api.services.Request;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.ws.rs.core.Response;

/**
 * Write audit info to log
 */
public class LogAuditor extends Auditor {

  /**
   *  Logger instance.
   */
  private final static Logger LOG = LoggerFactory.getLogger(LogAuditor.class);


  /**
   * Set a mark
   */
  @Override
  public void mark() {
    LOG.debug("log auditor set a mark");
  }

  /**
   * Record audit info to log
   *
   * @param message
   */
  @Override
  public void record(String message) {
    String userName = currentUser();
    LOG.info(userName + " " + message);
  }

  /**
   * Record api request and response
   *
   * @param request
   * @param response
   */
  @Override
  public void record(Request request, Response response) {
    if (request == null || request.getRequestType() == Request.Type.GET) {
      // ignore get request
      return;
    }
    String userName = currentUser();
    String uri = request.getURI();
    int status = response.getStatus();
    LOG.info(userName + " " + uri + " " + status);
  }
}
