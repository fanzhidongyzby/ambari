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
from resource_management import *
from utils import utils

class HWI(Script):

  def install(self, env):
    import params
    Toolkit.yum_install("hive-hwi")

  def uninstall(self, env):
    Toolkit.uninstall_service("hive")

  def start(self, env):
        import os
        import params
        env.set_params(params)

        self.configure(env) 
        Logger.info("start hwi")
        utils().exe(params.hwi_start_command)
        
  def configure(self, env):
    import params
    env.set_params(params)
    XmlConfig("hive-site.xml",
            conf_dir=params.hive_config_dir,
            configurations=params.config['configurations']['hive-site'],
            configuration_attributes=params.config['configuration_attributes']['hive-site'],
            owner=params.hive_user,
            group=params.user_group,
            mode=0644)
    
  def status(self, env):
     Toolkit.check_process("org.apache.hadoop.hive.hwi.HWIServer")

  def stop(self, env):
     Toolkit.kill_process("org.apache.hadoop.hive.hwi.HWIServer")    

if __name__ == "__main__":
  HWI().execute()
