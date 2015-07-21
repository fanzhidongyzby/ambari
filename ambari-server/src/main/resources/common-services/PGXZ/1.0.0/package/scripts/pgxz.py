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
import sys
import os
from resource_management.core.logger import Logger
class pgxz:
  
  def init_coor(self):
    import params
    Logger.info("create coor pg_hba.conf")
    File(os.path.join(params.coordinator_path,'pg_hba.conf'),
      owner='root',
      group='root',
      mode=0644,
      content=Template("coor_pghba.j2")
    )

    Logger.info("create coor postgresql.conf")
    File(os.path.join(params.coordinator_path,'postgresql.conf'),
      owner='root',
      group='root',
      mode=0644,
      content=Template("coor_postgresql.j2")
    )


  def init_datanode(self):
    import params
    Logger.info("create datanode pg_hba.conf")
    File(os.path.join(params.datanode_path,'pg_hba.conf'),
      owner='root',
      group='root',
      mode=0644,
      content=Template("datanode_pghba.j2")
    )

    Logger.info("create datanode postgresql.conf")
    File(os.path.join(params.datanode_path,'postgresql.conf'),
      owner='root',
      group='root',
      mode=0644,
      content=Template("datanode_postgresql.j2")
    )


  def init_gtm(self):
    import params
    Logger.info("create gtm.conf")
    File(os.path.join(params.gtm_path,'gtm.conf'),
      owner='root',
      group='root',
      mode=0644,
      content=Template("gtm_conf.j2")
    )

