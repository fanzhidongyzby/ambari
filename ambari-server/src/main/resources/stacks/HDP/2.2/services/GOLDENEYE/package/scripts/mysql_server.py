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
import os
import sys
from resource_management import *

from mysql_service import mysql_service
from configinit import configinit

class MysqlServer(Script):

  def install(self, env):
    import params
    print 'install goldeneye'
    excludePackage = ['goldeneye-web']
    self.install_packages(env,excludePackage)
	
    print 'init scripts'
    configinit().init_mysql_scripts()
	
    print 'update configs'
    self.configure(env)

    Links(params.new_goldeneye_conf_path_metadb, params.goldeneye_conf_path_metadb)
    Links(params.new_goldeneye_log_path_metadb, params.goldeneye_log_path_metadb)

  def uninstall(self, env):
    Toolkit.uninstall_service("goldeneye")

  def configure(self, env):
    import params
    env.set_params(params)

    cmd = format("bash -x {start_mysql_script} {goldeneye_database_host} {goldeneye_database_port} {goldeneye_data_dir} {goldeneye_database_username} {goldeneye_database_password} {gri_ge_script} {gri_monitor_script} {goldeneye_web_host}")

    val= os.system(cmd)
    print val


  def start(self, env):
    import params
    env.set_params(params)
    mysql_service(daemon_name=params.daemon_name, action = 'start')
    print "ok"

    Links(params.new_goldeneye_data_path_metadb, params.goldeneye_data_path_metadb)

  def stop(self, env):
    import params
    env.set_params(params)

    mysql_service(daemon_name=params.daemon_name, action = 'stop')

  def status(self, env):
    import params
    mysql_service(daemon_name=params.daemon_name, action = 'status')

if __name__ == "__main__":
  MysqlServer().execute()
