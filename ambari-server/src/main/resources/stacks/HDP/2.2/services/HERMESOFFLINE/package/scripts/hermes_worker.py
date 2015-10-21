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


SERVICE_NAME = "HermesWorker"


class HermesWorker(Script):

    def install(self, env):
        self.install_packages(env)
        self.configure(env)

        import params
        Links(params.new_hermes_install_path, params.hermes_install_path)

    def uninstall(self, env):
        Toolkit.uninstall_service("hermes")

    def configure(self, env):
        util.init_config(env)
        util.load_command_script(env, 'start_worker.sh', 'start_worker.sh.j2')

    def start(self, env):
        import params
        env.set_params(params)

        shards = len(params.worker_hosts)
        shardid = str(sorted(params.worker_hosts).index(params.hostname))
        cmd_args = " {0} {1} {2}".format(shards, shardid, 3)
        start_worker_cmd = format("sudo bash -x {start_service_script} {start_worker_script} {hermes_topic}") + cmd_args
        is_success = util.command_exe(start_worker_cmd, SERVICE_NAME)
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
    HermesWorker().execute()
