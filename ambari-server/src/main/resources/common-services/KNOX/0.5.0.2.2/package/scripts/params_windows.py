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
import os

# server configurations
config = Script.get_config()

hdp_root = os.path.abspath(os.path.join(os.environ["HADOOP_HOME"],".."))
knox_home = os.environ['KNOX_HOME']
knox_conf_dir = os.environ['KNOX_CONF_DIR']
knox_logs_dir = os.environ['KNOX_LOG_DIR']
knox_bin = os.path.join(knox_home, 'bin', 'gateway.exe')
ldap_bin = os.path.join(knox_home, 'bin', 'ldap.exe')
knox_client_bin = os.path.join(knox_home, 'bin', 'knoxcli.cmd')
knox_data_dir = os.path.join(knox_home, 'data')

knox_master_secret_path = os.path.join(knox_data_dir, 'security', 'master')
knox_cert_store_path = os.path.join(knox_data_dir, 'security', 'keystores', 'gateway.jks')

knox_user = 'hadoop'
hdfs_user = "hadoop"
knox_group = None
mode = None
