#!/usr/bin/env python
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
from ams import ams
from ams_service import ams_service
from status import check_service_status

class AmsMonitor(Script):
  def install(self, env):
    self.install_packages(env, exclude_packages = ['ambari-metrics-collector'])
    self.configure(env) # for security

    import params
    Links(params.new_metrics_install_path_monitor_bin, params.metrics_install_path_monitor_bin)
    Links(params.new_metrics_install_path_monitor_lib, params.metrics_install_path_monitor_lib)
    Links(params.new_metrics_config_path_hbase, params.metrics_config_path_hbase)
    Links(params.new_metrics_config_path_monitor, params.metrics_config_path_monitor)

  def uninstall(self, env):
    Toolkit.uninstall_service("metrics")

  def configure(self, env):
    import params
    env.set_params(params)
    ams(name='monitor')

  def start(self, env):
    self.configure(env) # for security

    ams_service( 'monitor',
                 action = 'start'
    )

    import params
    Links(params.new_metrics_log_path_monitor, params.metrics_log_path_monitor)

  def stop(self, env):
    import params
    env.set_params(params)

    ams_service( 'monitor',
                 action = 'stop'
    )

  def status(self, env):
    import status_params
    env.set_params(status_params)
    check_service_status(name='monitor')


if __name__ == "__main__":
  AmsMonitor().execute()

