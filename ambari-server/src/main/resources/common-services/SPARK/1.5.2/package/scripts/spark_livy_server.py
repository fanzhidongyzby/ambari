#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE files
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this files
to you under the Apache License, Version 2.0 (the
"License"); you may not use this files except in compliance
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
from resource_management.libraries.resources.execute_hadoop import ExecuteHadoop

class SparkLivyServer(Script):

    def install(self, env):
        import params
        env.set_params(params)
        
        excludePackage = ['spark*']
        self.install_packages(env, excludePackage)
        
        self.configure(env)
        
        rm_command = format("rm -rf {livy_server_link_home}")
        Logger.info(rm_command)
        self.command_exe(rm_command)
        
        Links(params.livy_server_link_home, params.livy_server_home)
        
    def uninstall(self, env):
        import params
        env.set_params(params)
        
        rm_command = format("rm -rf {livy_server_link_home}")
        Logger.info(rm_command)
        self.command_exe(rm_command)

    def configure(self, env):
        import params
        env.set_params(params)

        # add template files
        File(params.livy_conf_path, mode=0644, content=Template("livy-defaults.conf.j2"))
        File(params.livy_env_path, mode=0755, content=Template("livy-server-env.j2"))

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        
        mkdir_command = format("fs -mkdir -p {params.livy_jar_path}")
        ExecuteHadoop(mkdir_command,
                      user=params.hdfs_user,
                      conf_dir=params.hadoop_conf_dir
        )
        
        copy_command = format("fs -put -f {livy_local_jar_file} {livy_jar_path}")
        ExecuteHadoop(copy_command,
                      user=params.hdfs_user,
                      conf_dir=params.hadoop_conf_dir
        )
        
        start_command = format("source {livy_env_path}; bash +x {livy_server_start_script} >> /usr/hdp/2.2.0.0-2041/livy/livy.log 2>&1 &")
        Logger.info(start_command)
        Execute(start_command,
            user=params.spark_user,
            environment={'JAVA_HOME': params.java_home}
        )

    def stop(self, env):
        import params
        env.set_params(params)

        # kill livy process
        kill_livy_process = "pids=$(ps -ef | grep 'com.cloudera.hue.livy.server.Main' | grep -v 'grep'| awk '{print $2}');for pid in ${pids[@]};do  kill -9 $pid; done"
        Logger.info(kill_livy_process)
        self.command_exe(kill_livy_process)

    def status(self, env):
        import status_params
        env.set_params(status_params)
        
        process_check_command = "ps -ef | grep 'com.cloudera.hue.livy.server.Main' | grep -v grep"
        output = self.command_exe(process_check_command)
        if not output:
            Logger.warning("{0} did not started!".format("Spark livy server"))
            raise ComponentIsNotRunning()

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
    SparkLivyServer().execute()
