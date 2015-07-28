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

HIVE_PORT = '{{hive-site/hive.server2.thrift.port}}'

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (HIVE_PORT)
  

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

def execute(parameters=None, host_name=None):
  """
  Returns a tuple containing the result code and a pre-formatted result label

  Keyword arguments:
  parameters (dictionary): a mapping of parameter key to value
  host_name (string): the name of this host where the alert is running
  """

  if parameters is None:
    return (('UNKNOWN', ['There were no parameters supplied to the script.']))

  hive_user = "hive"
  hive_port = "10000"

  if HIVE_PORT in parameters:
    hive_port = parameters[HIVE_PORT]
    
  unique = str(uuid.uuid1()).replace("-","")
  tmp_table = "tmp_table_"+unique;
  ddl_create_table_cmd = "create table if not exists {0}(id int); ".format(tmp_table)
  ddl_drop_table_cmd = "drop table if exists {0};".format(tmp_table)
  #ddl_cmd = "show tables;"
  cmd = 'su -c \"/usr/hdp/2.2.0.0-2041/hive/bin/beeline -n hive -p hive -u jdbc:hive2://{0}:{1} -e \\\"{2}\\\" -e \\\"{3}\\\" \" {4}'.format(host_name, hive_port, ddl_create_table_cmd, ddl_drop_table_cmd, hive_user)
  
  result_code = 'OK'
  label = 'hive service is running.'
  
  try:
    _execute_command(cmd,90)
  except Exception,e:
    result_code = "CRITICAL"
    label = 'hive service runs failed:'+str(e)
  
  return ((result_code, [label]))