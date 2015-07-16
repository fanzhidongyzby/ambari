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

import commands
import json
import datetime

LABEL = 'Last Checkpoint: [{h} hours, {m} minutes, {tx} transactions]'

LHOTSE_SERVICE_PORT = '{{lhotse-service/listen.port}}'
LHOTSE_DEFAULT_TASKID = '{{lhotse-service/lhotse.default.taskId}}'

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (LHOTSE_SERVICE_PORT, LHOTSE_DEFAULT_TASKID)
  

def execute(parameters=None, host_name=None):
  """
  Returns a tuple containing the result code and a pre-formatted result label

  Keyword arguments:
  parameters (dictionary): a mapping of parameter key to value
  host_name (string): the name of this host where the alert is running
  """

  if parameters is None:
    return (('UNKNOWN', ['There were no parameters supplied to the script.']))

  host = host_name
  port = 9010
  taskId = parameters[LHOTSE_DEFAULT_TASKID]

  if LHOTSE_SERVICE_PORT in parameters:
    port = parameters[LHOTSE_SERVICE_PORT]
    
  if taskId == "{{lhotse-service/lhotse.default.taskId}}":
    taskId = "20150602143023086"
  
  today = datetime.date.today()
  yestory = today - datetime.timedelta(days=1)
  today = today.strftime("%Y%m%d000000")
  yestory = yestory.strftime("%Y%m%d000000")
  cmd = 'curl "' + host + ':' + str(port) + '/LService/QueryTaskRun_new?taskId=' + str(taskId) + '&dateFrom='+yestory+'&dateTo='+today+'" 2>/dev/null'
  (ret, out) = commands.getstatusoutput(cmd)
  
  if ret == 0:
    label = 'lhotse service is running.'
    result_code = 'OK'
    try:
      lhotseResult = json.loads(out)
      serviceState = lhotseResult['state']
      if serviceState.strip() != "success":
        result_code = "CRITICAL"
        label = "lhotse service runs failed, state["+serviceState+"]"
    except Exception,e:
      result_code = "CRITICAL"
      label = 'lhotse service is down[{0}]:{1}'.format(cmd, str(e))
  else:
    result_code = 'CRITICAL'
    label = 'lhotse service is down[{0}].'.format(cmd)

  return ((result_code, [label]))