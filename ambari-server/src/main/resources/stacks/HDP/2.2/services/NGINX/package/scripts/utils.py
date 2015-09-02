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
from resource_management import *
from resource_management.core.logger import Logger  

class utils:
  
  def exe(self, cmd):
    Logger.info("exec command: {0}".format(cmd))
    
    (status, output) = commands.getstatusoutput(cmd)
    if (status != 0):
      Logger.error("command exec error, return code = {0}".format(status))
      Logger.error(output)
      raise Fail()
    
    Logger.info(output)
    return output
  

  def kill_process(self, keyword):
    Logger.info("kill process with: {}".format(keyword))
    cmd = "ps aux | grep -E '" + keyword + "' | grep -v grep | awk '{print $2}'"
    result = self.exe(cmd)
    if result != None:
      pids = result.split()
      for pid in pids:
        self.exe("kill -9 " + pid)



  # check process by key word
  def check_process(self, keyword):
    Logger.info("check process with: {}".format(keyword))
    cmd = "ps aux | grep -E '" + keyword + "' | grep -v grep | cat"
    result = self.exe(cmd)
    if (result == ""):
      Logger.error("process {} not exist".format(keyword))
      raise ComponentIsNotRunning()

  # check process with "service xxx status" and key word
  def check_service_status(self, service, keyword):
    cmd = "service {0} status | grep -E '{1}'".format(service, keyword)
    Logger.info("run service check on {0} : ".format(service))
    (status, output) = commands.getstatusoutput(cmd)
    if (output == ""):
      Logger.error("service {0} not running".format(service))
      raise ComponentIsNotRunning() 

  # check process by user pid file
  def check_pid(self, pid_file):
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
   

  # generate check shell script
  def generate_check_script(self,env):
    import params
    
    print 'create env.sh'
    File(params.env_script,
         mode=0755,
         content=StaticFile('env.sh')
    )
  
    print 'create supports.sh'
    File(params.supports_script,
         mode=0755,
         content=StaticFile('supports.sh')
    )

   
  # generate certification shell script
  def generate_certification_script(self, env):
    import params

    
    print 'create supports.sh'
    File(params.supports_script,
         mode=0755,
         content=StaticFile('supports.sh')
    )

    print 'create certification.sh'
    File(params.certification_script,
         mode=0755,
         content=StaticFile('certification.sh')
     )


  def check_local_environment(self, env, role):
    import params
    self.generate_check_script(env)
    
    cmd = "bash -x {0} {1}".format(params.env_script, role)
    self.exe(cmd)

   
  def grant_local_privilege(self, env):
    import params
    self.generate_certification_script(env)
    cmd = "su gaia -c 'bash -x {0} '".format(params.certification_script)
    self.exe(cmd)

  def bind_hosts_port(self, hosts, port, sep, prefix = ""):
    address = ""
    for host in hosts:
      address += prefix + host.strip() + ":" + str(port) + sep

    #address = address[:-1] if len(address) > 0 else address
    return address

if __name__ == "__main__":
    cmd="bash -x /var/lib/ambari-agent/data/tmp/env.sh slave"
    utils().exe(cmd)
