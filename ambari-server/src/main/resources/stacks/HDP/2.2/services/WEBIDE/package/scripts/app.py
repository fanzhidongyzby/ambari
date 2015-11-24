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
from resource_management.core.resources import Execute
from resource_management.core.logger import Logger


class WebIDE(Script):

    def install(self, env):
        import params
        self.install_packages(env)

        Links(params.new_webide_install_path, params.webide_install_path)
        Links(params.new_webide_log_path, params.webide_log_path)
        self.configure(env)
        

    def uninstall(self, env):
        Toolkit.uninstall_service("webide")

    def configure(self, env):
        import params
        env.set_params(params)

        # add template files
        File(params.webide_app_server_path, mode=0644, content=Template("server.xml.j2"))
        File(params.webide_app_properties_path, mode=0644, content=Template("webide.properties.j2"))
        File(params.webide_app_sql_path, mode=0655, content=StaticFile('app.sql'))
        
    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        
        # init database
        (ret, output) = commands.getstatusoutput(params.webide_db_exist_cmd)
        if ret != 0:
            self.init_app_sql_data()
        
        start_command = format("bash +x {webide_app_start_script}")
        Logger.info(start_command)
        Execute(start_command,
            user='root',
            environment={'JAVA_HOME': params.java_home}
        )

    def stop(self, env):
        import params
        env.set_params(params)

        stop_command = format("bash +x {webide_app_stop_script}")
        Logger.info(stop_command)
        self.command_exe(stop_command)
        # kill zombie process
        kill_zobie_process = "ps -ef | grep '/usr/hdp/2.2.0.0-2041/webide/webide-app' | grep -v 'grep'| awk '{print $2}' | xargs kill -9"
        Logger.info(kill_zobie_process)
        self.command_exe(kill_zobie_process)

    def status(self, env):
        import status_params
        env.set_params(status_params)
        # warring defalut port is 9090
        process_check_command = "sudo ps aux | grep '/usr/hdp/2.2.0.0-2041/webide/webide-app'  | grep -v 'grep' "
        output = self.command_exe(process_check_command)
        if not output:
            Logger.warning("{0} did not started!".format("webide APP server"))
            raise ComponentIsNotRunning()

    def init_app_sql_data(self):
        createuser_command = format("{postgresql_install_path}/bin/createuser webide -h {pg_host} -U postgres -p {pg_port} -d -S -R")
        self.command_exe(createuser_command)
        createdb_command = format("{postgresql_install_path}/bin/createdb webide -h {pg_host} -U webide -p {pg_port}")
        self.command_exe(createdb_command)
        load_data_command = format("{postgresql_install_path}/bin/psql -U webide -d webide -h {pg_host} -p {pg_port} -f {webide_app_sql_path}")
        self.command_exe(load_data_command)

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
    WebIDE().execute()
