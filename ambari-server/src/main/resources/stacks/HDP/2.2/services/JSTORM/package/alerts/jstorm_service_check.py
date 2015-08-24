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

LABEL = 'Last Checkpoint: [{h} hours, {m} minutes, {tx} transactions]'

UI_PORT = '{{jstorm-yaml/ui.port}}'
SLOTS = '{{jstorm-yaml/supervisor.slots.ports}}'

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (UI_PORT, SLOTS)
    
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
  ui_port = 8080
  slots_num = 1
  
  if UI_PORT in parameters:
    ui_port = parameters[UI_PORT]
  if SLOTS in parameters:
    slots_num = len(parameters[SLOTS].split(","))
  
  api = 'curl "http://{0}:{1}/api/v1/cluster/summary" 2>/dev/null'.format(host, ui_port)
  (ret, out) = commands.getstatusoutput(api)
  
  if ret == 0:
    label = 'jstorm service is running.'
    result_code = 'OK'
    try:
      summary = json.loads(out)
      freeSlots = summary['slotsFree']
      if freeSlots <= slots_num:
        result_code = "WARNING"
        label = "jstorm is busy now, free slots:{0}".format(freeSlots)
    except Exception,e:
      result_code = "CRITICAL"
      label = '{0} parse error:{1}'.format(out,str(e))
  else:
    result_code = 'CRITICAL'
    label = 'jstorm service is down[{0}].'.format(api)
  
  return ((result_code, [label]))
