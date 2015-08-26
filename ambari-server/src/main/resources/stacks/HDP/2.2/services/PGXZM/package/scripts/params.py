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

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

# global
pgxzm_install_path = "/usr/local/pgxzm"

pgxzm_center_etc_sys = "{0}/center/etc/sys".format(pgxzm_install_path)
pgxzm_center_etc_sys_mq = "{0}/center/etc/sys/mq".format(pgxzm_install_path)

pgxzm_agent_etc_sys = "{0}/agent/etc/sys".format(pgxzm_install_path)
pgxzm_agent_etc_sys_mq = "{0}/agent/etc/sys/mq".format(pgxzm_install_path)

pgxm_pg_conf = "/var/lib/pgsql/9.3/data"

httpd_conf_dir = "/etc/httpd/conf.d"
cgi_conf_dir = "{0}/cgi"
web_conf_dir = "{0}/web/config"

pgxzm_cmd = "({0}&) &> /dev/null"
restart_httpd = "service httpd restart"

# Center
center_start = "{0}/center/tools/op/start.sh".format(pgxzm_install_path)
center_start = pgxzm_cmd.format(center_start)

center_stop = "{0}/center/tools/op/stop.sh".format(pgxzm_install_path)
center_stop = pgxzm_cmd.format(center_stop)

center_status = "./center_watchdog"

center_host = default("/clusterHostInfo/pgxzm_center_hosts", ["127.0.0.1"])[0]
center_ha_host = default("/clusterHostInfo/pgxzm_center_ha_hosts", ["127.0.0.1"])[0]
center_port = default("/configurations/pgxzm_global/center.port", 55001)

center_ccd_shm_key = default("/configurations/center_ccd/shm_key", 7151)
center_dcc_shm_key = default("/configurations/center_dcc/shm_key", 7161)

center_mcd0_shm_key = default("/configurations/center_mcd0/shm_key", 7111)
center_mcd0_center_is_master = 1
center_mcd0_heart_beat_cycle = default("/configurations/center_mcd0/heart_beat_cycle", 5)
center_mcd0_heart_beat_retry = default("/configurations/center_mcd0/heart_beat_retry", 3)
center_mcd0_handle_time_out = default("/configurations/center_mcd0/handle_time_out", 500)

center_mq_ccd_2_mcd0_shm_key = default("/configurations/center_mq_ccd_2_mcd0/shm_key", 1)
center_mq_ccd_2_mcd0_sem_name = default("/configurations/center_mq_ccd_2_mcd0/sem_name", "/center_1_qguo")
center_mq_ccd_2_mcd0_fifo_path = default("/configurations/center_mq_ccd_2_mcd0/fifo_path", "./tmp/center_1_ccd_2_mcd0.fifo")

center_mq_dcc_2_mcd0_shm_key = default("/configurations/center_mq_dcc_2_mcd0/shm_key", 3)
center_mq_dcc_2_mcd0_sem_name = default("/configurations/center_mq_dcc_2_mcd0/sem_name", "/center_3_qguo")
center_mq_dcc_2_mcd0_fifo_path = default("/configurations/center_mq_dcc_2_mcd0/fifo_path", "./tmp/center_3_dcc_2_mcd0.fifo")

center_mq_mcd0_2_ccd_shm_key = default("/configurations/center_mq_mcd0_2_ccd/shm_key", 2)
center_mq_mcd0_2_ccd_sem_name = default("/configurations/center_mq_mcd0_2_ccd/sem_name", "/center_2_qguo")
center_mq_mcd0_2_ccd_fifo_path = default("/configurations/center_mq_mcd0_2_ccd/fifo_path", "./tmp/center_2_mcd0_2_ccd.fifo")

