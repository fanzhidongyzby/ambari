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

class Hue(Script):
  def install(self, env):
    self.install_packages(env)
    import params
    # configure django settings to replace cas server url
    daemon_cmd = 'sed -i \'s/{{CAS_SERVER_URL}}/"{0}"/g\' {1}'.format(
        params.sso_cas_url.replace('/', '\/'), params.hue_django_settings)
    Execute(daemon_cmd,
            user=params.hue_user,
            )
    # create default admin user
    if "admin" != params.hue_admin_user:
        daemon_cmd = '{0} createsuperuser --username {1} --email {1}@tencent.com --noinput'.format(
            params.hue_admin_bin, params.hue_admin_user)
        print daemon_cmd
        Execute(daemon_cmd,
            user=params.hue_user,
            )
    self.configure(env)

  def uninstall(self, env):
    Toolkit.uninstall_service("hue")

  def configure(self, env):
    import params
    env.set_params(params)

    File(os.path.join(params.hue_conf_dir, 'hue.ini'),
         owner=params.hue_user,
         group='hadoop',
         mode=0644,
         content=Template("hue.ini.j2")
         )

  def start(self, env, rolling_restart=False):
    import params
    env.set_params(params)
    self.configure(env)

    pid_file = params.hue_pid_file
    if pid_file and os.path.isfile(pid_file):
        return

    daemon_cmd = "{0} -d -p {1}".format(params.hue_bin, params.hue_pid_file)
    Execute(daemon_cmd,
            user=params.hue_user,
    )

  def stop(self, env, rolling_restart=False):
    import params
    env.set_params(params)
    self.configure(env)

    daemon_cmd = 'kill -15 $(cat {0})'.format(params.hue_pid_file)
    Execute(daemon_cmd,
            user=params.hue_user,
            )

  def status(self, env):
    import status_params
    env.set_params(status_params)
    check_process_status(status_params.hue_pid_file)

if __name__ == "__main__":
    Hue().execute()
