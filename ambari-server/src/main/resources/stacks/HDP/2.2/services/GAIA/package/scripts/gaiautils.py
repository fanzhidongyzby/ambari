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

import sys
import commands

class gaiautils:

    def sub_dict(self,form_dict, sub_keys, default=None):
       return dict([(k, form_dict.get(k.strip(), default)) for k in sub_keys.split(',')])

    def read_cpuinfo(self):
      cpu_stat = []
      with open('/proc/cpuinfo', 'r') as f:
        data = f.read()
        for line in data.split('\n\n'):
            cpu_stat.append(line)
      return cpu_stat[-2]

    def get_local_cpunum(self):
      data = self.read_cpuinfo()
      cpu_info = {}
      for i in data.splitlines():
        k, v = [x.strip() for x in i.split(':')]
        cpu_info[k] = v
       
      cpu_info['physical id'] = str(int(cpu_info.get('physical id')) + 1)

      cpuinfo = self.sub_dict(cpu_info, 'model name,physical id,cpu cores')
      return int(cpuinfo.get("cpu cores",None))
    
   
    def get_local_memorytotal(self):
      mem_info = {}
      with open('/proc/meminfo', 'r') as f:
        data = f.readlines()
        for i in data:
            k, v = [x.strip() for x in i.split(':')]
            mem_info[k] = int(v.split()[0])
      meminfo = self.sub_dict(mem_info, 'MemTotal,SwapTotal')
      return int(meminfo.get("MemTotal",0)/1024)

    def get_first_data(self):
      cmd = "df | awk '{print $6}' | grep /data" 
      (code, output) = commands.getstatusoutput(cmd) 
      if code == 0:
        local_disks = output.split()
        if len(local_disks) > 0:
          return local_disks[0]

      return "/data"

    def get_local_dirs(self, subdir):
      DEFAULT_LOCAL_DIRS = ["/data"]
      local_disks = DEFAULT_LOCAL_DIRS
    
      cmd = "df | awk '{print $6}' | grep /data" 
      (code, output) = commands.getstatusoutput(cmd) 
      if code == 0:
        local_disks = output.split()
    
      local_dirs = ""
      for disk in local_disks:
        local_dirs += disk + subdir + ","
    
      return local_dirs[:-2]


    def bind_hosts_port(self, hosts, port, sep, prefix = ""):
      address = ""
      for host in hosts:
        address += prefix + host.strip() + ":" + str(port) + sep

      address = address[:-2] if len(address) > 0 else address

      return address


if  __name__ == "__main__":
    a = gaiautils().get_local_cpunum()
    print(a)
    b = gaiautils().get_local_memorytotal()
    print(b)
    print gaiautils().get_local_dirs("/yarnenv/local")
    print gaiautils().get_first_data()
    print gaiautils().bind_hosts_port(["123", "345"], 9090, ";")
    print gaiautils().bind_hosts_port(["123", "345"], 9090, ";", "http://")
