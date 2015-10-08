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

Ambari Agent

"""

from resource_management import *
import os


class EasyCountClient(Script):

    def install(self, env):
        self.install_packages(env)
        self.configure(env)

        import params
        Links(params.new_easycount_install_path, params.easycount_install_path)

    def uninstall(self, env):
        Toolkit.uninstall_service("easycount")

    def configure(self, env):
        import params
        env.set_params(params)

        # toplogy directory
        toplogy_path = os.path.join(params.easycount_install_path, params.toplogyname)
        Directory(toplogy_path, owner=params.storm_user)

        # sysconfig file
        sysconfig_file = os.path.join(toplogy_path, 'sys_configfile')
        File(sysconfig_file,
             content=Template('sys_configfile.j2'),
             owner=params.storm_user,
             group=params.storm_group,
             mode=0644)

        # sysconfig file
        sysconfig_file = os.path.join(toplogy_path, 'sql_configfile.ec')
        File(sysconfig_file,
             content=Template('sql_configfile.ec.j2'),
             owner=params.storm_user,
             group=params.storm_group,
             mode=0644)

        # sysconfig file
        sysconfig_file = os.path.join(toplogy_path, 'easycount.sh')
        File(sysconfig_file,
             content=Template('easycount.sh.j2'),
             owner=params.storm_user,
             group=params.storm_group,
             mode=0744)

        def status(self, env):
            raise ClientComponentHasNoStatus()

if __name__ == "__main__":
    EasyCountClient().execute()
