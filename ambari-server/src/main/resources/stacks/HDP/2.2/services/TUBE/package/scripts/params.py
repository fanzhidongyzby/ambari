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

# zk hosts
zk_hosts = default("/clusterHostInfo/zookeeper_hosts", [])
zk_connection = util.zk_connection_string(zk_hosts, 2181)

host_name = default("hostname", [])

# JAVA HOME
java_home = default("/hostLevelParams/java_home", "/usr/jdk64/jdk1.7.0_67")

# master-ini.xml
tube_user = config['configurations']['master-ini']['tube.user']
tube_group = config['configurations']['master-ini']['tube.group']
zk_root = config['configurations']['master-ini']['zk.root']
master_listen_port = config['configurations']['master-ini']['master.listen.port']
master_web_port = config['configurations']['master-ini']['master.web.port']
consumer_balance_period = config['configurations']['master-ini']['consumer.balance.period']
first_balance_delay_after_start = config['configurations']['master-ini']['first.balance.delay.after.start']
consumer_heartbeat_timeout = config['configurations']['master-ini']['consumer.heartbeat.timeout']
producer_heartbeat_timeout = config['configurations']['master-ini']['producer.heartbeat.timeout']
broker_heartbeat_timeout = config['configurations']['master-ini']['broker.heartbeat.timeout']

# topic tool
topic_port = config['configurations']['master-ini']['topic.tool.port']
topic_client_timeval = config['configurations']['master-ini']['topic.tool.timeval']

# master hosts
master_hosts = default("/clusterHostInfo/tube_master_hosts", [])
master_address_list = util.zk_connection_string(master_hosts, master_listen_port)

topic_tool_server_hosts = default("/clusterHostInfo/topic_tool_server_hosts", [])[0]

# broker-ini.xml
broker_listen_port = config['configurations']['broker-ini']['broker.listen.port']
num_partitions = config['configurations']['broker-ini']['num.partitions']
unflush_threshold = config['configurations']['broker-ini']['unflush.threshold']
unflush_interval = config['configurations']['broker-ini']['unflush.interval']
max_segment_size = config['configurations']['broker-ini']['max.segment.size']
transfer_size = config['configurations']['broker-ini']['transfer.size']
delete_policy = config['configurations']['broker-ini']['delete.policy']
delete_when = config['configurations']['broker-ini']['delete.when']
data_path = config['configurations']['broker-ini']['data.path']
load_message_stores_in_parallel = "true" if config['configurations']['broker-ini']['load.message.stores.in.parallel'] else "false"

# refractor service path
tube_install_path = "/usr/hdp/2.2.0.0-2041/tube"
new_tube_install_path = "/opt/tbds/tube"

# scripts
master_script = new_tube_install_path + "/bin/master.sh"
broker_script = new_tube_install_path + "/bin/broker.sh"
topic_tool_server = new_tube_install_path + "/bin/topic_tool.py"
topic_tool_client = new_tube_install_path + "/bin/start_tool_client.py"
start_tool_server = new_tube_install_path + "/bin/start_tool_server.sh"






