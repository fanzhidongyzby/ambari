#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import sys
from resource_management import *
from resource_management.core.logger import Logger
from utils import utils

class Docker(Script):

  def install(self, env):
    Logger.info("install Docker")
    excludePackage = ['haproxy-ng', 'hadoop-ng', 'portal_api_server', 'resource_monitor']
    self.install_packages(env,excludePackage)


  def configure(self, env):
    print 'configure Docker'

  def start(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    Logger.info("start Docker")
    utils().exe(params.docker_start)

  def stop(self, env):
    import params
    env.set_params(params)

    Logger.info("stop Docker")
    utils().exe(params.docker_stop)

  def status(self, env):
    import params
    Logger.info("check status of Docker")
    utils().check_service_status(params.docker_service, params.docker_status_key)                                                                                                            

if __name__ == "__main__":
    Docker().execute()

