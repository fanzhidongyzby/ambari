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

from resource_management import *
from resource_management.core import shell
from resource_management.core.logger import Logger
import os

class NiFi(Script):
  def install(self, env):
    self.install_packages(env)
    self.configure(env)

    import params
    Links(params.new_nifi_config_path, params.nifi_conf_dir)
    Links(params.new_nifi_log_path, params.nifi_log_dir)

  def uninstall(self, env):
    Toolkit.uninstall_service("nifi")

  def configure(self, env):
    import params
    env.set_params(params)
    File(os.path.join(params.nifi_conf_dir, 'nifi.properties'),
         owner=params.nifi_user,
         group='hadoop',
         mode=0644,
         content=Template("nifi.properties.j2")
         )
    File(os.path.join(params.nifi_conf_dir, 'bootstrap.conf'),
         owner=params.nifi_user,
         group='hadoop',
         mode=0644,
         content=InlineTemplate(params.nifi_bootstrap_conf_template)
         )

  #def pre_rolling_restart(self, env):
    #import params
    #env.set_params(params)
    #upgrade.prestart(env, "kafka-broker")

  def start(self, env, rolling_restart=False):
    import params
    env.set_params(params)
    self.configure(env)

    pid_file = params.nifi_pid_file
    if pid_file and os.path.isfile(pid_file):
        return

    daemon_cmd = "export PATH={0}/bin:$PATH;".format(params.java64_home)
    daemon_cmd += "{0} start".format(params.nifi_bin)
    Execute(daemon_cmd,
            user=params.nifi_user,
    )

  def stop(self, env, rolling_restart=False):
    import params
    env.set_params(params)
    self.configure(env)
    daemon_cmd = "{0} stop".format(params.nifi_bin)
    Execute(daemon_cmd,
            user=params.nifi_user,
            )

  def status(self, env):
    import status_params
    env.set_params(status_params)
    self.check_nifi_process_status(status_params.nifi_pid_file)

  def check_nifi_process_status(self, pid_file):
    """
    Function checks whether process is running.
    Process is considered running, if pid file exists, and process with
    a pid, mentioned in pid file is running
    If process is not running, will throw ComponentIsNotRunning exception

    @param pid_file: path to service pid file
    """
    if not pid_file or not os.path.isfile(pid_file):
        raise ComponentIsNotRunning()

    try:
        lines = [line.rstrip('\n') for line in open(pid_file)]
        pid = int(lines[2].split('=')[1]);
    except:
        Logger.warn("Pid file {0} does not exist".format(pid_file))
        raise ComponentIsNotRunning()

    code, out = shell.call(["ps","-p", str(pid)])

    if code:
        Logger.debug("Process with pid {0} is not running. Stale pid file"
                     " at {1}".format(pid, pid_file))
        raise ComponentIsNotRunning()
    pass

if __name__ == "__main__":
    NiFi().execute()
