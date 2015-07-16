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

GOLDENEYE_DATABASE_USER = '{{goldeneye-database/goldeneye.db.username}}'
GOLDENEYE_DATABASE_PASSWORD = '{{goldeneye-database/goldeneye.db.password}}'

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (GOLDENEYE_DATABASE_USER, GOLDENEYE_DATABASE_PASSWORD)
  

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
  port = '3306'
  user = 'goldeneye'
  psw = 'goldeneye'

  if GOLDENEYE_DATABASE_USER in parameters:
    user = parameters[GOLDENEYE_DATABASE_USER]
  if GOLDENEYE_DATABASE_PASSWORD in parameters:
    psw = parameters[GOLDENEYE_DATABASE_PASSWORD]

  cmd = 'mysql -h"' + host + '" -P"' + port + '" -u"' + user + '" -p"' + psw + '" -e"show databases"'
  (ret, out) = commands.getstatusoutput(cmd)

  if ret == 0:
      label = 'goldeneye database process is running.'
      result_code = 'OK'
  else:
      label = 'goldeneye database process is down.'
      result_code = 'CRITICAL'

  return ((result_code, [label]))