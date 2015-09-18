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

import collections
import os
import platform
from ambari_commons.os_family_impl import OsFamilyFuncImpl, OsFamilyImpl
from ambari_commons import OSConst


MAX_USED_PERCENT = 85
WRAN_USED_PERCENT = 70

def _get_disks_space():
  diskInfos = os.popen("df -h").read().split("\n")
  
  firstLineContinue = True
  errorInfo = []
  warnInfo = []
  diskInfo = []

  for info in diskInfos :
    if firstLineContinue:
      firstLineContinue = False
      continue

    info = info.strip()
    if(info == ""):
      continue
    items = info.split()
    usedPercent = float(items[4].replace("%",""))
    if(usedPercent >= MAX_USED_PERCENT):
      errorInfo.append("{0} Total:[{1}] Used:[{2} {3}]".format(items[5], items[1],items[2],items[4]))
    elif(usedPercent >= WRAN_USED_PERCENT):
      warnInfo.append("{0} Total:[{1}] Used:[{2} {3}]".format(items[5], items[1],items[2],items[4]))
    else:
      diskInfo.append("{0} Total:[{1}] Used:[{2} {3}]".format(items[5], items[1],items[2],items[4]))
  return (errorInfo, warnInfo, diskInfo)
    
    
def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return None

def execute(parameters=None, host_name=None):
  """
  Performs advanced disk checks under Linux
  Returns a tuple containing the result code and a pre-formatted result label

  Keyword arguments:
  parameters (dictionary): a mapping of parameter key to value
  host_name (string): the name of this host where the alert is running
  """
  result_code = "CRITICAL"
  label = ["Unknow Disk Space"]
  infos = _get_disks_space()
  if len(infos[0]) > 0:
    result_code = "CRITICAL"
    label = infos[0]
  elif len(infos[1]) > 0:
    result_code = "WARNING"
    label = infos[1]
  else:
    result_code = "OK"
    label = infos[2]
    

  return result_code, ["; ".join(label)]

if __name__ == '__main__':
    print _get_disks_space()