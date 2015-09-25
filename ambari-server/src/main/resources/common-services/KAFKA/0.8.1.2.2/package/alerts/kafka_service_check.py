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

from resource_management import *

LABEL = 'Last Checkpoint: [{h} hours, {m} minutes, {tx} transactions]'

ZOOKEEPER_CONNECT = '{{kafka-broker/zookeeper.connect}}'
PORT = '{{kafka-broker/port}}'

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (PORT, ZOOKEEPER_CONNECT)
    
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
    
  topic = "tencent_kafka_service_check"
  jarPath = "/var/lib/ambari-agent/cache/common-services/KAFKA/0.8.1.2.2/package/files/kafka_service_check.jar:/usr/hdp/2.2.0.0-2041/kafka/libs/*"
    
  producer_cmd = "/usr/jdk64/jdk1.7.0_67/bin/java -cp "+jarPath+" kafka.KafkaProducer "+topic+" "+host_name+":"+port
  consumer_cmd = "/usr/jdk64/jdk1.7.0_67/bin/java -cp "+jarPath+" kafka.KafkaConsumer "+topic+" "+zk_connect
  
  result_code = 'OK'
  label = 'kafka service is running.'
  
  try:
    Toolkit.execute_shell(producer_cmd,timeout=90)
    Toolkit.execute_shell(consumer_cmd,timeout=90)
  except Exception,e:
    result_code = "CRITICAL"
    label = 'kafka service runs failed:'+str(e)
  
  return ((result_code, [label]))