center_mq_mcd0_2_dcc_shm_key = default("/configurations/center_mq_mcd0_2_dcc/shm_key", 4)
center_mq_mcd0_2_dcc_sem_name = default("/configurations/center_mq_mcd0_2_dcc/sem_name", "/center_4_qguo")
center_mq_mcd0_2_dcc_fifo_path = default("/configurations/center_mq_mcd0_2_dcc/fifo_path", "./tmp/center_4_mcd0_2_dcc.fifo")

center_watchdog_key = default("/configurations/center_watchdog/watchdog_key", 8114)

# Agent
agent_start = "{0}/agent/tools/op/start.sh".format(pgxzm_install_path)
agent_start = pgxzm_cmd.format(agent_start)

agent_stop = "{0}/agent/tools/op/stop.sh".format(pgxzm_install_path)
agent_stop = pgxzm_cmd.format(agent_stop)

agent_status = "./agent_watchdog"

agent_port = default("/configurations/pgxzm_global/agent.port", 55002)

agent_dcc_shm_key = default("/configurations/agent_dcc/shm_key", 5002)
agent_mcd0_shm_key = default("/configurations/agent_mcd0/shm_key", 5001)

agent_mq_dcc_2_mcd0_shm_key = default("/configurations/agent_mq_dcc_2_mcd0/shm_key", 1)
agent_mq_dcc_2_mcd0_sem_name = default("/configurations/agent_mq_dcc_2_mcd0/sem_name", "/qguo_2mcd0")
agent_mq_dcc_2_mcd0_fifo_path = default("/configurations/agent_mq_dcc_2_mcd0/fifo_path", "./tmp/CXZAgent_1_dcc_2_mcd0.fifo")

agent_mq_mcd0_2_dcc_shm_key = default("/configurations/agent_mq_mcd0_2_dcc/shm_key", 2)
agent_mq_mcd0_2_dcc_sem_name = default("/configurations/agent_mq_mcd0_2_dcc/sem_name", "/qguo_2dcc")
agent_mq_mcd0_2_dcc_fifo_path = default("/configurations/agent_mq_mcd0_2_dcc/fifo_path", "./tmp/CXZAgent_2_mcd0_2_dcc.fifo")

agent_watchdog_key = default("/configurations/agent_watchdog/watchdog_key", 911)

# Pg
pg_bin = "/etc/init.d/postgresql-9.3 {0}"

pg_init = pg_bin.format("initdb")
pg_start = pg_bin.format("start")
pg_stop = pg_bin.format("stop")
pg_status = pg_bin.format("status")

pg_host = default("/clusterHostInfo/pgxzm_global_hosts", ["127.0.0.1"])[0]
pg_port = default("/configurations/pgxzm_global/pgxzm.database.port", 5432)
pg_name = default("/configurations/pgxzm_global/pgxzm.database.name", "postgres")
pg_user = default("/configurations/pgxzm_global/pgxzm.database.user", "postgres")

pg_hba_cont = default("/configurations/pgxzm-database-env/content", "host    all             all             0.0.0.0/0         trust")

# Cgi
cgi_host = default("/clusterHostInfo/pgxzm_cgi_hosts", ["127.0.0.1"])[0]
cgi_port = default("/configurations/pgxzm_global/pgxzm.cgi.port", 80)
cgi_need_listen_port = (cgi_port != 80)

cgi_start = restart_httpd
cgi_stop = "rm -f {0}/pgczm-cgi.conf; {1}".format(httpd_conf_dir, restart_httpd)
cgi_status = "http://{0}:{1}/pgxzm-cgi".format(cgi_host, cgi_port)

# Web
web_host = default("/clusterHostInfo/pgxzm_web_hosts", ["127.0.0.1"])[0]
web_port = default("/configurations/pgxzm_global/pgxzm.web.port", 80)
web_need_listen_port = (web_port != 80)

web_start = restart_httpd
web_stop = "rm -f {0}/pgczm-web.conf; {1}".format(httpd_conf_dir, restart_httpd)
web_status = "http://{0}:{1}/pgxzm".format(web_host, web_port)

