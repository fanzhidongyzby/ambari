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

from resource_management import *
from resource_management.core.logger import Logger
from utils import utils
from config import config

class Cgi(Script):

  def install(self, env):
    Logger.info("install Cgi")
    excludePackage = ["pgxzm-center", "pgxzm-agent", "pgxzm-web", "postgresql93*"]
    self.install_packages(env,excludePackage)

    import params
    Links(params.new_pgxzm_install_path, params.pgxzm_install_path)
    Links(params.new_pgxzm_conf_cgi, params.pgxzm_conf_cgi)

  def uninstall(self, env):
    Toolkit.uninstall_service("pgxzm")

  def configure(self, env):
    Logger.info('configure Cgi')
    config().update_cgi(env)

  def start(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    Logger.info("start Cgi")
    utils().exe(params.cgi_start)

  def stop(self, env):
    import params
    env.set_params(params)

    Logger.info("stop Cgi")
    utils().exe(params.cgi_stop)

  def status(self, env):
    import params
    Logger.info("check status of Cgi")
    utils().check_url(params.cgi_status)

if __name__ == "__main__":
    Cgi().execute()


