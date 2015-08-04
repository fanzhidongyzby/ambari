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
import string
from resource_management.libraries.functions.default import default
from resource_management import *
from gaiautils import gaiautils

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

# ENV
user = "gaia"
group = "users"
java_home = default("/hostLevelParams/java_home", "/usr/jdk64/jdk1.8.0_51")


# HDFS

hadoop_home = default("/configurations/gaia-hdfs-site/hadoop.home", "/gaia/hadoop")
hadoop_tmp_dir = default("/configurations/gaia-hdfs-site/hadoop.tmpdir", "/gaia/hadoop/hdfsadmin/hdfsenv/runtime")
# datanode_data_subdir = default("/configurations/gaia-hdfs-site/datanode.data.subdir", "/hadoop")
# datanode_data_dirs = gaiautils().get_local_dirs(datanode_data_subdir)
datanode_data_dirs = default("/configurations/gaia-hdfs-site/datanode.data.dirs", "data/hadoop")
namenode_edits_dir = default("/configurations/gaia-hdfs-site/namenode.edits.dir", "/data/editlog")
journalnode_edits_dir = default("/configurations/gaia-hdfs-site/journalnode.edits.dir", "/gaia/hadoop/hdfsadmin/hdfsenv/runtime/dfsnamespace/journal")

namenode_host = default("/configurations/gaia-hdfs-site/namenode.host", "127.0.0.1")
namenode_rpc_port = default("/configurations/gaia-hdfs-site/namenode.rpc.port", "9000")
namenode_http_port = default("/configurations/gaia-hdfs-site/namenode.http.port", "8080")

snamenode_host = default("/configurations/gaia-hdfs-site/snamenode.host", "127.0.0.1")
snamenode_rpc_port = default("/configurations/gaia-hdfs-site/snamenode.rpc.port", "9000")
snamenode_http_port = default("/configurations/gaia-hdfs-site/snamenode.http.port", "8080")


journalnode_hosts = default("/configurations/gaia-hdfs-site/journalnode.hosts", "127.0.0.1")
journalnode_rpc_port = default("/configurations/gaia-hdfs-site/journalnode.rpc.port", "8485")
journalnode_http_port = default("/configurations/gaia-hdfs-site/journalnode.http.port", "8087")
journalnode_address = gaiautils().bind_hosts_port(journalnode_hosts.split(","), journalnode_rpc_port, ";")

# CHECK

env_script = format("{tmp_dir}/env.sh")
supports_script = format("{tmp_dir}/supports.sh")
certification_script = format("{tmp_dir}/certification.sh")

master = "master"
slave = "slave"

# ZooKeeper
zk_server_port = default("/configurations/zoo.cfg/client.port",2181)
zk_hosts = default("/clusterHostInfo/zookeeper_hosts", ["127.0.0.1"])
inner_zk_urls = gaiautils().bind_hosts_port(zk_hosts, zk_server_port, ",")
zk_urls = default("/configurations/gaia-yarn-site/gaia.resourcemanager.zk-address", inner_zk_urls)


# ETCD
etcd_server_port = default("/configurations/etcd/etcd.server.port",4001)
etcd_hosts = default("/clusterHostInfo/etcd_service_hosts", ["127.0.0.1"])
inner_etcd_urls = gaiautils().bind_hosts_port(etcd_hosts, etcd_server_port, ",")
etcd_urls = default("/configurations/gaia-yarn-site/gaia.etcd-address", inner_etcd_urls)


# utils
gaia_script = "cd /gaia/hadoop && su gaia -c '{}'"

yarn_config_path = "/gaia/hadoop/etc/hadoop"
yarn_script = gaia_script.format("env JAVA_HOME={} /gaia/hadoop/sbin/yarn-daemon.sh {} {}".format(java_home, "{}", "{}"))
yarn_start = yarn_script.format("start", "{}")
yarn_stop = yarn_script.format("stop", "{}")

service_script = "{}".format("service {} {}")
service_start = service_script.format("{}", "start")
service_stop = service_script.format("{}", "stop")
service_status = service_script.format("{}", "status")

# strip blank line ahead in file, or cause RM start failed
sfair_schedule_content = default("/configurations/sfair-scheduler-env/content", "").strip()

# yarn-site.xml
yarn_cluster_id = default("/configurations/gaia-yarn-site/gaia.resourcemanager.cluster-id", "gaia-test")
yarn_nm_local_dirs = default("/configurations/gaia-yarn-site/gaia.nodemanager.local-dirs", "/yarnenv/local")
yarn_nm_local_dirs_fullpath = gaiautils().get_local_dirs(yarn_nm_local_dirs)

yarn_nm_reserve_cpu = default("/configurations/gaia-yarn-site/gaia.nodemanager.resource.reserved-cpu-vcores", "20")
yarn_nm_cpu = gaiautils().get_local_cpunum() * 10 - int(yarn_nm_reserve_cpu)


