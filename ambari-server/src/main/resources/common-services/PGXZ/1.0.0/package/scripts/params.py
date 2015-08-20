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
from utils import utils
config = Script.get_config()

#global settings
user_name = default("/configurations/pgxz-global/pgxz.username", "pgxz")
user_group = default("/configurations/cluster-env/user_group", "hadoop")
user_password = default("/configurations/pgxz-global/pgxz.password", "pgxz")


#component hosts
host_name = default("/hostname", "127.0.0.1")
gtm_host = default("/clusterHostInfo/pgxz_gtm_hosts", ["127.0.0.1"])[0]
coordinator_hosts = default("/clusterHostInfo/pgxz_coordinator_hosts", [])
datanode_hosts = default("/clusterHostInfo/pgxz_datanode_hosts", [])

#component port
gtm_port = default("/configurations/gtm-config-env/pgxz.gtm.port", 6666)
coordinator_port = default("/configurations/coordinator-config-env/pgxz.coordinator.port", 5434)
coordinator_pooler_port = default("/configurations/coordinator-config-env/pgxz.coordinator.pooler.port", 6668)
datanode_port = default("/configurations/datanode-config-env/pgxz.datanode.port", 5433)

#component content
gtm_content = default("/configurations/gtm-config-env/content", "")
coordinator_content = default("/configurations/coordinator-config-env/content", "")
datanode_content = default("/configurations/datanode-config-env/content", "")

#component auth ip
coordinator_auth_ip = default("/configurations/coordinator-config-env/authorized.ip", "")
datanode_auth_ip = default("/configurations/datanode-config-env/authorized.ip", "")

pgxz_path = "/usr/local/pgxz"

#component config directory
config_path = pgxz_path + "/nodes"
gtm_path = config_path + "/gtm"
coordinator_path = config_path + "/coordinator"
datanode_path = config_path + "/datanode"

#component pidfile
gtm_pid = gtm_path + "/gtm.pid"
coordinator_pid = coordinator_path + "/postmaster.pid"
datanode_pid = datanode_path + "/postmaster.pid"

#component name 
gtm_name = utils().get_gtm_name()
coordinator_name = utils().get_coordinator_name()
datanode_name = utils().get_datanode_name()

#component cmd
cmd_prefix = "cd " + pgxz_path + "; su " + user_name + " -c '"
cmd_suffix = "'"

bin_path= pgxz_path + "/bin"
initgtm = bin_path + "/initgtm"
initdb = bin_path + "/initdb"
gtm_ctl = bin_path + "/gtm_ctl"
pg_ctl = bin_path + "/pg_ctl"

gtm_install = cmd_prefix + initgtm + " -Z gtm -D " + gtm_path + cmd_suffix
gtm_start = cmd_prefix + gtm_ctl + " -Z gtm -D " + gtm_path + " start" + cmd_suffix
gtm_stop = cmd_prefix + gtm_ctl + " -Z gtm -D " + gtm_path + " stop" + cmd_suffix

coordinator_install = cmd_prefix + initdb + " -D " + coordinator_path + " --nodename " + coordinator_name + cmd_suffix
coordinator_start = cmd_prefix + pg_ctl + " start -D " + coordinator_path + " -Z coordinator" + cmd_suffix
coordinator_stop = cmd_prefix + pg_ctl + " stop -D " + coordinator_path + " -Z coordinator" + cmd_suffix

datanode_install = cmd_prefix + initdb + " -D " + datanode_path + " --nodename " + datanode_name + cmd_suffix
datanode_start = cmd_prefix + pg_ctl + " start -D " + datanode_path + " -Z datanode" + cmd_suffix
datanode_stop = cmd_prefix + pg_ctl + " stop -D " + datanode_path + " -Z datanode" + cmd_suffix

psql = bin_path + "/psql"
sql_str = "cd {0}; su {1} -c \"{2}\"".format(pgxz_path, user_name, "{0} -h {1} -p {2} postgres -c \\\"{3}\\\"").format(psql, "{0}", "{1}", "{2}")

# refractor service path

pgxz_install_path = "/usr/local/pgxz"

pgxz_conf_path_gtm = "/usr/local/pgxz/nodes/gtm"
pgxz_conf_path_coordinator = "/usr/local/pgxz/nodes/coordinator"
pgxz_conf_path_datanode = "/usr/local/pgxz/nodes/datanode"

pgxz_data_path_gtm = "/usr/local/pgxz/nodes/gtm"
pgxz_data_path_coordinator = "/usr/local/pgxz/nodes/coordinator"
pgxz_data_path_datanode = "/usr/local/pgxz/nodes/datanode"

new_pgxz_install_path = "/opt/tbds/pgxz"

new_pgxz_conf_path_gtm = "/etc/tbds/pgxz/gtm"
new_pgxz_conf_path_coordinator = "/etc/tbds/pgxz/coordinator"
new_pgxz_conf_path_datanode = "/etc/tbds/pgxz/datanode"

new_pgxz_data_path_gtm = "/data/tbds/pgxz/gtm"
new_pgxz_data_path_coordinator = "/data/tbds/pgxz/coordinator"
new_pgxz_data_path_datanode = "/data/tbds/pgxz/datanode"