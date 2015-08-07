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

import sys
import os
import commands
import socket
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.exceptions import Fail
from resource_management.core.logger import Logger  
import time

class utils:
  def get_local_ip(self):
    localip = socket.gethostbyname(socket.gethostname())
    return localip

  def get_local_name(self):
    localip = self.get_local_ip()
    localname = localip.replace(".", "_")
    return localname

  def get_gtm_name(self):
    ret = "gtm_" + self.get_local_name()
    Logger.info("utils.py: generator gtm name {0}".format(ret))
    return ret

  def get_coordinator_name(self):
    ret = "coordinator_" + self.get_local_name()
    Logger.info("utils.py: generator coordinator name {0}".format(ret))
    return ret
  
  def get_datanode_name(self):
    ret = "datanode_" + self.get_local_name()
    Logger.info("utils.py: generator datanode name {0}".format(ret))
    return ret
  
  def exe(self, cmd):
    Logger.info("exec command: {0}".format(cmd))
    #(status, output) = commands.getstatusoutput(cmd)
    status = os.system(cmd)
    if (status != 0):
      Logger.error("command exec error, return code = {0}".format(status))
      #raise Fail()
    #Logger.info(output)

  def check_process(self, pid_file):
    Logger.info("check process status")
    if not pid_file or not os.path.isfile(pid_file):
      Logger.info("pid file = '{0}' is not existed".format(pid_file))
      raise ComponentIsNotRunning()
    (ret, pid) = commands.getstatusoutput("awk 'NR==1{print}' " + pid_file)
    Logger.info("get pid = {0}, return code = {1}".format(pid, ret))
    cmd = "ps aux | awk '{print $2}' | grep -E '^" + pid + "$' | wc -l"
    (ret, num) = commands.getstatusoutput(cmd)
    if (num == 0):
      Logger.info("process {0} not exists".format(pid))
      raise ComponentIsNotRunning()
    else:
      Logger.info("process {0} exists".format(pid))

  def check_install(self, node_dir):
    Logger.info("checking path {0}".format(node_dir));
    if not os.path.isdir(node_dir):
      Logger.error("path {0} init failed".format(node_dir));
      raise Fail()
    Logger.info("path {0} init success".format(node_dir));

  def check_start(self, pid_file):
    Logger.info("check whether process start")
    time.sleep(1)
    try:
      self.check_process(pid_file)
    except ComponentIsNotRunning:
      Logger.error("process start failed")
      raise Fail()
    Logger.info("process start success")

  def check_stop(self, pid_file):
    Logger.info("check whether process stop")
    try:
      self.check_process(pid_file)
    except ComponentIsNotRunning:
      Logger.info("process stop success")
      return
    Logger.error("process stop failed")
    raise Fail()

  def syncCluster(self, coors, datanodes, coord_port, datanode_port, host, sql_str):
    for coor in coors:
      name = "coordinator_" + coor.replace(".", "_")
      sql = "CREATE NODE {0} WITH (TYPE = '{1}', HOST = '{2}', PORT = {3});".format(name, "coordinator", coor, coord_port)
      cmd = sql_str.format(host, coord_port, sql)
      Logger.info(cmd)
      (ret, out) = commands.getstatusoutput(cmd)
      if (ret == 0 and out.rfind("CREATE NODE") != -1):
        # insert record
        Logger.info("coordinator {0} create success on coordinator {1}".format(name, host))
      elif (ret != 0 and out.rfind(name) != -1):
        # update record
        Logger.info("coordinator {0} exist on coordinator {1}, updating coordinator ...".format(name, host))
        update_cmd = cmd.replace("CREATE", "ALTER")
        Logger.info(update_cmd)
        (ret, out) = commands.getstatusoutput(update_cmd)
        if (ret == 0 and out.rfind("ALTER NODE") != -1):
          Logger.info("coordinator {0} update success on coordinator {1}".format(name, host))
        elif (ret != 0 and out.rfind(name) != -1):
          # update coordinator self
          # update pgxc_node set node_host = 'local', node_port = 5000 WHERE node_name = 'datanode_10_151_0_123';
          self_sql = "update pgxc_node set node_host = '{0}', node_port = {1} WHERE node_name = '{2}';".format(host, datanode_port, name)
          self_cmd = sql_str.format(coor, coord_port, self_sql)
          Logger.info(self_cmd)
          (ret, out) = commands.getstatusoutput(self_cmd)
          if (ret == 0 and out.rfind("UPDATE 1") != -1):
            Logger.info("coordinator {0} update success on coordinator {1} itself".format(name, host))
          else:
            Logger.error("coordinator {0} update failed on coordinator {1} itself".format(name, host))
            raise Fail()
        else:
          Logger.error("coordinator {0} update failed on coordinator {1}".format(name, host))
          raise Fail()
      else:
        Logger.error("coordinator {0} create failed on coordinator {1}".format(name, host))
        raise Fail()

    for datanode in datanodes:
      name = "datanode_" + datanode.replace(".", "_")
      sql = "CREATE NODE {0} WITH (TYPE = '{1}', HOST = '{2}', PORT = {3});".format(name, "datanode", datanode, datanode_port)
      cmd = sql_str.format(host, coord_port, sql)
      Logger.info(cmd)
      (ret, out) = commands.getstatusoutput(cmd)
      if (ret == 0 and out.rfind("CREATE NODE") != -1):
        # insert record
        Logger.info("datanode {0} create success on coordinator {1}".format(name, host))
      elif (ret != 0 and out.rfind(name) != -1):
        # update record
        Logger.info("datanode {0} exist on coordinator {1}, updating datanode ...".format(name, host))
        update_cmd = cmd.replace("CREATE", "ALTER")
        Logger.info(update_cmd)
        (ret, out) = commands.getstatusoutput(update_cmd)
        if (ret == 0 and out.rfind("ALTER NODE") != -1):
          Logger.info("datannode {0} update success on coordinator {1}".format(name, host))
        else:
          Logger.error("datanode {0} update failed on coordinator {1}".format(name, host))
          raise Fail()
      else:
        Logger.error("datanode {0} create failed on coordinator {1}".format(name, host))
        raise Fail()

if __name__ == "__main__":
  utils().exe("pwd")
  utils().get_local_name()
  utils().get_gtm_name()
  utils().get_coordinator_name()
  utils().get_datanode_name()
  utils().check_install("/")
  utils().check_stop("test")
  utils().check_start("test")
  pgxz_path = "/usr/local/pgxz/bin"
  user_name = "pgxz"
  psql = "/usr/local/pgxz/bin/psql"
  sql_str = "cd {0}; su {1} -c \"{2}\"".format(pgxz_path, user_name, "{0} -h {1} -p {2} postgres -c \\\"{3}\\\"").format(psql, "{0}", "{1}", "{2}")
  utils().syncCluster(["127.0.0.0","127.0.0.1"], ["127.0.0.2","127.0.0.3"], 5434, 5433, "10.151.0.12", sql_str)

