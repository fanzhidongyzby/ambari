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

import sys
import os
from resource_management import *
from resource_management.core.logger import Logger
from utils import utils


class configinit(Script):
  def update_common(self, env):
    import params

    Logger.info('update yarn-site.xml')
    File(os.path.join(params.yarn_config_path, 'yarn-site.xml'),
         owner=params.user,
         group=params.group,
         mode=0644,
         content=Template("yarn-site.xml.j2")
         )

    Logger.info('update hdfs-site.xml')
    File(os.path.join(params.yarn_config_path, 'hdfs-site.xml'),
         owner=params.user,
         group=params.group,
         mode=0644,
         content=Template("hdfs-site.xml.j2")
         )

    Logger.info('update core-site.xml')
    File(os.path.join(params.yarn_config_path, 'core-site.xml'),
         owner=params.user,
         group=params.group,
         mode=0644,
         content=Template("core-site.xml.j2")
         )

    Logger.info("generate nodes_to_decommission file")
    File(os.path.join(params.yarn_config_path, 'nodes_to_decommission'),
         owner=params.user,
         group=params.group,
         mode=0644,
         content=Template("nodes_to_decommission.j2")
         )

  def update_rmhaproxy_configs(self, env):
    import params

    Logger.info('configure Haproxy on ResourceManager')

    File(os.path.join(params.rmhaproxy_install_path, 'haproxy.cfg'),
         owner=params.user,
         group=params.group,
         mode=0644,
         content=Template("haproxy.cfg.j2")
         )

  def update_apiserver_configs(self, env):
    import params

    Logger.info("update apiserver.properties")
    File(os.path.join(params.apiserver_config_path, 'apiserver.properties'),
         owner=params.user,
         group=params.group,
         mode=0644,
         content=Template("apiserver.properties.j2")
         )

    Logger.info("update application.properties")

    File(os.path.join(params.apiserver_config_path, 'application.properties'),
         owner=params.user,
         group=params.group,
         mode=0644,
         content=Template("application.properties.j2")
         )

  def update_rm_configs(self, env):
    import params

    Logger.info('configure ResourceManager')

    self.update_common(env)

    Logger.info("generate sfair-scheduler.xml on ResourceManager")
    File(os.path.join(params.yarn_config_path, 'sfair-scheduler.xml'),
         owner=params.user,
         group=params.group,
         mode=0644,
         content=Template("sfair-scheduler.xml.j2")
         )

  def update_nm_configs(self, env):
    import params

    Logger.info('configure NodeManager')

    self.update_common(env)

    Logger.info("generate container-executor.cfg on ResourceManager")
    File(os.path.join(params.yarn_config_path, 'container-executor.cfg'),
         owner=params.user,
         group=params.group,
         mode=0644,
         content=Template("container-executor.cfg.j2")
         )

    Logger.info("generate hadoop tmp directory")
    Directory(params.hadoop_tmp_dir,
              owner=params.user,
              group=params.group,
              mode=0755,
              recursive=True
              )

    Logger.info("generate gaia recovery directory")
    Directory(params.gaia_nodemanager_recovery_dir,
              owner=params.user,
              group=params.group,
              mode=0755,
              recursive=True
              )

    Logger.info("generate nodemanager local dirs")
    for dir in params.yarn_nm_local_dirs_fullpath.split(","):
      Directory(dir,
                owner=params.user,
                group=params.group,
                mode=0755,
                recursive=True
                )


if __name__ == "__main__":
  configinit().execute()
