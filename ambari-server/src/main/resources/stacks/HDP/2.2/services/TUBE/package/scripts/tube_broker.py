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


SERVICE_NAME = "broker"
SERVICE_PROCESS = "ServerStartup"


class TubeBroker(Script):

    def install(self, env):
        self.install_packages(env)
        self.configure(env)

        import params
        Links(params.new_tube_install_path, params.tube_install_path)

    def uninstall(self, env):
        Toolkit.uninstall_service("tube")

    def configure(self, env):
        util.init_config(env)

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        util.service_action(SERVICE_NAME, "start")

    def status(self, env):
        import status_params
        env.set_params(status_params)
        if not util.is_service_run(SERVICE_PROCESS):
            Logger.warning("{0} did not started!".format(SERVICE_NAME))
            raise ComponentIsNotRunning()

    def stop(self, env):
        import params
        env.set_params(params)
        util.service_action(SERVICE_NAME, "stop")

if __name__ == "__main__":
    TubeBroker().execute()
