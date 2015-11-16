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

Ambari Agent

"""

from resource_management import *
import util
import commands


class TubeMaster(Script):

    def install(self, env):
        self.install_packages(env)
        import params
        Links(params.new_tube_install_path, params.tube_install_path)

        self.configure(env)


    def uninstall(self, env):
        Toolkit.uninstall_service("tube")

    def configure(self, env):
        import params
        File(params.topic_tool_server, mode=0755, content=StaticFile('topic_tool.py'))
        util.init_config(env)

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)

        start_topic_tool = format("bash +x {start_tool_server}")
        (ret, output) = commands.getstatusoutput(start_topic_tool)
        Logger.info(start_topic_tool)
        if ret != 0:
            Logger.info("start {0}  failed".format("topic tools"))
            Logger.error(output)
        else:
            Logger.info("start {0}  success".format("topic tools"))
            Logger.info(output)

    def status(self, env):
        import status_params
        env.set_params(status_params)
        # warring defalut port is 9002
        port_check_command = format("sudo ps aux | grep 'topic_tool.py'  | grep -v 'grep' ")
        output = util.exe_command(port_check_command)
        if not output:
            Logger.warning("{0} did not started!".format("Topic Tool Server"))
            raise ComponentIsNotRunning()

    def stop(self, env):
        import params
        env.set_params(params)
        port_check_command = "sudo netstat -tlnp|grep 9002|awk  '{print $7}'|awk -F '/' '{print $1}'|xargs kill"
        (ret, output) = commands.getstatusoutput(port_check_command)
        Logger.info(port_check_command)
        if ret != 0:
            Logger.error(output)
            Logger.error("can no stop {0}!".format("Topic Tool Server"))


if __name__ == "__main__":
    TubeMaster().execute()
