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

__all__ = ["Toolkit"]

import commands
from resource_management.core.exceptions import Fail
from resource_management.core.logger import Logger

class Toolkit():

  @staticmethod
  def exe(cmd, ignoreFail = False):
    Logger.info("exec command: {0}".format(cmd))

    (status, output) = commands.getstatusoutput(cmd)
    if not ignoreFail:
      if (status != 0):
        Logger.error("command exec error, return code = {0}".format(status))
        Logger.error(output)
        raise Fail()

      Logger.info(output)
      return output
    else:
      Logger.info(output)
      return (status == 0, output)

  @staticmethod
  def remove_links_dir(dir):
    Logger.info("remove links directory: {0}".format(dir))
    cmd = "DIR={0}; for x in $(find $DIR -type l); do rm -rf $(readlink -f $x); done; rm -rf $DIR".format(dir)
    Toolkit.exe(cmd)

if __name__ == '__main__':
  pass