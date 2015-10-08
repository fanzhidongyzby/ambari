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
from resource_management import *
from configinit import configinit
from init_pg import init_pg

class PgMaster(Script):
  def install(self, env):
    import params
    env.set_params(env)

    excludePackage = ['plclient*','thive']
    self.install_packages(env,excludePackage)
  

    configinit().init_pg_scripts()
    configinit().init_checkstatus_script()

    print "--------initdb"
    (ret, output) = commands.getstatusoutput("/etc/init.d/postgresql-9.3 initdb")
    print ret
    print output
    if ret != 0:
      sys.exit(1)
    
    self.configure(env)
    print "--------start db"
    (ret, output) = commands.getstatusoutput("/etc/init.d/postgresql-9.3 start")
    print ret
    print output
    
    if ret != 0 :
      sys.exit(1)
    
    print '----------init pg'
    init_pg().init(env)
#    cmd = format("bash -x {tmp_dir}/initpg.sh {pg_server_hosts} {pg_server_port} {params.pg_server_user} {params.pg_server_password} {params.hive_plc_user} {params.hive_plc_password}")
#    (ret, output) = commands.getstatusoutput(cmd)
#    print ret
#    print output
#    
#    if ret != 0 :
#       sys.exit(1)

    Links(params.new_thive_conf_path_pgsql, params.thive_conf_path_pgsql)
    Links(params.new_thive_log_path_pgsql, params.thive_log_path_pgsql)
    Links(params.new_thive_data_path_pgsql, params.thive_data_path_pgsql)


  def uninstall(self, env):
    Toolkit.uninstall_service("thive")

  def start(self, env):
    import params
    env.set_params(params)

    print 'refresh configs'
    self.configure(env)

    print 'start the pg';
    cmd = format("/etc/init.d/postgresql-9.3 start")
    
    (ret, output) = commands.getstatusoutput(cmd)
    print "[ret]"
    print ret
    print "[output]"
    print output
    if ret != 0:
      sys.exit(1)

    init_pg().create_pg_user(env)

  def stop(self, env):
    import params
    env.set_params(params)

    print 'Stop the pg';
    cmd = format("/etc/init.d/postgresql-9.3 stop")

    (ret, output) = commands.getstatusoutput(cmd)
    print "[ret]"
    print ret
    print "[output]"
    print output
   
    

  def configure(self, env):
    import params
    env.set_params(params)
    print "update thive configs"
    configinit().update_pg_config(env)


     
  def status(self, env):
    import params
    env.set_params(params)
    
    print 'Status of thive master'

    cmd = format("bash -x {checkstatus_script} {pg_process_keyword} 1")
    
    (ret, output) = commands.getstatusoutput(cmd)
    print ret
    print output

    if ret == 0:
      print "pg server is running"
    else:
      raise ComponentIsNotRunning()

if __name__ == "__main__":
  PgMaster().execute()

