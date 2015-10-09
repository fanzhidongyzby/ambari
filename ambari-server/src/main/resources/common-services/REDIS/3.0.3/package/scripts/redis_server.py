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

class RedisServer(Script):
  def install(self, env):
    import params
    self.install_packages(env)
    self.configure(env)
    #Workaround to fix "couldn't open session when su redis"
    code, out = shell.call(["rm","/etc/security/limits.d/95-redis.conf"])
    if code:
        Logger.warning("Failed to remove 95-redis.conf")

    #create the parent directory of log file
    dirIndex = params.redis_log_file.rindex("/")
    parentDir = params.redis_log_file[0:dirIndex]
    Directory(parentDir)
    #create log file
    File(params.redis_log_file,
         owner=params.redis_user,
         group='hadoop',
         mode=0644,
         content=""
    )

    Links(params.new_redis_install_path, params.redis_install_path)
    Links(params.new_redis_config_path, params.redis_config_path)
    Links(params.new_redis_data_path, params.redis_data_path)

  def uninstall(self, env):
    Toolkit.uninstall_service("redis")

  def configure(self, env):
    import params
    env.set_params(params)
    File(os.path.join(params.redis_conf_dir, 'redis.conf'),
         owner='root',
         group='root',
         mode=0644,
         content=Template("redis.conf.j2")
    )

  def start(self, env, rolling_restart=False):
    import params
    env.set_params(params)
    self.configure(env)
    daemon_cmd = format('{params.redis_bin_dir}/redis-server {params.redis_conf_dir}/redis.conf')
    Execute(daemon_cmd,
            user=params.redis_user
    )
    Links(params.new_redis_log_path, params.new_redis_log_path)


  def stop(self, env, rolling_restart=False):
    import params
    env.set_params(params)
    self.configure(env)
    try:
        pid = int(sudo.read_file(params.redis_pid_file))
        code, out = shell.call(["kill","-15", str(pid)])
    except:
        Logger.warning("Pid file {0} does not exist".format(params.redis_pid_file))
        return

    if code:
        Logger.warning("Process with pid {0} is not running. Stale pid file"
                       " at {1}".format(pid, params.redis_pid_file))

  def status(self, env):
    import status_params
    env.set_params(status_params)
    check_process_status(status_params.redis_pid_file)

if __name__ == "__main__":
  RedisServer().execute()
