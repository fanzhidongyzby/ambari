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
import os
from resource_management import *
from resource_management.core.logger import Logger
from utils import utils

class mysqlServer(Script):


    def install(self, env):
        import params
        env.set_params(params)

        Logger.info("install mysql")
        excludePackage = ['dse']
        self.install_packages(env,excludePackage)
        utils().generate_db_script(env)
        
        #init db
        cmd = params.mysql_init_command
        utils().exe(cmd)

    def uninstall(self, env):
        Toolkit.uninstall_service("dse")

    def configure(self, env):
        import params
        Logger.info("have no configure need to update")

    def start(self, env):
        import os
        import params
        Logger.info("start mysql")
        cmd = "sudo service mysqld start"
        utils().exe(cmd)
        

    def stop(self, env):
        import os
        import params

        Logger.info("stop mysql")
        cmd = "sudo service mysqld stop"

        utils().exe(cmd)

    def status(self, env):
        import os.path
        import params
        utils().check_service_status(params.mysql_service, params.mysql_keyword)



if __name__ == "__main__":
    mysqlServer().execute()

