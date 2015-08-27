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
import commands
import time
import datetime
import shlex
import subprocess

LABEL = 'Last Checkpoint: [{h} hours, {m} minutes, {tx} transactions]'

ZOOKEEPER_CONNECT = '{{kafka-broker/zookeeper.connect}}'
PORT = '{{kafka-broker/port}}'

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (PORT, ZOOKEEPER_CONNECT)
  
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

  zk_connect = "localhost:2181"
  port = 6667
  
  if PORT in parameters:
    port = parameters[PORT]
  if ZOOKEEPER_CONNECT in parameters:
    zk_connect = parameters[ZOOKEEPER_CONNECT]
    
  topic = "ambari_kafka_service_check"
  jarPath = "/var/lib/ambari-agent/cache/common-services/KAFKA/0.8.1.2.2/package/files/kafka_service_check.jar:/usr/hdp/2.2.0.0-2041/kafka/libs/*"
    
  producer_cmd = "/usr/jdk64/jdk1.7.0_67/bin/java -cp "+jarPath+" kafka.KafkaProducer "+topic+" "+host_name+":"+port
  consumer_cmd = "/usr/jdk64/jdk1.7.0_67/bin/java -cp "+jarPath+" kafka.KafkaConsumer "+topic+" "+zk_connect
  
  result_code = 'OK'
  label = 'kafka service is running.'
  
  try:
    _execute_command(producer_cmd,90)
    _execute_command(consumer_cmd,90)
  except Exception,e:
    result_code = "CRITICAL"
    label = 'kafka service runs failed:'+str(e)
  
  return ((result_code, [label]))
