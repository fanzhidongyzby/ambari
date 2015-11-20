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
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management.libraries.functions.default import default
from resource_management.core.logger import Logger

import status_params

# server configurations
config = Script.get_config()

stack_name = default("/hostLevelParams/stack_name", None)

version = default("/commandParams/version", None)

stack_version_unformatted = str(config['hostLevelParams']['stack_version'])
hdp_stack_version = format_hdp_stack_version(stack_version_unformatted)

hue_install_dir = '/opt/tbds/hue'
hue_install_tar = 'hue-3.9.0-bin.tgz'
hue_bin = '/opt/tbds/hue/build/env/bin/supervisor'
hue_conf_dir = "/opt/tbds/hue/desktop/conf"
hue_log_dir = "/opt/tbds/hue/logs"
hue_pid_file = "/opt/tbds/hue/hue.pid"

new_hue_config_path = "/etc/tbds/hue"
new_hue_data_path = "/data/tbds/hue"
new_hue_log_path = "/var/log/tbds/hue"

hue_user = config['configurations']['hue-env']['hue_user']
hostname = config['hostname']
user_group = config['configurations']['cluster-env']['user_group']
java64_home = config['hostLevelParams']['java_home']
http_port = config['configurations']['hue-site']['http.port']

#hadoop services' addresses
namenode_http_address = config['configurations']['hdfs-site']['dfs.namenode.http-address']
fs_defaultFS = config['configurations']['core-site']['fs.defaultFS']
hive_host = config['clusterHostInfo']['hive_server_host'][0]
hive_port = default('/configurations/hive-site/hive.server2.thrift.port',"10000")
yarn_rm_url = default('/configurations/yarn-site/yarn.resourcemanager.webapp.address', "http://localhost:8088")
livy_server_host = config['clusterHostInfo']['spark_livy_server_hosts'][0]
livy_server_port = default('/configurations/livy-defaults/livy.server.port',"8998")

zookeeper_host = default('/clusterHostInfo/zookeeper_hosts', ['localhost'])
zk_address = zookeeper_host[0] + ":" + default('/configurations/zoo-cfg/clientPort', "2181")

# Security-related params
security_enabled = config['configurations']['cluster-env']['security_enabled']