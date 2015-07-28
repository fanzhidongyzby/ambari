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
import socket

from resource_management.libraries.functions.default import default
from resource_management import *

config = Script.get_config()

etcd_listen_port = default("/configurations/etcd/etcd.listen.port",7001) 
etcd_server_port = default("/configurations/etcd/etcd.server.port",4001)
etcd_hosts = default("/clusterHostInfo/etcd_service_hosts", [])

local_hostname = socket.gethostname()

etcd_listen_ip_port = "http://{}:{}".format(local_hostname, etcd_listen_port)
etcd_server_ip_port = "http://{}:{}".format(local_hostname, etcd_server_port)
etcd_cluster_server_ip_port = ""

for ip in etcd_hosts:
    tmp = "{}=http://{}:{}".format(ip,ip,etcd_listen_port)
    etcd_cluster_server_ip_port = etcd_cluster_server_ip_port + "," + tmp

etcd_cluster_server_ip_port =  etcd_cluster_server_ip_port[1:] if len(etcd_cluster_server_ip_port)>1 else ""

etcd_start_cmd = "/gaia/etcd/etcd -name {} -data-dir=/gaia/etcd/backup -initial-advertise-peer-urls {} -listen-peer-urls {}  -listen-client-urls {} -advertise-client-urls {} -initial-cluster {} ".format(local_hostname,etcd_listen_ip_port,etcd_listen_ip_port,etcd_server_ip_port,etcd_server_ip_port,etcd_cluster_server_ip_port)


etcd_keyword = "/gaia/etcd/etcd"
