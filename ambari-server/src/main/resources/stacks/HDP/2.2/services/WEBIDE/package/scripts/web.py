#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE files
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this files
to you under the Apache License, Version 2.0 (the
"License"); you may not use this files except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
import sys
import commands
from resource_management import *
from resource_management.core.logger import Logger


class WebIDE(Script):

    def install(self, env):
        import params
        self.install_packages(env, ["postgresql93*"])
        Links(params.new_webide_install_path, params.webide_install_path)
        Links(params.new_webide_log_path, params.webide_log_path)

        self.configure(env)

    def uninstall(self, env):
        Toolkit.uninstall_service("webide")

    def configure(self, env):
        import params
        env.set_params(params)

        # add template files
        File(params.webide_conf_path, mode=0644, content=Template("webide.conf.j2"))
        File(params.webide_rest_uri_file_path, mode=0644, content=Template("setting.php.j2"))
        File(params.config_web_script, mode=0755, content=Template("configWeb.sh.j2"))
        File(params.http_conf_path, mode=0644, content=Template("httpd.conf.j2"))

        cmd = format("sudo bash -x {config_web_script}")
        (ret, output) = commands.getstatusoutput(cmd)
        Logger.info(cmd)
        if ret != 0:
            Logger.info(output)
            Logger.error("httpd config fail")
            sys.exit(1)

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)

    def stop(self, env):
        import params
        env.set_params(params)

        #delete conf files
        cmd = format("rm  {webide_conf_path}")
        commands.getstatusoutput(cmd)
        commands.getstatusoutput("service httpd restart")

    def status(self, env):
        import status_params

        cmd = "curl -I \"" + status_params.webide_web_url + "\" 2> /dev/null | awk 'NR==1{print}' | awk '{print $2}'"
        Logger.info("run cmd = {0}".format(cmd))
        (ret, output) = commands.getstatusoutput(cmd)
        if output != "301":
            Logger.error("webide not exists")
            raise ComponentIsNotRunning()

if __name__ == "__main__":
    WebIDE().execute()
