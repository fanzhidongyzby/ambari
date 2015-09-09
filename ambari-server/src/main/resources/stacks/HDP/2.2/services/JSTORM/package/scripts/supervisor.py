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
from resource_management import *
from resource_management.core.logger import Logger
from utils import utils

from configinit import configinit

class Supervisor(Script):

  def install(self, env):
    import params
    env.set_params(params)
    self.install_packages(env)

    Links(params.new_jstorm_install_path, params.jstorm_install_path)
    Links(params.new_jstorm_config_path, params.jstorm_config_path)
    Links(params.new_jstorm_log_path, params.jstorm_log_path)

  def configure(self, env):
    import params
    env.set_params(params)
    Directory(params.local_dir,
              owner=params.storm_user,
              group=params.storm_group,
              mode=0755,
              recursive=True
              )
    configinit().update_supervisor_config()

  def start(self, env, rolling_restart=False):
    import params
    import status_params
    env.set_params(params)
    self.configure(env)    
    cmd = "su {0} -c '{1}/start-supervisor.sh'".format(params.storm_user, params.bin_dir)
    Logger.info("start supervisor")
    utils().exe(cmd)
    utils().check_process(status_params.proc_supervisor_name)

    Links(params.new_jstorm_data_path, params.jstorm_data_path)

  def stop(self, env, rolling_restart=False):
    import params
    import status_params
    env.set_params(params)
    cmd = "su {0} -c '{1}/stop-supervisor.sh'".format(params.storm_user, params.bin_dir)
    Logger.info("stop supervisor")
    utils().exe(cmd)
    utils().check_stop(status_params.proc_supervisor_name) 

  def status(self, env):
    import status_params
    utils().check_process(status_params.proc_supervisor_name) 


if __name__ == "__main__":
  Supervisor().execute()

