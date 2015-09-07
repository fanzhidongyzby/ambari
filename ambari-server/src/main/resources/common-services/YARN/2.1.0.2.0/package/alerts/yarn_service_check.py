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

YARN_WEB_ADDRESS = '{{yarn-site/yarn.resourcemanager.webapp.address}}'
YARN_USER = '{{yarn-env/yarn_user}}'

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (YARN_WEB_ADDRESS,YARN_USER)
  
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
          sub.terminate()
          return 1,"Timeout:%s"%cmdstring
        
    stdout,stderr = sub.communicate()
    return sub.returncode,stdout+stderr
  
def _executeHadoop(hdfs_user, cmd, not_if=None, yes_if=None):
  hadoop_bin = "/usr/bin/hadoop"
  hadoop_conf_dir = "/etc/hadoop/conf"
  if not_if != None:
    (not_if_ret, not_if_out) = execute_command('su -c "{0} --config {1} {2}" - {3}'.format(hadoop_bin,hadoop_conf_dir,not_if,hdfs_user),60)
    if not_if_ret == 0:
      return (not_if_ret, "cmd[ {0} ] success;".format(cmd)+not_if_out)
      
  if yes_if != None:
    (yes_if_ret, yes_if_out) = execute_command('su -c "{0} --config {1} {2}" - {3}'.format(hadoop_bin,hadoop_conf_dir,yes_if,hdfs_user),60)
    if yes_if_ret != 0:
      return (yes_if_ret, "cmd[ {0} ] success;\n".format(cmd)+yes_if_out)
          
  hdfs_cmd = 'su -c "{0} --config {1} {2}" - {3}'.format(hadoop_bin,hadoop_conf_dir,cmd,hdfs_user);
  (ret, out) = execute_command(hdfs_cmd,120)
  if ret == 0:
    label = "cmd[ {0} ]success;\n".format(cmd)+out
    return (ret, label)
  else:
    error_content = "cmd[ {0} ] fail;\n".format(cmd)+out
    raise Exception(ret, error_content)

def execute(parameters=None, host_name=None):
  """
  Returns a tuple containing the result code and a pre-formatted result label
  
  Keyword arguments:
  parameters (dictionary): a mapping of parameter key to value
  host_name (string): the name of this host where the alert is running
  """
  if parameters is None:
    return (('UNKNOWN', ['There were no parameters supplied to the script.']))
    
  web_address = "localhost:8088"
  yarn_user = "yarn"
  hdfs_user = "hdfs"
  
  if YARN_WEB_ADDRESS in parameters:
    web_address = parameters[YARN_WEB_ADDRESS]
  
  if YARN_USER in parameters:
    yarn_user = parameters[YARN_USER]
  
  # check the if yarn manager is started or not
  (ret, out) = execute_command('curl "{0}/ws/v1/cluster" 2>/dev/null'.format(web_address),60)
  if ret == 0:
    try:
      yarnCluster = json.loads(out)
      serviceState = yarnCluster['clusterInfo']['state']
      if serviceState.strip() != "STARTED":
        result_code = "CRITICAL"
        label = "resource manager state is not Started, state["+serviceState+"]"
        return ((result_code, [label]))
    except Exception,e:
      result_code = "CRITICAL"
      label = 'resource manager is down:'+str(e)
      return ((result_code, [label]))
  else:
    label = 'resource manager is down.'
    result_code = 'CRITICAL'
    return ((result_code, [label]))
    
  # check whether exists active nodeManager or not
  (ret, out) = execute_command('curl "{0}/ws/v1/cluster/metrics" 2>/dev/null'.format(web_address),60)
  if ret == 0:
    try:
      metrics = json.loads(out)
      activeNodeNum = metrics['clusterMetrics']['activeNodes']
      if activeNodeNum < 1:
        result_code = "CRITICAL"
        label = "there is not active nodemanager, active node number:"+str(activeNodeNum)
        return ((result_code, [label]))
    except Exception,e:
      result_code = "CRITICAL"
      label = 'parse active nodemanager num error:'+str(e)
      return ((result_code, [label]))
  else:
    label = 'curl cluster metrics error.'
    result_code = 'CRITICAL'
    return ((result_code, [label]))
  
  # run the wordcount mr
  dir = '/tmp'
  unique = str(uuid.uuid1()).replace("-","")
  service_check_output = dir+"/yarn_service_check_output"+unique
  service_check_input = dir+"/yarn_service_check_input"+unique
  
  test_dir_exists ="fs -test -e {0}".format(dir)
  create_dir_cmd = "fs -mkdir {0}".format(dir)
  chmod_command = "fs -chmod 777 {0}".format(dir)
  
  test_input_exists ="fs -test -e {0}".format(service_check_input)
  cleanup_input_cmd = "fs -rm {0}".format(service_check_input)
  create_input_cmd = "fs -put /etc/passwd {0}".format(service_check_input)
  
  test_output_exists ="fs -test -e {0}".format(service_check_output)
  cleanup_output_cmd = "fs -rm -r {0}".format(service_check_output)
  wordcount_command = "jar /usr/hdp/2.2.0.0-2041/hadoop-mapreduce/hadoop-mapreduce-examples.jar wordcount {0} {1}".format(service_check_input,service_check_output)  
  
  label = 'yarn service is good'
  result_code = 'OK'
  try:
    _executeHadoop(hdfs_user, create_dir_cmd, test_dir_exists)
    _executeHadoop(hdfs_user, chmod_command)
    
    _executeHadoop(hdfs_user, create_input_cmd)
    
    _executeHadoop(hdfs_user, wordcount_command)
  except Exception,e:
    result_code = "CRITICAL"
    label = 'yarn service is down:'+str(e)
  
  _executeHadoop(hdfs_user, cleanup_input_cmd, None, test_input_exists)
  _executeHadoop(hdfs_user, cleanup_output_cmd, None, test_output_exists)
  
  return ((result_code, [label]))
