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
from resource_management import *

import status_params

# server configurations
config = Script.get_config()

smoke_user =  config['configurations']['cluster-env']['smokeuser']

redis_bin_dir="/usr/bin"
redis_user="redis"

redis_port = config['configurations']['redis-env']['redis_port']
redis_log_file = config['configurations']['redis-env']['redis_log_file']
redis_conf_dir = config['configurations']['redis-env']['redis_conf_dir']
redis_pid_file = status_params.redis_pid_file

# refractor service path

redis_install_path = "/usr/bin/redis-server"
redis_config_path = "/etc/redis.conf"
redis_log_path = default("/configurations/redis-env/redis_log_file", "/data/var/log/redis")
redis_data_path = "/var/lib/redis"

new_redis_install_path = "/opt/tbds/redis"
new_redis_config_path = "/etc/tbds/redis/redis.conf"
new_redis_log_path = "/var/log/tbds/redis"
new_redis_data_path = "/data/tbds/redis"

