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
from resource_management.core import sudo
from resource_management.core.logger import Logger
import os
import time

class KafkaBroker(Script):
  def install(self, env):
    self.install_packages(env)
    self.configure(env)

  def uninstall(self, env):
    Toolkit.uninstall_service("kafka")

  def configure(self, env):
    import params
    env.set_params(params)
    File(os.path.join(params.kafka_manager_dir + '/conf', 'application.conf'),
       owner='root',
       group='root',
       mode=0644,
       content=Template("application.conf.j2")
    )

  #def pre_rolling_restart(self, env):
    #import params
    #env.set_params(params)
    #upgrade.prestart(env, "kafka-broker")

  def start(self, env, rolling_restart=False):
    import params
    env.set_params(params)
    self.configure(env)

    pid_file = params.kafka_manager_pid_file
    if pid_file and os.path.isfile(pid_file):
        return

    daemon_cmd = "nohup {0}/bin/kafka-manager -Dconfig.file={0}/conf/application.conf -Dhttp.port={1} &".format(params.kafka_manager_dir, str(params.kafka_manager_http_port))
    Execute(daemon_cmd,
            user=params.kafka_user,
    )

    time.sleep(15)
    cmd = "curl -d 'name=tbds_kafka&zkHosts={0}&kafkaVersion=0.8.1.1' http://127.0.0.1:{1}/clusters".format(params.zookeeper_connect, str(params.kafka_manager_http_port))
    Execute(cmd,
            user=params.kafka_user,
            )

  def stop(self, env, rolling_restart=False):
    import params
    env.set_params(params)
    self.configure(env)
    try:
        pid = int(sudo.read_file(params.kafka_manager_pid_file))
        code, out = shell.call(["kill","-15", str(pid)])
    except:
        Logger.warning("Pid file {0} does not exist".format(params.kafka_manager_pid_file))
        return

    if code:
       Logger.warning("Process with pid {0} is not running. Stale pid file"
                 " at {1}".format(pid, params.kafka_manager_pid_file))

  def status(self, env):
    import status_params
    env.set_params(status_params)
    check_process_status(status_params.kafka_manager_pid_file)

if __name__ == "__main__":
  KafkaBroker().execute()
