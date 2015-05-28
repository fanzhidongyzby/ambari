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
import os

def hdfs(component=None):
  import params
  if component == "namenode":
    directories = params.dfs_name_dir.split(",")
    Directory(directories,
              owner=params.hdfs_user,
              mode="(OI)(CI)F",
              recursive=True
    )
    File(params.exclude_file_path,
         content=Template("exclude_hosts_list.j2"),
         owner=params.hdfs_user,
         mode="f",
    )
  if "hadoop-policy" in params.config['configurations']:
    XmlConfig("hadoop-policy.xml",
              conf_dir=params.hadoop_conf_dir,
              configurations=params.config['configurations']['hadoop-policy'],
              owner=params.hdfs_user,
              mode="f",
              configuration_attributes=params.config['configuration_attributes']['hadoop-policy']
    )

  XmlConfig("hdfs-site.xml",
            conf_dir=params.hadoop_conf_dir,
            configurations=params.config['configurations']['hdfs-site'],
            owner=params.hdfs_user,
            mode="f",
            configuration_attributes=params.config['configuration_attributes']['hdfs-site']
  )
