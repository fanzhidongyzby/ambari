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
import os
import commands
from configinit import configinit


from resource_management import *
from resource_management.core.logger import Logger
from utils import utils



class PgMaster(Script):
  def install(self, env):

    Logger.info("install Pg")
    excludePackage = ['pgxzm-center']
    self.install_packages(env,excludePackage)

    # create dba user for pg
    #	configinit().create_pg_dba(env)

    # get a best avilable dir for pg data
    #	configinit().get_avilable_dir(env)


    import params
    Logger.info("create  user and passwd")
    Logger.info(params.pgxx_passwd)

    Logger.info("create  install dir")

    Logger.info(params.pgxx_install_path)
    utils().exe(params.create_install_dir)
    utils().exe(params.chown_install_dir)
    Logger.info("create log dir")
    Logger.info(params.pgxx_log_path)
    utils().exe(params.create_log_dir)
    utils().exe(params.chown_log_dir)
    Logger.info("process initdb")
    utils().exe(params.pg_init_db)
    Logger.info("update configure parameters")
    self.configure(env)
    self.start(env)
    self.createdbsuperuser(env)

    Links(params.new_postgresql_install_path, params.postgresql_install_path)

  def uninstall(self, env):
      Toolkit.uninstall_service("postgresql")

  def createdbsuperuser(self, env):
    Logger.info("create super user for postgresql --")
    Logger.info("load exe scripts")
    import params
    File(params.config_runner_script_for_db,
       mode=0755,
       content=StaticFile('createdbsuperuser.sh')
       )
    Logger.info("exe scripts create user")
    if os.path.exists(params.config_runner_script_for_db):
      Logger.info(params.create_superuser_sh)
      val = os.system(params.create_superuser_sh)
      # createdbsuperuser.sh pgxx_postgre_port pgxx_user   'CREATE ROLE  pgxx_db_user SUPERUSER;'
      #		val= os.system("su hdfs -c '/usr/local/lhotse_runners/initLogScript.sh /usr/local/lhotse_runners'")
      Logger.info("exe createdbsuperusersh result = " + str(val) )
    else:
      Logger.info('createdbsuperuser.sh is not exist')

  def start(self, env):
    Logger.info("start the pg")
    import params
    env.set_params(params)

    self.configure(env)
    utils().exe(params.pg_start)
    #		utils.exe(params.pg_cofig_check)

    Links(params.new_postgresql_data_path, params.postgresql_data_path)
    Links(params.new_postgresql_log_path, params.postgresql_log_path)


  def stop(self, env):
      Logger.info("Stop the pg")
      import params
      env.set_params(params)
      utils().exe(params.pg_stop)

  def configure(self, env):
    import params
    env.set_params(params)
    Logger.info("update pg configs")
    configinit().update_pg(env)



  def status(self, env):
    Logger.info("check pg server running status---")
    #	import params
    #	utils().exe_status(params.pg_status)
    import params
    #Toolkit1.check_service(params.pg_status)
    Toolkit.check_command(params.pg_status,keyword = "is running")
    #	import params
    #	utils.check_postgre_running(params.pg_status)

if __name__ == "__main__":
  PgMaster().execute()

