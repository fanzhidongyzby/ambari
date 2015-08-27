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

class dse(Script):


    def install(self, env):
        Logger.info("install dse")
        excludePackage = ['mysql-server*']

        self.install_packages(env,excludePackage)


    def configure(self, env):
        import params
        Logger.info('update config')
        Logger.info("update server.conf")
        File(os.path.join(params.server_conf_path,'server.conf'),
          mode=0755,
          content=Template("server.conf.j2")
        )

        Logger.info("update start.sh")
        File(os.path.join(params.dse_bin_dir,'start.sh'),
             mode=0755,
             content=Template("server.start.sh.j2")
             )

        Logger.info("update kill.sh")
        File(os.path.join(params.dse_bin_dir,'kill.sh'),
             mode=0755,
             content=Template("server.kill.sh.j2")
             )

        Logger.info("update db.properties")
        File(os.path.join(params.db_properties_path,'db.properties'),
          mode=0755,
          content=Template("db.properties.j2")
        )               
        
        Logger.info("update kafka.properties")
        File(os.path.join(params.kafka_properties_path,'kafka.properties'),
          mode=0755,
          content=Template("kafka.properties.j2")
        )               

    def start(self, env):
        import os
        import params
        env.set_params(params)

        self.configure(env)
        Logger.info("start dse")
        utils().exe(params.dse_start_command)


    def stop(self, env):
        import os
        import params
        Logger.info("stop dse")
        utils().exe(params.dse_stop_command)

    def status(self, env):
        import os.path
        import params
        utils().check_process(params.dse_keyword) 



if __name__ == "__main__":
    dse().execute()

