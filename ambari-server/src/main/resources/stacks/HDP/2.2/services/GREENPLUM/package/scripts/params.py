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

gp_install_dir = '/opt/tbds/greenplum-db-4.3.6.2'
gp_install_zip = 'greenplum-db-4.3.6.2.zip'
gp_install_symlink = '/opt/tbds/greenplum-db'
gp_conf_dir = "/etc/tbds/greenplum"

gp_user = config['configurations']['gp-env']['gp_user']
hostname = config['hostname']
user_group = config['configurations']['cluster-env']['user_group']
java64_home = config['hostLevelParams']['java_home']

gp_master_host = default('/clusterHostInfo/gp_master_hosts', ['localhost'])[0]
gp_segment_hosts = default('/clusterHostInfo/gp_segment_hosts', ['localhost'])
gp_master_port = config['configurations']['gp-site']['master.port']
gp_master_data_dir = config['configurations']['gp-site']['master.data.dir']
gp_segment_data_dir = config['configurations']['gp-site']['segment.data.dir']
gp_segment_base_port = config['configurations']['gp-site']['segment.base.port']