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

class Coordinator(Script):
  def install(self, env):
    import params
    self.install_packages(env)
    Logger.info("init coordinator")
    #su pgxz -c '/usr/local/pgxz/bin/initdb -D /usr/local/pgxz/nodes/coordinator --nodename coordinator'
    utils().exe(params.coordinator_install)
    utils().check_install(params.coordinator_path)

  def start(self, env):
    import params
    Logger.info("create coordinator config")
    self.configure(env)

    Logger.info("start coordinator")
    #su pgxz -c '/usr/local/pgxz/bin/pg_ctl start -D /usr/local/pgxz/nodes/coordinator -Z coordinator'
    utils().exe(params.coordinator_start)
    utils().check_start(params.coordinator_pid)

    utils().syncCluster(params.coordinator_hosts, params.datanode_hosts, params.coordinator_port, params.datanode_port, params.host_name, params.sql_str)

  def configure(self, env):
    import params
    Logger.info("create the config file by pgxz().init_coor()")
    env.set_params(params)
    pgxz().init_coor()

  def stop(self, env):
    import params
    Logger.info("Stop the coordinator")
    #su pgxz -c '/usr/local/pgxz/bin/pg_ctl stop -D /usr/local/pgxz/nodes/coordinator -Z coordinator'
    utils().exe(params.coordinator_stop)
    utils().check_stop(params.coordinator_pid)
     
  def status(self, env):
    import params
    Logger.info("Status of the coordinator")
    utils().check_process(params.coordinator_pid)

if __name__ == "__main__":
  Coordinator().execute()


