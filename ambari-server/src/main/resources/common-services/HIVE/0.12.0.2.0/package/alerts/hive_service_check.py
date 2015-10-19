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

import uuid
from resource_management import *


LABEL = 'Last Checkpoint: [{h} hours, {m} minutes, {tx} transactions]'

HIVE_PORT = '{{hive-site/hive.server2.thrift.port}}'
HIVE_USER = '{{hive-site/javax.jdo.option.ConnectionUserName}}'
HIVE_PASSWORD = '{{hive-site/javax.jdo.option.ConnectionPassword}}'

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (HIVE_PORT,HIVE_USER,HIVE_PASSWORD)

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
  connect_user = "hive"
  connect_pwd = "hive"

  if HIVE_PORT in parameters:
    hive_port = parameters[HIVE_PORT]
  if HIVE_USER in parameters:
    connect_user = parameters[HIVE_USER]
  if HIVE_PASSWORD in parameters:
    connect_pwd = parameters[HIVE_PASSWORD]
    
  tmp_table = "service_check_table";
  ddl_create_table_cmd = "create table if not exists {0}(id int); ".format(tmp_table)
  ddl_drop_table_cmd = "drop table if exists {0};".format(tmp_table)
  #ddl_cmd = "show tables;"
  cmd = 'su -c \"/usr/hdp/2.2.0.0-2041/hive/bin/beeline -n {0} -p {1} -u jdbc:hive2://{2}:{3} -e \\\"{4}\\\" -e \\\"{5}\\\" \" {6}'.format(connect_user, connect_pwd, host_name, hive_port, ddl_create_table_cmd, ddl_drop_table_cmd, hive_user)
  
  result_code = 'OK'
  label = 'hive service is running.'
  
  try:
    Toolkit.execute_shell(cmd,timeout=90)
  except Exception,e:
    result_code = "CRITICAL"
    label = 'hive service runs failed'
  
  return ((result_code, [label]))