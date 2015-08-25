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

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

#thive config
fs_default_name = default("/configurations/thive-config-env/fs.default.name", "hdfs://0.0.0:8020/")
analysisbuffer_tmp_addr  = default("/configurations/thive-config-env/analysisbuffer.tmp.addr","/tmp/thive/temp")
hive_rctmpfile_path = default("/configurations/thive-config-env/hive.rctmpfile.path","/tmp/thive/tdw_rctmp")
hive_multi_rctmpfile_path_number =  default("/configurations/thive-config-env/hive.multi.rctmpfile.path.number",5)
hive_multi_rctmpfile_path = default("/configurations/thive-config-env/hive.multi.rctmpfile.path","/data1/tdw_rctmp/,/data2/tdw_rctmp/,/data3/tdw_rctmp/,/data4/tdw_rctmp/,/data5/tdw_rctmp/")
thive_log4j = default("/configurations/thive-config-env/content","")
hive_plc_user = default("/configurations/thive-config-env/hive.plc.user","thive")
hive_plc_password = default("/configurations/thive-config-env/hive.plc.password","thive")
thive_port = default("/configurations/thive-config-env/thive.server.port",10002)

hive_process_keyword = 'hive_service.jar'

thive_config_path = "/usr/local/thive/dist/conf"


#pg config
pg_server_hosts = default("/clusterHostInfo/thive_metadata_database_hosts", ["127.0.0.1"])[0]
pg_server_hosts_hba = default("/clusterHostInfo/thive_metadata_database_hosts", ["127.0.0.1"])[0]
pg_server_port = '5432'
pg_server_user = default("/configurations/pg-config-env/pg.user","pgmeta")
pg_server_password = default("/configurations/pg-config-env/pg.password","pgmeta")

pg_authorized_ip = default("/configurations/pg-hba-env/content","host    all             all             0.0.0.0/0         trust")

pg_postgresql_conf = default("/configurations/pg-config-env/content","")

pg_config_path = "/var/lib/pgsql/9.3/data/"

pg_process_keyword = 'postmaster'


initpg_script = format("{tmp_dir}/initpg.sh")
clean_doc_script = format("{tmp_dir}/clean_doc.sh")
reset_meta_script = format("{tmp_dir}/reset_meta.sql")
tdw_meta_global_db_script = format("{tmp_dir}/tdw_meta_global_db.sql")

tdw_meta_init_script = format("{tmp_dir}/tdw_meta_init.sql")
tdw_meta_pbjar_db_script = format("{tmp_dir}/tdw_meta_pbjar_db.sql")

tdw_meta_query_info_db_script = format("{tmp_dir}/tdw_meta_query_info_db.sql")
tdw_meta_segment_db_script = format("{tmp_dir}/tdw_meta_segment_db.sql")

checkstatus_script = format("{tmp_dir}/thive_check_status.sh")


# refractor service path

thive_install_path = "/usr/local/thive"

thive_conf_path_server = "/usr/local/thive/dist/conf"
thive_conf_path_pgsql = "/var/lib/pgsql/9.3/data"

thive_log_path_server = "/usr/local/thive/log"
thive_log_path_pgsql = "/var/lib/pgsql/9.3/data/pg_log"

thive_data_path_pgsql = "/var/lib/pgsql/9.3/data"


new_thive_install_path = "/opt/tbds/thive"

new_thive_conf_path_server = "/etc/tbds/thive/server"
new_thive_conf_path_pgsql = "/etc/tbds/thive/metadb"

new_thive_log_path_server = "/var/log/tbds/thive/server"
new_thive_log_path_pgsql = "/var/log/tbds/thive/metadb"

new_thive_data_path_pgsql = "/data/tbds/thive/metadb"
