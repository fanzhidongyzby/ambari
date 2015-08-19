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
from ambari_commons.constants import AMBARI_SUDO_BINARY
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management.libraries.functions.default import default
from resource_management.libraries.script import Script
from resource_management.libraries.functions import default, format

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

def format(str, isItemDigit = False):
  if(str == None or str.strip() == ""):
    return ""
  items = str.strip().split(",")
  result = ""
  for item in items:
    if isItemDigit:
      result += "  -  {0} \n".format(item.strip())
    else:
      result += "  -  \"{0}\" \n".format(item.strip())
  return result
  
def formatArray(items, isItemDigit = False):
  if(items == None or len(items) == 0):
    return ""
  result = ""
  for item in items:
    if isItemDigit:
      result += "  -  {0} \n".format(item)
    else:
      result += "  -  \"{0}\" \n".format(item)
  return result

#jstorm params
conf_dir = "/usr/local/jstorm/conf"
root_dir = "/usr/local/jstorm"
bin_dir = "/usr/local/jstorm/bin"

#jstorm-env.xml
storm_user = config['configurations']['jstorm-env']['jstorm.user']
storm_group = config['configurations']['jstorm-env']['jstorm.group']
storm_env_sh_template = config['configurations']['jstorm-env']['content']
java64_home = config['hostLevelParams']['java_home']
storm_env_sh_template = storm_env_sh_template.replace("{{java64_home}}",java64_home)

#storm-yaml.xml
java_library_path = config['configurations']['jstorm-yaml']['java.library.path']
local_dir = config['configurations']['jstorm-yaml']['jstorm.local.dir']
#storm_zookeeper_servers = format(config['configurations']['jstorm-yaml']['jstorm.zookeeper.servers'])
storm_zookeeper_servers = formatArray(config['clusterHostInfo']['zookeeper_hosts'])
#storm_zookeeper_port = config['configurations']['jstorm-yaml']['jstorm.zookeeper.port']
storm_zookeeper_port = config['configurations']['zoo.cfg']['clientPort']
storm_zookeeper_root = config['configurations']['jstorm-yaml']['storm.zookeeper.root']
ui_port = config['configurations']['jstorm-yaml']['ui.port']
logviewer_port = config['configurations']['jstorm-yaml']['logviewer.port']

#drpc_servers = format(config['configurations']['jstorm-yaml']['drpc.servers'])
storm_scheduler = config['configurations']['jstorm-yaml']['storm.scheduler']
storm_messaging_transport = config['configurations']['jstorm-yaml']['storm.messaging.transport']
supervisor_slots_ports = format(config['configurations']['jstorm-yaml']['supervisor.slots.ports'], True)

#script
check_status_script = "{0}/checkStatus.sh".format(tmp_dir)
