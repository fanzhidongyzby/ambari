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
from resource_management import *


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
  cmd = 'export PLCLIENT_PATH=/usr/local/thive/dist/PLClient; /usr/local/thive/dist/PLClient/PLC {0} {1} {2} {3} \"{4}\"'.format(thive_user, thive_password, host_name, thive_port,  ddl_cmd)
  
  result_code = 'OK'
  label = 'thive service is running.'
  try:
    Toolkit.execute_shell(cmd,timeout=120)
  except Exception,e:
    result_code = "CRITICAL"
    label = 'thive service runs failed'
    
  return ((result_code, [label]))