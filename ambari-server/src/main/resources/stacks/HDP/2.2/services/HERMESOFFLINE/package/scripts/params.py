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

# hermes worker hosts
hostname = default("hostname", [])
worker_hosts = default("/clusterHostInfo/hermesoffline_worker_hosts", [])

# tube master hosts
master_listen_port = config['configurations']['master-ini']['master.listen.port']
master_hosts = default("/clusterHostInfo/tube_master_hosts", [])
hermes_adapter_pull_masterHost = util.zk_connection_string(master_hosts, master_listen_port)

# zk hosts
zk_hosts = default("/clusterHostInfo/zookeeper_hosts", [])
hermes_zkConnectionString = util.zk_connection_string(zk_hosts, 2181)

# JAVA HOME
java_home = default("/hostLevelParams/java_home", "/usr/jdk64/jdk1.7.0_67")
# hermes port used
hermes_server_port = config['configurations']['hermes-properties']['hermes.server.port']
hermes_worker_port = config['configurations']['hermes-properties']['hermes.worker.port']
debug_jms_port = config['configurations']['hermes-properties']['debug.jms.port']
# hermes JVN setting
hermes_xms = config['configurations']['hermes-properties']['hermes.xms']
hermes_xmx = config['configurations']['hermes-properties']['hermes.xmx']
hermes_xmn = config['configurations']['hermes-properties']['hermes.xmn']

# master-ini.xml
hermes_user = config['configurations']['hermes-properties']['hermes.user']
hermes_group = config['configurations']['hermes-properties']['hermes.group']
hermes_topic = config['configurations']['hermes-properties']['hermes.topic']
higo_userpackage_docIdsLocalBaseDir = config['configurations']['hermes-properties']['higo.userpackage.docIdsLocalBaseDir']
higo_userpackage_pkgBaseLocalDir = config['configurations']['hermes-properties']['higo.userpackage.pkgBaseLocalDir']
higo_userpackage_bitsLocalBaseDir = config['configurations']['hermes-properties']['higo.userpackage.bitsLocalBaseDir']
hermes_store_local_dir = config['configurations']['hermes-properties']['hermes.store.local.dir']
hermes_store_download_port = config['configurations']['hermes-properties']['hermes.store.download.port']
hermes_store_upload_port = config['configurations']['hermes-properties']['hermes.store.upload.port']
hermes_local_conf_dir = config['configurations']['hermes-properties']['hermes.local.conf.dir']
hermes_conf_dir = config['configurations']['hermes-properties']['hermes.conf.dir']
hermes_hadoop_conf_dir = config['configurations']['hermes-properties']['hermes.hadoop.conf.dir']
hermes_hadoop_home = config['configurations']['hermes-properties']['hermes.hadoop.home']
hermes_mode = config['configurations']['hermes-properties']['hermes.mode']
hermes_schema_mode = config['configurations']['hermes-properties']['hermes.schema.mode']
hermes_worker_tasklist_assign_type = config['configurations']['hermes-properties']['hermes.worker.tasklist.assign.type']
hermes_index_path = config['configurations']['hermes-properties']['hermes.index.path']
hermes_schema_path = config['configurations']['hermes-properties']['hermes.schema.path']

# zk.root
zk_root = config['configurations']['hermes-properties']['zk.root']
log4j_properties = config['configurations']['offline-log4j-properties']['content']

# hermes-adapter-properties.xml
hermes_adapter_impl_class_pull = config['configurations']['hermes-adapter-properties']['hermes.adapter.impl.class.pull']
hermes_adapter_tid = config['configurations']['hermes-adapter-properties']['hermes.adapter.tid']
hermes_adapter_push_tdManagerIp = config['configurations']['hermes-adapter-properties']['hermes.adapter.push.tdManagerIp']
hermes_adapter_push_cluster_id = config['configurations']['hermes-adapter-properties']['hermes.adapter.push.cluster_id']
hermes_adapter_push_net_tag = config['configurations']['hermes-adapter-properties']['hermes.adapter.push.net_tag']
hermes_adapter_push_business_id = config['configurations']['hermes-adapter-properties']['hermes.adapter.push.business_id']
hermes_adapter_push_dt = config['configurations']['hermes-adapter-properties']['hermes.adapter.push.dt']
hermes_adapter_push_timeout = config['configurations']['hermes-adapter-properties']['hermes.adapter.push.timeout']
hermes_adapter_pull_setMaxoffset = config['configurations']['hermes-adapter-properties']['hermes.adapter.pull.setMaxoffset']
hermes_adapter_pull_queueMaxsize = config['configurations']['hermes-adapter-properties']['hermes.adapter.pull.queueMaxsize']
hermes_adapter_pull_speed = config['configurations']['hermes-adapter-properties']['hermes.adapter.pull.speed']
hermes_adapter_pull_topic = config['configurations']['hermes-adapter-properties']['hermes.adapter.pull.topic']
hermes_adapter_pull_group = config['configurations']['hermes-adapter-properties']['hermes.adapter.pull.group']

# refractor service path
hermes_install_path = "/usr/hdp/2.2.0.0-2041/hermes"
new_hermes_install_path = "/opt/tbds/hermes"

# scripts
start_service_script = "/opt/tbds/hermes/start_service.sh"
start_manager_script = "bin/start_manager.sh"
start_hermes_server_script = "bin/start_hermesserver.sh"
start_package_server_script = "bin/start_hermesuserpackageserver.sh"
start_store_server_script = "bin/start_hermesstoreserver.sh"
start_worker_script = "bin/start_worker.sh"






