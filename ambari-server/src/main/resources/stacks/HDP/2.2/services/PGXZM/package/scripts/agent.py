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

import time
from resource_management import *
from resource_management.core.logger import Logger
from utils import utils
from config import config

class Agent(Script):

  def install(self, env):
    Logger.info("install Agent")
    self.install_packages(env)


  def configure(self, env):
    Logger.info('configure Agent')
    config().update_agent(env)

  def start(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    Logger.info("start Agent")
    utils().exe(params.agent_start)

  def stop(self, env):
    import params
    env.set_params(params)

    Logger.info("stop Agent")
    utils().exe(params.agent_stop)
    time.sleep(5)

  def status(self, env):
    import params
    Logger.info("check status of Agent")
    utils().check_process(params.agent_status)                                                                                                            

if __name__ == "__main__":
    Agent().execute()


