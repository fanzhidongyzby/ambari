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

class etcd(Script):

    def install(self, env):
        import params
        env.set_params(params)

        self.install_packages(env)

        Logger.info("first start etcd")
        cmd = params.etcd_start_cmd
        cmd = cmd + " -initial-cluster-state new >>/gaia/etcd/backup/etcd.log  2>&1 &"
        cmd = "su gaia -c '{}'".format(cmd)
        utils().exe(cmd)

    def configure(self, env):
        print 'configured etcd'

    def start(self, env):
        import params
        env.set_params(params)

        cmd = params.etcd_start_cmd
        cmd = cmd + " -initial-cluster-state existing >>/gaia/etcd/backup/etcd.log  2>&1 &"
        cmd = "su gaia -c '{}'".format(cmd)
        Logger.info("start etcd")
        utils().exe(cmd)

    def stop(self, env):
        import params
        Logger.info("stop etcd")
        utils().kill_process(params.etcd_keyword)

    def status(self, env):
        import params
        utils().check_process(params.etcd_keyword) 



if __name__ == "__main__":
    etcd().execute()

