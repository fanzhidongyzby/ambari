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

Ambari Agent

"""

from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.logger import Logger
from resource_management.core import shell
from resource_management.core import sudo
__all__ = ["check_process_status"]

import os

def check_process_status(pid_file):
  """
  Function checks whether process is running.
  Process is considered running, if pid file exists, and process with
  a pid, mentioned in pid file is running
  If process is not running, will throw ComponentIsNotRunning exception

  @param pid_file: path to service pid file
  """
  if not pid_file or not os.path.isfile(pid_file):
    raise ComponentIsNotRunning()
  
  try:
    pid = int(sudo.read_file(pid_file))
  except:
    Logger.debug("Pid file {0} does not exist".format(pid_file))
    raise ComponentIsNotRunning()

  code, out = shell.call(["ps","-p", str(pid)])
  
  if code:
    Logger.debug("Process with pid {0} is not running. Stale pid file"
              " at {1}".format(pid, pid_file))
    raise ComponentIsNotRunning()
  pass
