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

class Datanode(Script):
  def install(self, env):
    import params
    self.install_packages(env)
    Logger.info("init datanode")
    #su pgxz -c '/usr/local/pgxz/bin/initdb -D /usr/local/pgxz/nodes/datanode --nodename datanode'
    utils().exe(params.datanode_install)
    utils().check_install(params.datanode_path)

    Links(params.new_pgxz_install_path, params.pgxz_install_path)
    Links(params.new_pgxz_conf_path_datanode, params.pgxz_conf_path_datanode)
    Links(params.new_pgxz_data_path_datanode, params.pgxz_data_path_datanode)

  def uninstall(self, env):
    Toolkit.uninstall_service("pgxz")

  def start(self, env):
    import params
    Logger.info("create datanode config")
    self.configure(env)

    Logger.info("start datanode")
    #su pgxz -c '/usr/local/pgxz/bin/pg_ctl start -D /usr/local/pgxz/nodes/datanode -Z datanode'
    utils().exe(params.datanode_start)
    utils().check_start(params.datanode_pid)


  def configure(self, env):
    import params
    Logger.info("create the config file by pgxz().init_datanode()")
    env.set_params(params)
    pgxz().init_datanode()

  def stop(self, env):
    import params
    Logger.info("Stop the datanode")
    #su pgxz -c '/usr/local/pgxz/bin/pg_ctl stop -D /usr/local/pgxz/nodes/datanode -Z datanode'
    utils().exe(params.datanode_stop)
    utils().check_stop(params.datanode_pid)
     
  def status(self, env):
    import params
    Logger.info("Status of the datanode")
    utils().check_process(params.datanode_pid)

if __name__ == "__main__":
  Datanode().execute()

