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


class TdbusTopicToolClient(Script):

    def install(self, env):
        self.install_packages(env)
        self.configure(env)

        import params
        Links(params.new_tdbus_install_path, params.tdbus_install_path)

    def uninstall(self, env):
        Toolkit.uninstall_service("tdbus")

    def configure(self, env):
        util.init_config(env)

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)

        topic_tool_client = format("(nohup  python {tube_topic_tool_client}&) &> {new_tdbus_install_path}/topic_client.log")
        (ret, output) = commands.getstatusoutput(topic_tool_client)
        Logger.info(topic_tool_client)
        if ret != 0:
            Logger.info("start {0}  failed".format("topic tools client"))
            Logger.error(output)
        else:
            Logger.info("start {0}  success".format("topic tools client"))
            Logger.info(output)

    def status(self, env):
        import status_params
        env.set_params(status_params)
        process_check_command = "sudo ps aux | grep tube_topic_tool_client  | grep -v 'grep' "
        output = util.exe_command(process_check_command)
        if not output:
            raise ComponentIsNotRunning()

    def stop(self, env):
        import params
        env.set_params(params)
        process_check_command = "sudo ps aux | grep tube_topic_tool_client | grep -v 'grep' |  awk '{print $2}' | xargs kill"
        (ret, output) = commands.getstatusoutput(process_check_command)
        Logger.info(process_check_command)
        if ret != 0:
            Logger.error(output)
            Logger.error("can no stop {0}!".format("tube_topic_tool_client"))

if __name__ == "__main__":
    TdbusTopicToolClient().execute()
