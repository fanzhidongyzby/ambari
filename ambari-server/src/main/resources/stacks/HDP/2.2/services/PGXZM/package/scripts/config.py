#!/usr/bin/env python
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
import os
from resource_management import *
from resource_management.core.logger import Logger

class config(Script):

  def update_center(self, env):
    import params

    Logger.info('create center_ccd.conf')
    File(os.path.join(params.pgxzm_center_etc_sys,'center_ccd.conf'),
         mode=0644,
         content=Template("center_ccd.conf.j2")
         )

    Logger.info('create center_dcc.conf')
    File(os.path.join(params.pgxzm_center_etc_sys,'center_dcc.conf'),
         mode=0644,
         content=Template("center_dcc.conf.j2")
         )

    Logger.info('create center_mcd0.conf')
    File(os.path.join(params.pgxzm_center_etc_sys,'center_mcd0.conf'),
         mode=0644,
         content=Template("center_mcd0.conf.j2")
         )

    Logger.info('create center_watchdog.conf')
    File(os.path.join(params.pgxzm_center_etc_sys,'center_watchdog.conf'),
         mode=0644,
         content=Template("center_watchdog.conf.j2")
         )

    Logger.info('create mq_ccd_2_mcd0.conf')
    File(os.path.join(params.pgxzm_center_etc_sys_mq,'mq_ccd_2_mcd0.conf'),
         mode=0644,
         content=Template("center_mq_ccd_2_mcd0.conf.j2")
         )

    Logger.info('create mq_dcc_2_mcd0.conf')
    File(os.path.join(params.pgxzm_center_etc_sys_mq,'mq_dcc_2_mcd0.conf'),
         mode=0644,
         content=Template("center_mq_dcc_2_mcd0.conf.j2")
         )

    Logger.info('create mq_mcd0_2_ccd.conf')
    File(os.path.join(params.pgxzm_center_etc_sys_mq,'mq_mcd0_2_ccd.conf'),
         mode=0644,
         content=Template("center_mq_mcd0_2_ccd.conf.j2")
         )

    Logger.info('create mq_mcd0_2_dcc.conf')
    File(os.path.join(params.pgxzm_center_etc_sys_mq,'mq_mcd0_2_dcc.conf'),
         mode=0644,
         content=Template("center_mq_mcd0_2_dcc.conf.j2")
         )

  def update_agent(self, env):
    import params

    Logger.info('create agent_dcc.conf')
    File(os.path.join(params.pgxzm_agent_etc_sys,'agent_dcc.conf'),
         mode=0644,
         content=Template("agent_dcc.conf.j2")
         )

    Logger.info('create agent_mcd0.conf')
    File(os.path.join(params.pgxzm_agent_etc_sys,'agent_mcd0.conf'),
         mode=0644,
         content=Template("agent_mcd0.conf.j2")
         )

    Logger.info('create agent_watchdog.conf')
    File(os.path.join(params.pgxzm_agent_etc_sys,'agent_watchdog.conf'),
         mode=0644,
         content=Template("agent_watchdog.conf.j2")
         )

    Logger.info('create mq_dcc_2_mcd0.conf')
    File(os.path.join(params.pgxzm_agent_etc_sys_mq,'mq_dcc_2_mcd0.conf'),
         mode=0644,
         content=Template("agent_mq_dcc_2_mcd0.conf.j2")
         )

    Logger.info('create mq_dcc_2_mcd0.conf')
    File(os.path.join(params.pgxzm_agent_etc_sys_mq,'mq_dcc_2_mcd0.conf'),
         mode=0644,
         content=Template("agent_mq_dcc_2_mcd0.conf.j2")
         )

  def update_pg(self, env):
    import params

    Logger.info('create postgresql.conf')
    File(os.path.join(params.pgxm_pg_conf,'postgresql.conf'),
         mode=0644,
         content=Template("pg_postgresql.conf.j2")
         )

    Logger.info('create pg_hba.conf')
    File(os.path.join(params.pgxm_pg_conf,'pg_hba.conf'),
         mode=0644,
         content=Template("pg_pg_hba.conf.j2")
         )

  def update_cgi(self, env):
    import params

    Logger.info('create pgxzm-cgi.conf')
    File(os.path.join(params.httpd_conf_dir,'pgxzm-cgi.conf'),
         mode=0644,
         content=Template("cgi_httpd.conf.j2")
         )

    Logger.info('create server.conf')
    File(os.path.join(params.cgi_conf_dir,'server.conf'),
         mode=0644,
         content=Template("cgi_server.conf.j2")
         )

  def update_web(self, env):
    import params

    Logger.info('create pgxzm-web.conf')
    File(os.path.join(params.httpd_conf_dir,'pgxzm-web.conf'),
         mode=0644,
         content=Template("web_httpd.conf.j2")
         )

    Logger.info('create config.conf')
    File(os.path.join(params.web_conf_dir,'setting.php'),
         mode=0644,
         content=Template("web_setting.php.j2")
         )



if __name__ == "__main__":
  pass
