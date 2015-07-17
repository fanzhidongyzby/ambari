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

THIVE_USER = '{{thive-config-env/hive.plc.user}}'
THIVE_PASSWORD = '{{thive-config-env/hive.plc.password}}'
THIVE_PORT = '{{thive-config-env/thive.server.port}}'

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (THIVE_USER, THIVE_PASSWORD, THIVE_PORT)
  

def execute_command(cmdstring, timeout=None, shell=True):
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
          return 1,"Timeout:%s"%cmdstring
        
    stdout,stderr = sub.communicate()
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

  thive_user = "thive"
  thive_password = "thive"
  hdfs_user = "hdfs"
  thive_port = "10002"

  if THIVE_USER in parameters:
    thive_user = parameters[THIVE_USER]
    
  if THIVE_PASSWORD in parameters:
    thive_password = parameters[THIVE_PASSWORD]
    
  if THIVE_PORT in parameters:
    thive_port = parameters[THIVE_PORT]
    
  unique = str(uuid.uuid1()).replace("-","")
  tmp_table = "tmp_table_"+unique;
  ddl_cmd = "create table {0}(id int); drop table {1};".format(tmp_table, tmp_table)
  #ddl_cmd = "show tables;"
  cmd = 'export PLCLIENT_PATH=/usr/local/thive/dist/PLClient; su -c \"/usr/local/thive/dist/PLClient/PLC {0} {1} {2} {3} \\\"{4}\\\"\" {5}'.format(thive_user, thive_password, host_name, thive_port,  ddl_cmd, hdfs_user)
  (ret, out) = execute_command(cmd,60)
  
  if ret == 0:
    label = 'thive service is running.'
    result_code = 'OK'
  else:
    label = 'thive service runs failed:'+out
    result_code = 'CRITICAL'

  return ((result_code, [label]))