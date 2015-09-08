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
from resource_management.core.resources import Package

class Toolkit():

  # run shell command
  # cmd : command to run
  # ignoreFail : default as False, raise Fail when command return not 0
  # return : return output of command when ignoreFail is False, or (code, output)
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

  # remove dir, when it contains links, remove links' targets together
  # dir : directory to remove
  # return : None
  @staticmethod
  def remove_links_dir(dir):
    Logger.info("remove links directory: {0}".format(dir))
    cmd = "DIR={0}; for x in $(find $DIR -type l); do rm -rf $(readlink -f $x); done; rm -rf $DIR".format(dir)
    Toolkit.exe(cmd)

  # convert var to array, if var is already list, return itself
  # elem : var
  # return : list of var
  @staticmethod
  def to_array(elem):
    elems = []
    if type(elem) == list:
      elems = elem
    else:
      elems.append(elem)
    return elems

  # install yum package or packages
  # package : yum package's or packages' name
  # return : None
  @staticmethod
  def yum_install(package):
    packages = Toolkit.to_array(package)
    for pack in packages:
      Logger.info("installing yum package {0}".format(pack))
      Package(pack)

  # remove yum package or packages
  # package : yum package's or packages' name
  # return : None
  @staticmethod
  def yum_remove(package):
    packages = Toolkit.to_array(package)
    for pack in packages:
      Logger.info("removing yum package {0}".format(pack))
      Package(pack, action = "remove")

  # uninstall service, including yum package and install directory
  # package : yum package's or packages' name
  # service : service name
  # return : None
  @staticmethod
  def uninstall_service(package, service):
    service = service.lower()
    Logger.info("uninstalling service {0}".format(service))
    Toolkit.yum_remove(package)
    paths = ["/opt", "/etc", "/data", "/var/log"]
    for path in paths:
      path += "/" + service
      Toolkit.remove_links_dir(service)

if __name__ == '__main__':
  # export PYTHONPATH=$PYTHONPATH:/usr/lib/python2.6/site-packages
  from resource_management.core import Environment
  Environment()
  Toolkit.exe("ls")