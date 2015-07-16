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

LABEL = 'Last Checkpoint: [{h} hours, {m} minutes, {tx} transactions]'

LHOTSE_DATABASE_USER = '{{lhotse-database/lhotse.db.username}}'
LHOTSE_DATABASE_PASSWORD = '{{lhotse-database/lhotse.db.password}}'
LHOTSE_DATABASE_PORT = 3306

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (LHOTSE_DATABASE_USER, LHOTSE_DATABASE_PASSWORD)
  

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
  port = LHOTSE_DATABASE_PORT
  user = 'lhotse'
  psw = 'lhotse'

  if LHOTSE_DATABASE_USER in parameters:
    user = parameters[LHOTSE_DATABASE_USER]
  if LHOTSE_DATABASE_PASSWORD in parameters:
    psw = parameters[LHOTSE_DATABASE_PASSWORD]

  cmd = 'mysql -h"' + host + '" -P"' + str(port) + '" -u"' + user + '" -p"' + psw + '" -e"show databases"'
  (ret, out) = commands.getstatusoutput(cmd)

  if ret == 0:
      label = 'lhotse database process is running.'
      result_code = 'OK'
  else:
      label = 'lhotse database process is down.'
      result_code = 'CRITICAL'

  return ((result_code, [label]))