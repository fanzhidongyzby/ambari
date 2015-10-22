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
worker_hosts = default("/clusterHostInfo/hermesonline_worker_hosts", [])


# zk hosts
zk_hosts = default("/clusterHostInfo/zookeeper_hosts", [])
hermes_zkConnectionString = util.zk_connection_string(zk_hosts, 2181)

# JAVA HOME
java_home = default("/hostLevelParams/java_home", "/usr/jdk64/jdk1.7.0_67")
# hermes port used
hermes_server_port = config['configurations']['online-hermes-properties']['hermes.server.port']
hermes_worker_port = config['configurations']['online-hermes-properties']['hermes.worker.port']
debug_jms_port = config['configurations']['online-hermes-properties']['debug.jms.port']
# hermes JVN setting
hermes_xms = config['configurations']['online-hermes-properties']['hermes.xms']
hermes_xmx = config['configurations']['online-hermes-properties']['hermes.xmx']
hermes_xmn = config['configurations']['online-hermes-properties']['hermes.xmn']

# master-ini.xml
hermes_user = config['configurations']['online-hermes-properties']['hermes.user']
hermes_group = config['configurations']['online-hermes-properties']['hermes.group']
hermes_topic = config['configurations']['online-hermes-properties']['hermes.topic']
higo_userpackage_docIdsLocalBaseDir = config['configurations']['online-hermes-properties']['higo.userpackage.docIdsLocalBaseDir']
higo_userpackage_pkgBaseLocalDir = config['configurations']['online-hermes-properties']['higo.userpackage.pkgBaseLocalDir']
higo_userpackage_bitsLocalBaseDir = config['configurations']['online-hermes-properties']['higo.userpackage.bitsLocalBaseDir']
hermes_store_local_dir = config['configurations']['online-hermes-properties']['hermes.store.local.dir']
hermes_store_download_port = config['configurations']['online-hermes-properties']['hermes.store.download.port']
hermes_store_upload_port = config['configurations']['online-hermes-properties']['hermes.store.upload.port']
hermes_local_conf_dir = config['configurations']['online-hermes-properties']['hermes.local.conf.dir']
hermes_conf_dir = config['configurations']['online-hermes-properties']['hermes.conf.dir']
hermes_hadoop_conf_dir = config['configurations']['online-hermes-properties']['hermes.hadoop.conf.dir']
hermes_hadoop_home = config['configurations']['online-hermes-properties']['hermes.hadoop.home']
hermes_mode = config['configurations']['online-hermes-properties']['hermes.mode']
hermes_schema_mode = config['configurations']['online-hermes-properties']['hermes.schema.mode']
hermes_worker_tasklist_assign_type = config['configurations']['online-hermes-properties']['hermes.worker.tasklist.assign.type']
hermes_index_path = config['configurations']['online-hermes-properties']['hermes.index.path']
hermes_schema_path = config['configurations']['online-hermes-properties']['hermes.schema.path']

# zk.root
zk_root = config['configurations']['online-hermes-properties']['zk.root']

# online-log4j-properties.xml
log4j_properties = config['configurations']['online-log4j-properties']['content']

# refractor service path
hermes_install_path = "/usr/hdp/2.2.0.0-2041/hermes"
new_hermes_install_path = "/data/tbds/hermes"

# scripts
start_service_script = "/data/tbds/hermes/start_service.sh"
start_manager_script = "bin/start_manager.sh"
start_hermes_server_script = "bin/start_hermesserver.sh"
start_dispatcher_script = "bin/start_dispatcher.sh"
start_worker_script = "bin/start_worker.sh"






