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
import web

class Ftp(Script):

  def install(self, env):
    import params
    excludePackage = ['lhotse-runner*','lhotse-base*','lhotse-service*','mysql-server*','mysql','lhotse-web*']
    self.install_packages(env,excludePackage)
    self.configure(env)

    Links(params.new_lhotse_install_path_ftp, params.lhotse_install_path_ftp)
    Links(params.new_lhotse_log_path_ftp, params.lhotse_log_path_ftp)
    Links(params.new_lhotse_config_path_ftp, params.lhotse_config_path_ftp)
    Links(params.new_lhotse_data_path_ftp, params.lhotse_data_path_ftp)

  def uninstall(self, env):
    Toolkit.uninstall_service("lhotse")

  def configure(self, env):
    import params
    env.set_params(params)

    File(params.config_ftp_script,
         mode=0755,
         content=StaticFile('configFtp.sh')
    )

    cmd = format("bash -x {config_ftp_script} {ftp_server_root_path} {ftp_server_port} {ftp_server_user} {ftp_server_pwd}")
    print cmd

    val = os.system(cmd)

    print val


  def start(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    mysql_service(daemon_name=params.ftp_service_daemon, action = 'start')

  def stop(self, env):
    import params
    env.set_params(params)

    mysql_service(daemon_name=params.ftp_service_daemon, action = 'stop')

  def status(self, env):
    import params

    mysql_service(daemon_name=params.ftp_service_daemon, action = 'status')

if __name__ == "__main__":
  Ftp().execute()