yarn_nm_reserve_mem  = default("/configurations/gaia-yarn-site/gaia.nodemanager.resource.reserved-memory-mb", "1024")
yarn_nm_mem = gaiautils().get_local_memorytotal() - int(yarn_nm_reserve_mem)

yarn_etcd = etcd_urls
etcd_hosts = default("/clusterHostInfo/etcd_service_hosts", [])

yarn_rm_zk = zk_urls

rm_hosts = default("/clusterHostInfo/gaia_resourcemanager_hosts", [])
yarn_rm1 = rm_hosts[0] if len(rm_hosts) > 0 else "127.0.0.1"
yarn_rm2 = rm_hosts[1] if len(rm_hosts) > 1 else "127.0.0.1"

tls_hosts = default("/clusterHostInfo/jobhistory_hosts", [])
yarn_tls = tls_hosts[0] if len(tls_hosts) > 0 else "127.0.0.1"


nodemanager_address = default("/configurations/gaia-yarn-site/gaia.nodemanager.address", "0.0.0.0:8041")
nodemanager_docker_hup_address = default("/configurations/gaia-yarn-site/gaia.nodemanager.docker-hup-address", "docker.oa.com")
nodemanager_local_docker_address = default("/configurations/gaia-yarn-site/gaia.nodemanager.local-docker-address", "http://localhost:2375")
nodemanager_localizer_address = default("/configurations/gaia-yarn-site/gaia.nodemanager.localizer.address", "0.0.0.0:18040")
nodemanager_webapp_address = default("/configurations/gaia-yarn-site/gaia.nodemanager.webapp.address", "0.0.0.0:8086")
resourcemanager_address_rm1 = default("/configurations/gaia-yarn-site/gaia.resourcemanager.address.rm1", "${gaia.resourcemanager.hostname.rm1}:18032")
resourcemanager_address_rm2 = default("/configurations/gaia-yarn-site/gaia.resourcemanager.address.rm2", "${gaia.resourcemanager.hostname.rm2}:18032")
resourcemanager_admin_address_rm1 = default("/configurations/gaia-yarn-site/gaia.resourcemanager.admin.address.rm1", "${gaia.resourcemanager.hostname.rm1}:18033")
resourcemanager_admin_address_rm2 = default("/configurations/gaia-yarn-site/gaia.resourcemanager.admin.address.rm2", "${gaia.resourcemanager.hostname.rm2}:18033")
resourcemanager_resource_tracker_address_rm1 = default("/configurations/gaia-yarn-site/gaia.resourcemanager.resource-tracker.address.rm1", "${gaia.resourcemanager.hostname.rm1}:18031")
resourcemanager_resource_tracker_address_rm2 = default("/configurations/gaia-yarn-site/gaia.resourcemanager.resource-tracker.address.rm2", "${gaia.resourcemanager.hostname.rm2}:18031")
resourcemanager_scheduler_address_rm1 = default("/configurations/gaia-yarn-site/gaia.resourcemanager.scheduler.address.rm1", "${gaia.resourcemanager.hostname.rm1}:18030")
resourcemanager_scheduler_address_rm2 = default("/configurations/gaia-yarn-site/gaia.resourcemanager.scheduler.address.rm2", "${gaia.resourcemanager.hostname.rm2}:18030")
resourcemanager_webapp_address_rm1 = default("/configurations/gaia-yarn-site/gaia.resourcemanager.webapp.address.rm1", "${gaia.resourcemanager.hostname.rm1}:8084")
resourcemanager_webapp_address_rm2 = default("/configurations/gaia-yarn-site/gaia.resourcemanager.webapp.address.rm2", "${gaia.resourcemanager.hostname.rm2}:8084")
timeline_service_webapp_address = default("/configurations/gaia-yarn-site/gaia.timeline-service.webapp.address", "${gaia.timeline-service.hostname}:8089")
web_proxy_address_rm1 = default("/configurations/gaia-yarn-site/gaia.web-proxy.address.rm1", "${gaia.resourcemanager.hostname.rm1}:8081")
web_proxy_address_rm2 = default("/configurations/gaia-yarn-site/gaia.web-proxy.address.rm2", "${gaia.resourcemanager.hostname.rm2}:8081")
api_server_address = default("/configurations/gaia-yarn-site/gaia.api-server-address", "http://${yarn.resourcemanager.cluster-id}.api.oa.com/api")
log_server_url = default("/configurations/gaia-yarn-site/gaia.log.server.url", "http://${yarn.timeline-service.webapp.address}/applicationhistory/logs")
gaia_home_dir = default("/configurations/gaia-yarn-site/gaia.home.dir", "/gaia/hadoop")
gaia_nodemanager_recovery_dir = default("/configurations/gaia-yarn-site/gaia.nodemanager.recovery.dir", "/gaia/recovery")

