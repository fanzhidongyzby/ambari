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
import json
import datetime
import uuid
import shlex
import subprocess
import time

from resource_management.libraries.functions.format import format
from resource_management.libraries.functions import get_unique_id_and_date
from resource_management.core.resources import File
from resource_management.core.resources import Execute
from resource_management.libraries.script import Script
from resource_management.core.source import StaticFile


def _execute_command(cmdstring, timeout=None, shell=True):
    if shell:
      cmdstring_list = cmdstring
    else:   
      cmdstring_list = shlex.split(cmdstring)
    if timeout:
      end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    
    sub = subprocess.Popen(cmdstring_list, stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE,shell=shell)
    
    while sub.poll() is None:
      time.sleep(0.1)
      if timeout:
        if end_time <= datetime.datetime.now():
          raise Exception(1, "Timeout:%s"%cmdstring)
          
    stdout,stderr = sub.communicate()
    if sub.returncode != 0:
      raise Exception(sub.returncode, stdout+stderr)
    return sub.returncode,stdout+stderr

class ServiceCheck(Script):
  def service_check(self, env):
    import params
    env.set_params(params)

    unique = get_unique_id_and_date()
    storm_user = params.storm_user
    
    #cmd = 'su -c "{0}/storm jar {1}/storm-starter-topologies.jar storm.starter.WordCountTopology WordCountTopology{2}" - {3}'.format(params.bin_dir,params.root_dir,unique,storm_user)
    #killCmd = 'su -c "{0}/storm kill WordCountTopology{1}" - {2}'.format(params.bin_dir,unique,storm_user)
    #_execute_command(cmd,60)
    #_execute_command(killCmd,60)
    

if __name__ == "__main__":
  ServiceCheck().execute()
