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

HDFS_USER = '{{hadoop-env/hdfs_user}}'
NN_HTTP_ADDRESS_KEY = '{{hdfs-site/dfs.namenode.http-address}}'

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (HDFS_USER,NN_HTTP_ADDRESS_KEY)
  
def _executeHadoop(hdfs_user, cmd, not_if=None, yes_if=None):
  hadoop_bin = "/usr/bin/hadoop"
  hadoop_conf_dir = "/etc/hadoop/conf"
  if not_if != None:
    try:
      Toolkit.execute_shell('su -c "{0} --config {1} {2}" - {3}'.format(hadoop_bin,hadoop_conf_dir,not_if,hdfs_user),timeout=120)
      return True
    except Exception,e:
      print "{0} return false".format(not_if)
      
  if yes_if != None:
    Toolkit.execute_shell('su -c "{0} --config {1} {2}" - {3}'.format(hadoop_bin,hadoop_conf_dir,yes_if,hdfs_user),timeout=120)
          
  hdfs_cmd = 'su -c "{0} --config {1} {2}" - {3}'.format(hadoop_bin,hadoop_conf_dir,cmd,hdfs_user);
  return Toolkit.execute_shell(hdfs_cmd,timeout=300)

def execute(parameters=None, host_name=None):
  """
  Returns a tuple containing the result code and a pre-formatted result label
  
  Keyword arguments:
  parameters (dictionary): a mapping of parameter key to value
  host_name (string): the name of this host where the alert is running
  """
  if parameters is None:
    return (('UNKNOWN', ['There were no parameters supplied to the script.']))
  
  hdfs_user = "hdfs"
 
  if HDFS_USER in parameters:
    hdfs_user = parameters[HDFS_USER]
  
  unique = str(uuid.uuid1()).replace("-","")
  dir = '/tmp'
  tmp_file = dir+"/hdfs_service_check"+unique
  
  test_dir_exists ="fs -test -e {0}".format(dir)
  create_dir_cmd = "fs -mkdir {0}".format(dir)
  
  chmod_command = "fs -chmod 777 {0}".format(dir)
  
  create_file_cmd = "fs -put /etc/passwd {0}".format(tmp_file)
  
  cleanup_cmd = "fs -rm {0}".format(tmp_file)
  test_file_exists ="fs -test -e {0}".format(tmp_file)
  
  label = 'HDFS service is good'
  result_code = 'OK'
  try:
    _executeHadoop(hdfs_user, create_dir_cmd, test_dir_exists)
    _executeHadoop(hdfs_user, chmod_command)
    _executeHadoop(hdfs_user, create_file_cmd)
  except Exception,e:
    result_code = "CRITICAL"
    label = 'hdfs service is down:'+str(e)
  
  _executeHadoop(hdfs_user, cleanup_cmd, None, test_file_exists)
  
  return ((result_code, [label]))