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

import json
import datetime
import shlex
import subprocess
import time
import utils

def executeCommand(cmdstring, timeout=None, shell=True):
  if shell:
    cmdstring_list = cmdstring
  else:   
    cmdstring_list = shlex.split(cmdstring)
  if timeout:
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
	
  sub = subprocess.Popen(cmdstring_list, stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE,shell=shell)
	
  while sub.poll() is None:
    time.sleep(0.1)
    if timeout:
      if end_time <= datetime.datetime.now():
        return 1,"Timeout:%s"%cmdstring
	    
  stdout,stderr = sub.communicate()
  return sub.returncode,stdout+stderr
  
def _executeHadoop(hdfs_user, cmd, not_if=None, yes_if=None):
  hadoop_bin = "/usr/bin/hadoop"
  hadoop_conf_dir = "/etc/hadoop/conf"
  if not_if != None:
    (not_if_ret, not_if_out) = executeCommand('su -c "{0} --config {1} {2}" - {3}'.format(hadoop_bin,hadoop_conf_dir,not_if,hdfs_user),60)
    if not_if_ret == 0:
      return (not_if_ret, "cmd[ {0} ] success;".format(cmd)+not_if_out)
      
  if yes_if != None:
    (yes_if_ret, yes_if_out) = executeCommand('su -c "{0} --config {1} {2}" - {3}'.format(hadoop_bin,hadoop_conf_dir,yes_if,hdfs_user),60)
    if yes_if_ret != 0:
      return (yes_if_ret, "cmd[ {0} ] success;\n".format(cmd)+yes_if_out)
          
  hdfs_cmd = 'su -c "{0} --config {1} {2}" - {3}'.format(hadoop_bin,hadoop_conf_dir,cmd,hdfs_user);
  (ret, out) = executeCommand(hdfs_cmd,60)
  if ret == 0:
    label = "cmd[ {0} ]success;\n".format(cmd)+out
    return (ret, label)
  else:
    error_content = "cmd[ {0} ] fail;\n".format(cmd)+out
    raise Exception(ret, error_content)

class HiveDirInit():
  def createHiveDir(self):
    hdfs_user = "hdfs"
    hive_root="/data/hive"
    test_hive_root_exists ="fs -test -e {0}".format(hive_root)
    create_hive_root = "fs -mkdir -p {0}".format(hive_root)
		
    create_hive_import = "fs -mkdir {0}/import".format(hive_root)
    test_hive_import_exists ="fs -test -e {0}/import".format(hive_root)
    create_hive_export = "fs -mkdir {0}/export".format(hive_root)
    test_hive_export_exists ="fs -test -e {0}/export".format(hive_root)
    create_hive_check = "fs -mkdir {0}/check".format(hive_root)
    test_hive_check_exists ="fs -test -e {0}/check".format(hive_root)
		
    chmod_command = "fs -chmod -R 755 {0}".format(hive_root)
    chown_command = "fs -chown -R hive:hive {0}".format(hive_root)
	
    try:
      _executeHadoop(hdfs_user, create_hive_root, test_hive_root_exists)
      _executeHadoop(hdfs_user, create_hive_import, test_hive_import_exists)
      _executeHadoop(hdfs_user, create_hive_export, test_hive_export_exists)
      _executeHadoop(hdfs_user, create_hive_check, test_hive_check_exists)
		  
      _executeHadoop(hdfs_user, chmod_command)
      _executeHadoop(hdfs_user, chown_command)
    except Exception,e:
      print "[WARNING]:"+str(e)
