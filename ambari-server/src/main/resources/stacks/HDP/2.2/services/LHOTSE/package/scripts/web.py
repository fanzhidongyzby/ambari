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
import commands
from resource_management import *
from resource_management.core.logger import Logger

from mysql_service import mysql_service
from configinit import configinit
import web

class Web(Script):

  def install(self, env):
    import params

    excludePackage = ['lhotse-base*','mysql-server*','mysql','lhotse-service*','lhotse-runner*','vsftpd*']
    self.install_packages(env,excludePackage)

    self.configure(env)

    Links(params.new_lhotse_install_path_web, params.lhotse_install_path_web)
    Links(params.new_lhotse_log_path_web, params.lhotse_log_path_web)
    Links(params.new_lhotse_config_path_web, params.lhotse_config_path_web)

  def uninstall(self, env):
    Toolkit.uninstall_service("lhotse")

  def configure(self, env):
    import params
    env.set_params(params)

    File(params.config_web_script,
         mode=0755,
         content=StaticFile('configWeb.sh')
    )

    configinit().update_web_config()
    
    cmd = format("bash -x {config_web_script} {lhotse_web_hosts} {lhotse_web_listen_port}")

    (ret, output) = commands.getstatusoutput(cmd)
    print "update web httpd------output-------"
    print output
    print ret

    if ret != 0:
        print 'update httpd config fail'
        sys.exit(1)


  def start(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    commands.getstatusoutput("service httpd restart")

  def stop(self, env):
    import params
    env.set_params(params)
	
    #delete conf file
    cmd = format("rm {web_httpd_conf_path}/lhotse_web.conf")
    (ret, output) = commands.getstatusoutput(cmd)
    print "delete lhotse_web.conf output"
    print output
    print ret
    
    commands.getstatusoutput("service httpd restart")


  def status(self, env):
    import params
    cmd = "curl -I \"" + params.lhotse_web_url + "\" 2> /dev/null | awk 'NR==1{print}' | awk '{print $2}'"
    Logger.error("run cmd = {0}".format(cmd))
    (ret, output) = commands.getstatusoutput(cmd)
    if output != "200" :
      Logger.error("lhotse web not exists")
      raise ComponentIsNotRunning()

if __name__ == "__main__":
  Web().execute()
