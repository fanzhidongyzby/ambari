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
import os
import commands

SERVICE_NAME = "HermesStoreServer"


class HermesStoreServer(Script):

    def install(self, env):
        self.install_packages(env)
        self.configure(env)

        import params
        Links(params.new_hermes_install_path, params.hermes_install_path)

    def uninstall(self, env):
        Toolkit.uninstall_service("hermes")

    def configure(self, env):
        util.init_config(env)
        util.load_command_script(env, 'start_hermesstoreserver.sh', 'start_hermesstoreserver.sh.j2')

    def start(self, env):
        import params
        env.set_params(params)
        start_store_server_cmd = format("sudo bash -x {start_service_script} {start_store_server_script}")
        is_success = util.command_exe(start_store_server_cmd, SERVICE_NAME)
        if not is_success:
            Logger.error("Cannot allocate memory")

    def status(self, env):
        import status_params
        env.set_params(status_params)
        if not util.is_service_run(SERVICE_NAME):
            Logger.warning("{0} did not started!".format(SERVICE_NAME))
            raise ComponentIsNotRunning()

    def stop(self, env):
        import params
        env.set_params(params)
        service_pid = util.get_service_pid(SERVICE_NAME)
        if service_pid:
            stop_command = "sudo kill -9 {0}".format(service_pid)
            util.command_exe(stop_command, SERVICE_NAME)
        else:
            Logger.warning("{0} did not started!".format(SERVICE_NAME))

if __name__ == "__main__":
    HermesStoreServer().execute()
