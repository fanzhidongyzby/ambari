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

goldeneye_web_pid_file = '/usr/local/goldeneye/goldeneye-web/web.pid'

#scripts
config_web_script = format("{tmp_dir}/configWeb.sh")
gri_ge_script = format("{tmp_dir}/gri_ge.sql")
gri_monitor_script = format("{tmp_dir}/gri_monitor.sql")
start_mysql_script = format("{tmp_dir}/startMySql.sh")


#golden eye web
goldeneye_web_host = default("/clusterHostInfo/goldeneye_web_hosts", ["localhost"])[0]
goldeneye_web_listen_port = default("/configurations/goldeneye-web/listen.port", 80)
goldeneye_web_url = "http://" + goldeneye_web_host + ":" + str(goldeneye_web_listen_port) + "/ge/"
web_config_path = '/usr/local/goldeneye/goldeneye-web/config'
service_daemon = 'httpd'
goldeneye_web_root_path = '/usr/local/goldeneye/goldeneye-web'
web_http_path = '/etc/httpd/conf.d'
#golden eye db
goldeneye_database_host = default("/clusterHostInfo/goldeneye_metadata_database_hosts", ["localhost"])[0]

goldeneye_data_dir = default("/configurations/goldeneye-database/goldeneye.data.dir", "/data/goldeneye/mysql_data")
goldeneye_database_port = default("/configurations/goldeneye-database/database.port", 3306)
goldeneye_database_username = default("/configurations/goldeneye-database/goldeneye.username", "root")
goldeneye_database_password = default("/configurations/goldeneye-database/goldeneye.password", "")

# Lhotse metadata database used config settings
if System.get_instance().os_family == "suse" or System.get_instance().os_family == "ubuntu":
  daemon_name = 'mysql'
else:
  daemon_name = 'mysqld'

# refractor service path

goldeneye_install_path = "/usr/local/goldeneye"

goldeneye_conf_path_web = "/etc/httpd/conf.d/ge.conf"
goldeneye_conf_path_metadb = "/etc/my.cnf"

goldeneye_log_path_web = "/usr/local/goldeneye/goldeneye-web/logs"
goldeneye_log_path_metadb = "/var/log/mysqld.log"

goldeneye_data_path_metadb = "/data/goldeneye/mysql_data"


new_goldeneye_install_path = "/opt/tbds/goldeneye"

new_goldeneye_conf_path_web = "/etc/tbds/goldeneye/web/httpd/ge.conf"
new_goldeneye_conf_path_metadb = "/etc/tbds/goldeneye/metadb/my.cnf"

new_goldeneye_log_path_web = "/var/log/tbds/goldeneye/web"
new_goldeneye_log_path_metadb = "/var/log/tbds/goldeneye/metadb/mysqld.log"

new_goldeneye_data_path_metadb = "/data/tbds/goldeneye/metadb"