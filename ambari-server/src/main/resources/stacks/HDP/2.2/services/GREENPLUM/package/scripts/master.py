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
import subprocess

class GPMaster(Script):
  def install(self, env):
    self.install_packages(env)
    import params
    env.set_params(params)

    daemon_cmd = "cd {0};unzip {1}".format(params.gp_install_dir, params.gp_install_zip)
    Execute(daemon_cmd,
          user=params.gp_user,
          )
    daemon_cmd = "ln -s {0} {1}".format(params.gp_install_dir, params.gp_install_symlink)
    Execute(daemon_cmd,
            user="root",
            )

    Directory(params.gp_conf_dir,
              owner=params.gp_user,
              recursive=True
              )
    Directory(params.gp_log_dir,
              owner=params.gp_user,
              recursive=True
              )
    Directory(params.gp_master_data_dir,
              owner=params.gp_user,
              recursive=True
              )
    Directory(params.gp_segment_data_dir,
              owner=params.gp_user,
              recursive=True
              )

    File(os.path.join(params.gp_conf_dir, 'gpinitsystem_config'),
         owner=params.gp_user,
         group=params.user_group,
         mode=0644,
         content=Template("gpinitsystem_config.j2")
         )

    hosts = params.gp_master_host + "\n"
    for host in params.gp_segment_hosts:
        hosts += host + "\n"
    File(os.path.join(params.gp_conf_dir, 'hostfile_gpinitsystem'),
         owner=params.gp_user,
         group=params.user_group,
         mode=0644,
         content=hosts
         )

    File(params.expect_script,
         owner=params.gp_user,
         group=params.user_group,
         mode=0755,
         content=StaticFile("execExpect.sh")
         )

    self.configure(env)

  def uninstall(self, env):
    Toolkit.uninstall_service("greenplum")

  def configure(self, env):
    import params
    env.set_params(params)

  def start(self, env, rolling_restart=False):
    import params
    env.set_params(params)
    self.configure(env)

    if os.path.isfile(params.gp_install_flag):
        daemon_cmd = "source {0}/greenplum_path.sh;MASTER_DATA_DIRECTORY={1} {2}/gpstart -a" \
            .format(params.gp_install_dir, params.gp_master_data_dir+"/gpseg-1", params.gp_install_bin)
        print "Start gp: {0}".format(daemon_cmd)
        Execute(daemon_cmd,
            user=params.gp_user,
            )
    else:
        gpInit_cmd = "source {3}/greenplum_path.sh;MASTER_DATA_DIRECTORY={2} " \
                    "{0}/gpinitsystem -a -c {1}/gpinitsystem_config -h {1}/hostfile_gpinitsystem " \
                     "> {4} 2>&1" \
            .format(params.gp_install_bin, params.gp_conf_dir, params.gp_master_data_dir+"/gpseg-1",
                    params.gp_install_dir, params.gp_log_file)
        daemon_cmd = '{0} 3600 "{1}"'.format(params.expect_script, gpInit_cmd)
        Execute(daemon_cmd,
                user=params.gp_user,
               )

        logFile = open(params.gp_log_file, 'r')
        log = logFile.read()
        print log

        if "Greenplum Database instance successfully created" not in log:
            raise Fail("Failed to initialize system")

        daemon_cmd = "touch {0}".format(params.gp_install_flag)
        Execute(daemon_cmd,
                user=params.gp_user,
                )

  def stop(self, env, rolling_restart=False):
    import params
    env.set_params(params)
    self.configure(env)

    daemon_cmd = "source {0}/greenplum_path.sh;MASTER_DATA_DIRECTORY={1} {2}/gpstop -a"\
        .format(params.gp_install_dir, params.gp_master_data_dir+"/gpseg-1", params.gp_install_bin)
    print "Stop gp: {0}".format(daemon_cmd)

    Execute(daemon_cmd,
            user=params.gp_user,
            )

  def status(self, env):
    import status_params
    env.set_params(status_params)

    psCmd = "ps -ef|grep greenplum|grep -v grep|awk '{print $2}'"
    psProcess = subprocess.Popen(psCmd, shell=True, stdout=subprocess.PIPE)
    stdout = psProcess.communicate()[0]

    if not stdout:
        raise ComponentIsNotRunning()

if __name__ == "__main__":
    GPMaster().execute()
