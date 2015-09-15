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

from resource_management.libraries.functions.default import default
from resource_management import *
from utils import utils
import socket

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

#dse
dse_server_home = "/data/tbds/dse/DSE-service"

kafka_properties_path = "/data/tbds/dse/DSE-service/ambariConfig/"
db_properties_path = "/data/tbds/dse/DSE-service/ambariConfig/"
server_conf_path = "/data/tbds/dse/DSE-service/conf/"


dse_server_host = default("/clusterHostInfo/dse_server_hosts", ["127.0.0.1"])[0]
dse_server_local_host = socket.gethostbyname(socket.gethostname())
dse_server_port = default('/configurations/dse-env/dse.server.port', 54301)
dse_server_jmx_port = default('/configurations/dse-env/dse.server.jmx.port', 10007)

java_home = default('/hostLevelParams/hostLevelParams', "/usr/jdk64/jdk1.7.0_67")
dse_bin_dir = "{0}/bin".format(dse_server_home)

dse_start_command = "sudo /data/tbds/dse/DSE-service/bin/start.sh {0}".format(dse_server_jmx_port)
dse_stop_command = "sudo /data/tbds/dse/DSE-service/bin/kill.sh {0}".format(dse_server_jmx_port)
dse_keyword = "com.qq.taserver.startup.Main"



#mysql
dbinit_script = format("{tmp_dir}/dbInit.sql")
startmysql_script = format("{tmp_dir}/startMySql.sh")
mysql_host = default("/clusterHostInfo/dse_database_hosts", ["127.0.0.1"])[0]
mysql_port = default('/configurations/db-properties/dse.mysql.port', 3306)
mysql_user = default('/configurations/db-properties/dse.mysql.user', 'ambari') 
mysql_password = default('/configurations/db-properties/dse.mysql.password', 123456)
mysql_data_dir = default('/configurations/db-properties/mysql.data.dir', '/data/mysql_data')
mysql_service = "mysqld"
mysql_keyword = "pid"

mysql_init_command = "sudo bash -x {0} {1} {2} {3} {4} {5}".format(startmysql_script,mysql_host,mysql_data_dir,mysql_user,mysql_password,mysql_port)

#kafka
kafka_hosts = default("/clusterHostInfo/kafka_broker_hosts", ["127.0.0.1"])
kafka_port = default('/configurations/kafka-broker/port', 6667)
kafka_host_port = utils().bind_hosts_port(kafka_hosts,kafka_port,',','')


# refractor service path

dse_config_path = "/data/tbds/dse/DSE-service/conf"
dse_log_path = "/data/tbds/dse/DSE-service/log"

new_dse_config_path = "/etc/tbds/dse"
new_dse_log_path = "/var/log/tbds/dse"
