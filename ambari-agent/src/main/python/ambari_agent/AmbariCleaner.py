#!/usr/bin/env python
import os
import sys
import commands
import socket
import fileinput

repo_name_key = "repo_name"
directory_key = "directory"
class AmbariCleaner:
  def eraseagent(self):
    print "ambari-agent stop"
    cmd = "sudo ambari-agent stop"
    self.run_cmd(cmd)

    print "yum erase agent"
    cmd = "sudo yum erase -y ambari-agent*"
    self.run_cmd(cmd)

  def erasemetrics(self):
    print "yum erase metrics"
    cmd = "sudo yum erase -y ambari-metrics*"
    self.run_cmd(cmd)

  def isServerHost(self):
    print "get server host"
    cmd = "cat  /etc/ambari-agent/conf/ambari-agent.ini|grep hostname|awk -F '=' '{print $2}'"
    serverhost =  self.run_cmd(cmd)

    print "get local host"
    localhost = socket.gethostname()

    if localhost == serverhost:
       return True
    else:
       return False

  def remove_dir(self):
    dirs = self.readServiceInfo(directory_key)
    for dir in dirs:
      cmd = "sudo rm -rf {}".format(dir)
      self.run_cmd(cmd)
    return

    cmd = "sudo rm -rf /etc/ambari*"
    self.run_cmd(cmd)

  def remove_services_installed_rpm(self):

    #get all installed rpm
    repos = self.readServiceInfo(repo_name_key)
    for repo in repos:
      cmd = "yum list installed 2>/dev/null |grep " + repo + "| xargs yum remove -y"
      self.run_cmd(cmd)

    return

  def yum_clean(self):
    print "yum clean all"
    cmd = "sudo yum clean all"
    (ret, output) = commands.getstatusoutput(cmd)
    print output
    print ret
  
  def run_cmd(self,cmd):
    print cmd
    (ret, output) = commands.getstatusoutput(cmd)
    print output
    print ret
    return output

  def readServiceInfo(self,key):
    res = []
    findkey = False

    for line in fileinput.input("/usr/lib/python2.6/site-packages/ambari_agent/service_remove.txt"):
      print(line)
      line = line.strip()
      if ( line=="" ):
         continue

      if (findkey):
        if(line.find("[") < 0):
           print("add list: " + line)
           res.append(line)
        else:
          break

      elif (line.find(key)>=0) :
         findkey = True

    fileinput.close()
    return res

  def main(self):
    self.remove_services_installed_rpm()
    self.remove_dir()
    self.yum_clean()

if __name__ == '__main__':
   obj = AmbariCleaner()
   obj.main()
