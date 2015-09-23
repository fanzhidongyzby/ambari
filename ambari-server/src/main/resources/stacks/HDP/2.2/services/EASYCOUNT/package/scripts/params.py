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
from resource_management.libraries.script import Script

# server configurations
config = Script.get_config()


# configfile.xml
storm_user = config['configurations']['configfile']['jstorm.user']
storm_group = config['configurations']['configfile']['jstorm.group']

toplogyname = config['configurations']['configfile']['ToplogyName']
consumergroup = config['configurations']['configfile']['ConsumerGroup']
localMode = config['configurations']['configfile']['LocalMode']
work_num = config['configurations']['configfile']['work.num']
work_tasknum_decrease_factor = config['configurations']['configfile']['work.tasknum.decrease.factor']
compile = config['configurations']['configfile']['compile']
moniter_send_status = config['configurations']['configfile']['moniter.send.status']
consumefrommaxoffset = config['configurations']['configfile']['ConsumeFromMaxOffset']
gby_max_timeout = config['configurations']['configfile']['gby.max.timeout']
real_work_num = config['configurations']['configfile']['real.work.num']


# configfile-env.xml
sql_config_content = config['configurations']['configfile-env']['content']

# sysconfig-env.xml
sys_config_content = config['configurations']['sysconfig-env']['content']

# jstorm params
jstorm_install_path = "/usr/local/jstorm"
jstorm_config_path = "/usr/local/jstorm/conf"

# refractor service path
easycount_install_path = "/usr/hdp/2.2.0.0-2041/easycount"

new_easycount_install_path = "/data/tbds/easycount"
