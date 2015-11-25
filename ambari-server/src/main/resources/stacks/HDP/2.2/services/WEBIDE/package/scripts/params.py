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

java_home = config['hostLevelParams']['java_home']

webide_user = config['configurations']['webide']['webide.user']
webide_group = config['configurations']['webide']['webide.group']

#webide web info
webide_host = default("/clusterHostInfo/web_ide_web_hosts", ["localhost"])[0]
webide_web_listen_port = config['configurations']['webide']['web.listen.port']

webide_web_url = "http://" + webide_host + ":" + str(webide_web_listen_port) + "/tod_ide"

#webide web path
webide_install_path = "/usr/hdp/2.2.0.0-2041/webide"
new_webide_install_path = "/opt/tbds/webide"

webide_log_path = "/etc/http/logs"
new_webide_log_path = "/var/log/tbds/webide"

config_web_script = webide_install_path + "/configWeb.sh"
webide_conf_path = "/etc/httpd/conf.d/webide.conf"
webide_rest_uri_file_path = webide_install_path + "/tod_ide/config/setting.php"

#webide app
webide_app_host = default("/clusterHostInfo/web_ide_app_hosts", ["localhost"])[0]
webide_app_listen_port = config['configurations']['webide']['app.listen.port']

pg_host = default("/clusterHostInfo/postgresql_server_hosts", ["localhost"])[0]
pg_port = default("/configurations/postgresql-postgre-env/postgresql.postgre.port", 5432)

thive_host = default("/clusterHostInfo/thive_server_hosts", ["localhost"])[0]
thive_port = default("/configurations/thive-config-env/thive.server.port", 10002)

rest_uri = "http://" + webide_app_host + ":" + str(webide_app_listen_port)

#webide app path
webide_app_path = webide_install_path + "/webide-app"
webide_app_server_path = webide_app_path + "/conf/server.xml"
webide_app_properties_path = webide_app_path + "/conf/webide_conf.properties"
webide_app_start_script = webide_app_path + "/bin/startup.sh"
webide_app_stop_script = webide_app_path + "/bin/shutdown.sh"

http_conf_path = "/etc/httpd/conf/httpd.conf"
webide_app_sql_path = webide_app_path + "/app.sql"
postgresql_install_path = "/usr/pgsql-9.3"
webide_db_exist_cmd = format("{postgresql_install_path}/bin/psql -U postgres -h {pg_host} -p {pg_port}") + " -c '\l' | awk '{print $1}' | grep webide"
