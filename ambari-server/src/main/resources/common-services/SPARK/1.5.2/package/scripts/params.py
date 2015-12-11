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
fs_default_fs = config['configurations']['core-site']['fs.defaultFS']
hadoop_conf_dir = "/etc/hadoop/conf"
hive_site_file = "/etc/hive/conf/hive-site.xml"
tez_conf_dir = "/etc/tez/conf"
tez_site_file = tez_conf_dir + "/tez-site.xml"

# spark common
hdfs_user = "hdfs"
user_group = "hadoop"
spark_user = hdfs_user
spark_home = "/usr/hdp/2.2.0.0-2041/spark"
spark_submit_cmd = spark_home + "/bin/spark-submit"
spark_conf_dir = spark_home + "/conf"
spark_defaults_conf_file = spark_home + "/conf/spark-defaults.conf"
spark_log_home = "/data/log/tbds/spark"
spark_env_file = spark_conf_dir + "/spark-env.sh"

# spark history server
spark_history_ui_port = config['configurations']['spark-defaults']['spark.history.ui.port']
spark_eventLog_dir = spark_log_home + "/eventlog"
spark_history_fs_logDirectory =  spark_log_home +"/history"

spark_history_server_home = "/opt/tbds/spark-historyserver"
history_start_script = spark_home + "/sbin/start-history-server.sh"
history_stop_script = spark_home + "/sbin/stop-history-server.sh"

# spark jdbc server
spark_jdbc_server_host = default("/clusterHostInfo/spark_jdbc_server_hosts", ["localhost"])[0]
spark_jdbc_server_port = config['configurations']['spark-defaults']['spark.hive.server2.thrift.port']
spark_jdbc_server_home = "/opt/tbds/spark-jdbc-server"
jdbc_start_script = spark_home + "/sbin/start-thriftserver.sh --master yarn --driver-java-options -Dhdp.version=2.2.0.0-2041" + " --hiveconf hive.server2.thrift.bind.host=" + spark_jdbc_server_host + " --hiveconf hive.server2.thrift.port=" + str(spark_jdbc_server_port)
jdbc_stop_script = spark_home + "/sbin/stop-thriftserver.sh"

# spark client
spark_client_home = "/opt/tbds/spark-client"

# livy server
livy_server_host = default("/clusterHostInfo/spark_livy_server_hosts", ["localhost"])[0]
livy_server_port = config['configurations']['livy-defaults']['livy.server.port']
livy_server_home = "/usr/hdp/2.2.0.0-2041/livy"
livy_server_link_home = "/opt/tbds/spark-livy"
livy_conf_path = livy_server_home + "/conf/livy-defaults.conf"
livy_env_path = livy_server_home + "/bin/livy-server-env.sh"
livy_server_start_script = livy_server_home + "/bin/livy-server"
livy_jar_path = fs_default_fs + "/user/spark/share/lib"
livy_jar_file = livy_jar_path + "/livy-assembly-3.9.0-SNAPSHOT.jar"
livy_local_jar_file = livy_server_home + "/livy-assembly/target/scala-2.10/livy-assembly-3.9.0-SNAPSHOT.jar"

