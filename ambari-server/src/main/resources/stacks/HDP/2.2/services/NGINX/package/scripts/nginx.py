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
import sys

from resource_management.core.logger import Logger
from ambari_commons import OSConst
from resource_management import *
from utils import utils

class nginx(Script):


    def install(self, env):
        Logger.info("installed nginx")
        self.install_packages(env)


    def configure(self, env):
        import params
        Logger.info("update nginx.conf")

        File(os.path.join(params.nginx_log_path, 'access.log'),
             mode=0644,
             content=""
        )

        File(os.path.join(params.nginx_conf_path, 'nginx.conf'),
         mode=0644,
         content=Template("nginx.conf.j2")
         )              


        Logger.info("update default.conf")
        File(os.path.join(params.default_conf_path, 'default.conf'),
         mode=0644,
         content=Template("default.conf.j2")
         )        

    def start(self, env):
        import os
        import params

        env.set_params(params)
        self.configure(env)

        Logger.info("start nginx")
        utils().exe(params.nginx_start_command)

    def stop(self, env):
        import os
        import params
        Logger.info("stop nginx")
        utils().exe(params.nginx_stop_command)

    def status(self, env):
        import params
        Logger.info("check status of nginx")
        utils().check_service_status(params.nginx_service, params.nginx_status_key)



if __name__ == "__main__":
    nginx().execute()

