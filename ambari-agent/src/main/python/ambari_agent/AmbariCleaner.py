#!/usr/bin/env python
import os
import sys
import commands
import socket
import fileinput


class AmbariCleaner:

  repo_name_key = "repo_name"
  directory_key = "directory"

  def __init__(self):
    self.onServer = self.isServerHost()
    self.dirs = self.readServiceInfo(self.directory_key)
    self.repos = self.readServiceInfo(self.repo_name_key)

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

  def run_cmd(self,cmd):
    print cmd
    (ret, output) = commands.getstatusoutput(cmd)
    print output
    print ret
    return output

  def stop_agent(self):
    cmd = "sudo ambari-agent stop"
    self.run_cmd(cmd)


  def remove_services_installed_rpm(self):
    if not self.onServer:
      for repo in self.repos:
        cmd = "yum list installed 2>/dev/null |grep " + repo + " | xargs yum remove -y"
        self.run_cmd(cmd)

  def yum_clean(self):
    print "yum clean all"
    cmd = "sudo yum clean all"
    (ret, output) = commands.getstatusoutput(cmd)
    print output
    print ret


  def remove_yum_repo(self):
    if not self.onServer:
      cmd ="rm /etc/yum.repos.d/*.repo"
      self.run_cmd(cmd)

  def release_resources(self):
    self.run_cmd("umount /gaia/docker/var/lib/docker/devicemapper")

  def remove_dir(self):
    self.release_resources()
    for dir in self.dirs:
      cmd = "sudo rm -rf {}".format(dir)
      self.run_cmd(cmd)



  def main(self):
    # stop agent first
    self.stop_agent()

    # remove yum rpms
    self.remove_services_installed_rpm()
    self.yum_clean()
    self.remove_yum_repo()

    # remove user defined dirs
    self.remove_dir()

if __name__ == '__main__':
   obj = AmbariCleaner()
   obj.main()
