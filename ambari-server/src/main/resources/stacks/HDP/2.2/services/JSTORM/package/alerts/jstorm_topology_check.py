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

LABEL = 'Last Checkpoint: [{h} hours, {m} minutes, {tx} transactions]'

UI_PORT = '{{jstorm/ui.port}}'
LOGVIEWER_PORT = '{{jstorm/logviewer.port}}'

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (UI_PORT, LOGVIEWER_PORT)
  
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
          sub.terminate()
          raise Exception(1, "Timeout:%s"%cmdstring)
          
    stdout,stderr = sub.communicate()
    if sub.returncode != 0:
      raise Exception(sub.returncode, stdout+stderr)
    return sub.returncode,stdout+stderr
    
    
def execute(parameters=None, host_name=None):
  """
  Returns a tuple containing the result code and a pre-formatted result label

  Keyword arguments:
  parameters (dictionary): a mapping of parameter key to value
  host_name (string): the name of this host where the alert is running
  """

  if parameters is None:
    return (('UNKNOWN', ['There were no parameters supplied to the script.']))

  unique = str(uuid.uuid1()).replace("-","") 
  bin_dir = "/usr/local/jstorm/bin" 
  jar_dir = "/usr/local/jstorm"
  storm_user = "jstorm"

  cmd = 'su -c "{0}/storm jar {1}/storm-starter-topologies.jar storm.starter.WordCountTopology ServiceCheckWordCountTopology{2}" - {3}'.format(bin_dir,jar_dir,unique,storm_user)
  killCmd = 'su -c "{0}/storm kill WordCountTopology{1}" - {2}'.format(bin_dir,unique,storm_user)
  label = 'jstorm service is good'
  result_code = 'OK'
  try:
    _execute_command(cmd, 90)
    _execute_command(killCmd, 90)
  except Exception,e:
    result_code = "CRITICAL"
    label = 'jstorm service is down:'+str(e)
  
  return ((result_code, [label]))
