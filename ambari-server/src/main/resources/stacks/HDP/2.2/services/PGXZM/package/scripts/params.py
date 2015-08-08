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

pgxzm_center_etc_sys = "/usr/local/pgxzm/center/etc/sys"
pgxzm_center_etc_sys_mq = "/usr/local/pgxzm/center/etc/sys/mq"

pgxzm_agent_etc_sys = "/usr/local/pgxzm/agent/etc/sys"
pgxzm_agent_etc_sys_mq = "/usr/local/pgxzm/agent/etc/sys/mq"

pgxzm_cmd = "({0}&) &> /dev/null"

# Center
center_start = "{0}/center/tools/op/start.sh".format(pgxzm_install_path)
center_start = pgxzm_cmd.format(center_start)

center_stop = "{0}/center/tools/op/stop.sh".format(pgxzm_install_path)
center_stop = pgxzm_cmd.format(center_stop)

center_status = "./center_watchdog"

center_mcd0_center_host = default("/clusterHostInfo/pgxzm_center_hosts", ["127.0.0.1"])[0]

center_ccd_shm_key = default("/configurations/center_ccd/shm_key", 7151)
center_dcc_shm_key = default("/configurations/center_dcc/shm_key", 7161)

center_mcd0_center_port = default("/configurations/center_mcd0/center.port", 55001)
center_mcd0_shm_key = default("/configurations/center_mcd0/shm_key", 7111)
center_mcd0_center_is_master = default("/configurations/center_mcd0/center_is_master", 1)
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

agent_dcc_shm_key = default("/configurations/agent_dcc/shm_key", 5002)
agent_mcd0_shm_key = default("/configurations/agent_mcd0/center.port", 5001)

agent_mq_dcc_2_mcd0_shm_key = default("/configurations/agent_mq_dcc_2_mcd0/shm_key", 1)
agent_mq_dcc_2_mcd0_sem_name = default("/configurations/agent_mq_dcc_2_mcd0/sem_name", "/qguo_2mcd0")
agent_mq_dcc_2_mcd0_fifo_path = default("/configurations/agent_mq_dcc_2_mcd0/fifo_path", "./tmp/CXZAgent_1_dcc_2_mcd0.fifo")

agent_mq_mcd0_2_dcc_shm_key = default("/configurations/agent_mq_mcd0_2_dcc/shm_key", 2)
agent_mq_mcd0_2_dcc_sem_name = default("/configurations/agent_mq_mcd0_2_dcc/sem_name", "/qguo_2dcc")
agent_mq_mcd0_2_dcc_fifo_path = default("/configurations/agent_mq_mcd0_2_dcc/fifo_path", "./tmp/CXZAgent_2_mcd0_2_dcc.fifo")

agent_watchdog_key = default("/configurations/agent_watchdog/watchdog_key", 911)





