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

import sys
from resource_management import *
from resource_management.core.logger import Logger
from utils import utils
from configinit import configinit

class ApiServer(Script):


    def install(self, env):
        Logger.info("install apiserver")        
        excludePackage = ['docker-ng','hadoop-ng','haproxy-ng','resource_monitor']
        self.install_packages(env,excludePackage)


    def configure(self, env):
        configinit().update_apiserver_configs(env)

    def start(self, env):
        import params
        env.set_params(params)

        self.configure(env)

        Logger.info("start apiserver")
        utils().exe(params.apiserver_start)

    def stop(self, env):
        import params

        Logger.info("stop apiserver")
        utils().kill_process(params.apiserver_keyword)

    def status(self, env):
        import params
        Logger.info("status apiserver")
        utils().check_process(params.apiserver_keyword)
   


if __name__ == "__main__":
    ApiServer().execute()

