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

REDIS_PORT = '{{redis-env/redis_port}}'
SMOKE_USER = '{{cluster-env/smokeuser}}'

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (REDIS_PORT, SMOKE_USER)

def execute(parameters=None, host_name=None):
  """
  Returns a tuple containing the result code and a pre-formatted result label
  
  Keyword arguments:
  parameters (dictionary): a mapping of parameter key to value
  host_name (string): the name of this host where the alert is running
  """
  if parameters is None:
    return (('UNKNOWN', ['There were no parameters supplied to the script.']))
  
  smoke_user = "ambari-qa"
  redis_port = 6379

  if SMOKE_USER in parameters:
      smoke_user = parameters[SMOKE_USER]

  if REDIS_PORT in parameters:
      redis_port = parameters[REDIS_PORT]

  label = 'Redis service is good'
  result_code = 'OK'
  try:
    testRedisCmd = '/usr/bin/redis-cli -p {0} set foo bar'.format(redis_port)
    Execute(testRedisCmd,
        logoutput=True,
        try_sleep=3,
        tries=1,
        user=smoke_user
    )
  except Exception,e:
    result_code = "CRITICAL"
    label = 'redis service is unavailable:'+str(e)
  
  return ((result_code, [label]))