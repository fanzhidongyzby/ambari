#!/usr/bin/python
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

import commands
from resource_management import *
from resource_management.core.logger import Logger

class SparkClient(Script):
  def install(self, env):
    import params
    env.set_params(params)
    
    excludePackage = ['livy-server*']
    self.install_packages(env, excludePackage)
    
    rm_command = format("rm -rf {spark_client_home}")
    Logger.info(rm_command)
    self.command_exe(rm_command)
    
    Links(params.spark_client_home, params.spark_home)
    
    self.configure(env)
  
  def uninstall(self, env):
    import params
    env.set_params(params)
    
    uninstall_cmd = format("rm -rf  {spark_client_home}")
    Logger.info(uninstall_cmd)
    self.command_exe(uninstall_cmd)

  def configure(self, env):  
    import params
    env.set_params(params)
  
    """
    XmlConfig("spark-defaults.xml",
      conf_dir=params.spark_conf_dir,
      configurations=params.config['configurations']['spark-defaults'],
      configuration_attributes=params.config['configuration_attributes']['spark-defaults'],
      owner=params.spark_user,
      group=params.user_group
    )
    """
    
    # add template files
    File(params.spark_defaults_conf_file, mode=0644, content=Template("spark-defaults.conf.j2"))
    File(params.spark_env_file, mode=0644, content=Template("spark-env.j2"))
    
    copy_cmd = format("cp -arpf {hive_site_file} {spark_conf_dir}")
    Logger.info(copy_cmd)
    self.command_exe(copy_cmd)
        
    copy_cmd = format("cp -arpf {tez_site_file} {spark_conf_dir}")
    Logger.info(copy_cmd)
    self.command_exe(copy_cmd)
    
  def command_exe(self, command):
        (ret, output) = commands.getstatusoutput(command)
        Logger.info(command)
        if ret != 0:
            Logger.info("exe command :{0} failed".format(command))
            Logger.error(output)
        else:
            Logger.info("exe command :{0} success".format(command))
            Logger.info(output)
        return output

if __name__ == "__main__":
  SparkClient().execute()