# ResourceManager
rm_name = "resourcemanager"
rm_start = yarn_start.format(rm_name)
rm_stop = yarn_stop.format(rm_name)
rm_keyword = "org.apache.hadoop.yarn.server.resourcemanager.ResourceManager"


# JobHistory Server
jobhistory_name = "historyserver"
jobhistory_start = yarn_start.format(jobhistory_name)
jobhistory_stop = yarn_stop.format(jobhistory_name)
jobhistory_keyword = "org.apache.hadoop.yarn.server.applicationhistoryservice.ApplicationHistoryServer"


# ResourceManager Haproxy
rmhaproxy_install_path = "/usr/local/haproxy"
rmhaproxy_start_script = "cd {}; ./restart.sh".format(rmhaproxy_install_path)
rmhaproxy_start_command = "({} &) &> /dev/null".format(rmhaproxy_start_script)
rmhaproxy_hosts = default("/clusterHostInfo/rmhaproxy_hosts", [])
rmhaproxy_key = rmhaproxy_install_path



# API Server
etcd_url = etcd_urls
gaia_cluster_default = default("/configurations/apiserver-properties/gaia.cluster.default",'gaia-test')
gaia_queue_default = default("/configurations/apiserver-properties/gaia.queue.default",'root.gaia')
server_port = default("/configurations/application-proerties/server.port",8085)
management_port = default("/configurations/application-proerties/management.port",8088)
spring_datasource_url = default("/configurations/application-proerties/spring.datasource.url",'jdbc:postgresql://10.196.152.110:5432/gaia_portal')
spring_datasource_username = default("/configurations/application-proerties/spring.datasource.username",'postgres')
spring_datasource_password = default("/configurations/application-proerties/spring.datasource.password","postgres")
spring_jpa_hibernate_ddl_auto = default("/configurations/application-proerties/spring.jpa.hibernate.ddl-auto","update")

docker_default_port = default("/configurations/application-proerties/docker.default.port",2375)

apiserver_start = gaia_script.format("(/gaia/apiserver/bin/run.sh &) &>/gaia/apiserver/log/start.log")
apiserver_keyword = "com.tencent.gaia.portal.ApiServer"
apiserver_config_path = "/gaia/apiserver/conf"
gaia_apiserver_hosts = default("/clusterHostInfo/apiserver_hosts", [])

if len(gaia_apiserver_hosts) == 1:
   gaia_apiserver_host1 = gaia_apiserver_hosts[0]
   gaia_apiserver_host2 = "127.0.0.1"
elif len(gaia_apiserver_hosts) >= 2:
   gaia_apiserver_host1 = gaia_apiserver_hosts[0]
   gaia_apiserver_host2 = gaia_apiserver_hosts[1]
else:
   gaia_apiserver_host1 = "127.0.0.1"
   gaia_apiserver_host2 = "127.0.0.1"

# Node Manager
nm_name = "nodemanager"
nm_start = yarn_start.format(nm_name)
nm_stop = yarn_stop.format(nm_name)
nm_status_key = "org.apache.hadoop.yarn.server.nodemanager.NodeManager"

# NodeManager Haproxy
nmhaproxy_install_path = "/usr/local/haproxy"
nmhaproxy_script = "cd {} && ./update_proxy.sh".format(nmhaproxy_install_path)
nmhaproxy_start = "({}&) &> /dev/null".format(nmhaproxy_script)
nmhaproxy_hosts = default("/clusterHostInfo/nmhaproxy_hosts", [])
nmhaproxy_key = "/usr/local/haproxy|./update_proxy.sh"

# Docker
docker_service = "docker"
docker_start = service_start.format(docker_service)
docker_stop = service_stop.format(docker_service)
docker_status_key = "running"

# Resource Monitor
resourcemonitor_log_dir = default("/configurations/resourcemonitor/log.dir", "logs")
resourcemonitor_from_cadvisor = "false"
resourcemonitor_listen_port = default("/configurations/resourcemonitor/listen.port", "36007")
resourcemonitor_nm_address = nodemanager_address.split(":")[-1]
resourcemonitor_save_interval = default("/configurations/resourcemonitor/save.interval", "60")

resourcemonitor_install_path = "/gaia/resource_monitor"
resourcemonitor_script = "cd {} && ./resource_monitor".format(resourcemonitor_install_path)
resourcemonitor_start = gaia_script.format("({} -log_dir={} -from_cadvisor={} -listen_port={} -nmAddress={} -saveInterval={} &) &> /dev/null".format(resourcemonitor_script, resourcemonitor_log_dir, resourcemonitor_from_cadvisor, resourcemonitor_listen_port, resourcemonitor_nm_address, resourcemonitor_save_interval))
resourcemonitor_key = "./resource_monitor"


