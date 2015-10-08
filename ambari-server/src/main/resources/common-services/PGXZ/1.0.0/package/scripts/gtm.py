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
import os
from resource_management import *
from pgxz import pgxz
from utils import utils
from resource_management.core.logger import Logger

class Gtm(Script):
  def install(self, env):
    import params
    self.install_packages(env)
    Logger.info("init gtm")
    #su pgxz -c '/usr/local/pgxz/bin/initgtm -Z gtm -D /usr/local/pgxz/nodes/gtm'
    utils().exe(params.gtm_install)
    utils().check_install(params.gtm_path)

    Links(params.new_pgxz_install_path, params.pgxz_install_path)
    Links(params.new_pgxz_conf_path_gtm, params.pgxz_conf_path_gtm)
    Links(params.new_pgxz_data_path_gtm, params.pgxz_data_path_gtm)

  def uninstall(self, env):
    Toolkit.uninstall_service("pgxz")

  def start(self, env):
    import params
    Logger.info("create gtm config")
    self.configure(env)

    Logger.info("start gtm")
    #su pgxz -c '/usr/local/pgxz/bin/gtm_ctl -Z gtm -D /usr/local/pgxz/nodes/gtm start'
    utils().exe(params.gtm_start)
    utils().check_start(params.gtm_pid)

  def configure(self, env):
    Logger.info("create the config file by pgxz().init_gtm()")
    import params
    env.set_params(params)
    pgxz().init_gtm()

  def stop(self, env):
    import params
    Logger.info("Stop the gtm")
    #su pgxz -c '/usr/local/pgxz/bin/gtm_ctl -Z gtm -D /usr/local/pgxz/nodes/gtm stop'
    utils().exe(params.gtm_stop)
    utils().check_stop(params.gtm_pid)

  def status(self, env):
    import params
    Logger.info("Status of the gtm")
    utils().check_process(params.gtm_pid)

if __name__ == "__main__":
  Gtm().execute()
