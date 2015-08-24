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

USER = 'postgres'
PORT = '{{pgxzm_global/pgxzm.database.port}}'

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (PORT)
  
def execute(parameters=None, host_name=None):
  """
  Returns a tuple containing the result code and a pre-formatted result label

  Keyword arguments:
  parameters (dictionary): a mapping of parameter key to value
  host_name (string): the name of this host where the alert is running
  """

  if parameters is None:
    return (('UNKNOWN', ['There were no parameters supplied to the script.']))

  user = USER
  port = "5432"

  if PORT in parameters:
    port = parameters[PORT]

  cmd = 'psql -p"' + str(port) + '" -U"' + user + '" -c "\l"'
  (ret, out) = commands.getstatusoutput(cmd)

  if ret == 0:
    label = 'pgxzm database process is running.'
    result_code = 'OK'
  else:
    label = 'pgxzm database process is down.'
    result_code = 'CRITICAL'

  return ((result_code, [label]))