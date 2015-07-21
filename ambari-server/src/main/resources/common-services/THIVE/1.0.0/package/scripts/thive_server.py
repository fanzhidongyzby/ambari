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
from configinit import configinit

class Master(Script):
  def install(self, env):
    import params
    env.set_params(params)

    excludePackage = ['plclient*','postgresql93*']

    self.install_packages(env,excludePackage)
    
    self.configure(env)

    configinit().init_checkstatus_script()

  def start(self, env):
    import params
    env.set_params(params)

    print 'refresh configs'
    self.configure(env)

    print 'start the thive';
    cmd = format("su hdfs -c '/usr/local/thive/dist/bin/start-server.sh {thive_port}'")
    
    (ret, output) = commands.getstatusoutput(cmd)
    print "[ret]"
    print ret
    print "[output]"
    print output


  def stop(self, env):
    import params
    env.set_params(params)

    print 'Stop the thive';
    cmd = format("su hdfs -c '/usr/local/thive/dist/bin/stop-server.sh {hive_process_keyword}'")

    (ret, output) = commands.getstatusoutput(cmd)
    print "[ret]"
    print ret
    print "[output]"
    print output
   
    

  def configure(self, env):
    print "update thive configs"
    configinit().update_thive_config()


     
  def status(self, env):
    import params
    env.set_params(params)

    print 'Status of thive master'

    cmd = format("bash -x {checkstatus_script} {hive_process_keyword} 1")
    
    (ret, output) = commands.getstatusoutput(cmd)
    print ret
    print output

    if ret == 0:
      print "hive server is running"
    else:
      raise ComponentIsNotRunning()

if __name__ == "__main__":
  Master().execute()

