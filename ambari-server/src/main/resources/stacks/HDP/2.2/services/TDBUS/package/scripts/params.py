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
from resource_management.libraries.script import Script
from resource_management.libraries.functions.default import default
import util

# server configurations
config = Script.get_config()

# JAVA HOME
java_home = default("/hostLevelParams/java_home", "/usr/jdk64/jdk1.7.0_67")

# tdbus JVN setting
tdbus_xms = config['configurations']['tdbus-properties']['tdbus.xms']
tdbus_xmx = config['configurations']['tdbus-properties']['tdbus.xmx']
tdbus_xmn = config['configurations']['tdbus-properties']['tdbus.xmn']

# master-ini.xml
tdbus_user = config['configurations']['tdbus-properties']['tdbus.user']
tdbus_group = config['configurations']['tdbus-properties']['tdbus.group']
master_listen_port = config['configurations']['master-ini']['master.listen.port']

# tube master hosts
master_hosts = default("/clusterHostInfo/tube_master_hosts", [])
tube_master_address_list = util.zk_connection_string(master_hosts, master_listen_port)

topic_tool_server_hosts = default("/clusterHostInfo/topic_tool_server_hosts", [])[0]


# refractor service path
tdbus_install_path = "/usr/hdp/2.2.0.0-2041/tdbus"
new_tdbus_install_path = "/opt/tbds/tdbus"

# scripts
start_script = new_tdbus_install_path + "/bin/start_tdbus.sh"
stop_script = new_tdbus_install_path + "/bin/stop.sh"

# topic client
tube_topic_tool_client = new_tdbus_install_path + "/bin/tube_topic_tool_client.py"
tube_topic_client_timeval = config['configurations']['master-ini']['topic.tool.timeval']
tube_topic_port = config['configurations']['master-ini']['topic.tool.port']






