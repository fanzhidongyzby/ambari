#!/usr/bin/env python
import os
import sys
import commands
import socket
import fileinput
import time


class AmbariCleaner:

  repo_name_key = "repo_name"
  directory_key = "directory"

  def __init__(self):
    self.logfile = open("/tmp/clean_agent.log", "a")
    self.onServer = self.isServerHost()
    self.dirs = self.readServiceInfo(self.directory_key)
    self.repos = self.readServiceInfo(self.repo_name_key)

  def __del__(self):
    self.logfile.close()

  def log(self, str):
    now = time.strftime("%H:%M:%S", time.localtime())
    self.logfile.write("[{0}] {1}\n".format(now, str))

  def isServerHost(self):
    cmd = "cat /etc/ambari-agent/conf/ambari-agent.ini | grep hostname | awk -F '=' '{print $2}'"
    (ret, serverhost) = self.run_cmd(cmd)

    localhost = socket.gethostname()
    self.log("localhost is '{0}', serverhost is '{1}'".format(localhost,serverhost))

    if localhost == serverhost:
      return True
    else:
      return False

  def readServiceInfo(self,key):
    res = []
    findkey = False

    for line in fileinput.input("/usr/lib/python2.6/site-packages/ambari_agent/service_remove.txt"):
      line = line.strip()
      if (line == ""):
        continue

      if (findkey):
        if(line.find("[") < 0):
          self.log("get value: {0}".format(line))
          res.append(line)
        else:
          break

      elif (line.find(key)>=0) :
        findkey = True

    fileinput.close()
    return res

  def run_cmd(self,cmd):
    self.log("Running commmand: " + cmd)
    (ret, output) = commands.getstatusoutput(cmd)
    self.log(output)
    return (ret == 0,output)

  def stop_agent(self):
    self.run_cmd("ambari-agent stop")

  def remove_services_installed_rpm(self):
    repoNames = ''
    for repo in self.repos:
      repoNames += repo + "|"
    repoNames = repoNames[:-1]
    rpmsCmd = "yum list installed 2>/dev/null | grep -E '" + repoNames + "' | awk '{print $1}' | grep -vE '^(expect|expat|curl|glib2|zlib|openssl)\.x86_64$'"

    if self.onServer:
      rpmsCmd += " | grep -vE 'tbds-server|postgresql'"

    cmd = rpmsCmd + " | xargs yum remove -y"
    (ok, output) = self.run_cmd(cmd)
    if not ok:
      cmd = "for x in `" + rpmsCmd + "`; do echo \"removing $x ...\"; yum remove -y $x 2>&1 >/dev/null | grep -i error; done"
      self.run_cmd(cmd)

    self.run_cmd("yum clean all")

  def release_resources(self):
    # kill httpd
    self.run_cmd("service httpd stop")
    self.run_cmd("ps aux | grep httpd | grep -v grep | awk '{print \"kill -9 \"$2}' | sh")
    self.run_cmd("ipcs -m | grep apache | awk '{print \"ipcrm -m \"$2}' | sh")
    self.run_cmd("ipcs -s | grep apache | awk '{print \"ipcrm -s \"$2}' | sh")
    self.run_cmd("ipcs -q | grep apache | awk '{print \"ipcrm -q \"$2}' | sh")

    # gaia docker
    self.run_cmd("umount /gaia/docker/var/lib/docker/devicemapper")

    # kill pg
    if not self.onServer:
      self.run_cmd("service postgresql stop")
      self.run_cmd("ps aux | grep '/usr/pgsql-9.3/bin' | grep -v grep | awk '{print \"kill -9 \"$2}' | sh")
      self.run_cmd("ipcs -m | grep postgres | awk '{print \"ipcrm -m \"$2}' | sh")
      self.run_cmd("ipcs -s | grep postgres | awk '{print \"ipcrm -s \"$2}' | sh")
      self.run_cmd("ipcs -q | grep postgres | awk '{print \"ipcrm -q \"$2}' | sh")

  def remove_dir(self):
    if not self.onServer:
      self.run_cmd("rm -rf /usr/bin/ambari-python-wrap")
      self.run_cmd("rm -rf /usr/lib/python2.6/site-packages/ambari_commons")
      self.run_cmd("rm -rf /usr/lib/python2.6/site-packages/ambari_jinja2")
      self.run_cmd("rm -rf /usr/lib/python2.6/site-packages/resource_management")

      self.run_cmd("rm -rf /var/lib/pgsql/")
      self.run_cmd("rm -rf /var/run/post*")
      self.run_cmd("rm -rf /var/lock/subsys/postgresql*")
      self.run_cmd("rm -f /tmp/.s.PGSQL.*")

      self.log("remove ssh files on agent")
      self.run_cmd("rm -f /home/tencent/.ssh/*")

    dirNames = ""
    for dir in self.dirs:
      dirNames += dir + " "
    dirNames = dirNames[:-1]
    self.run_cmd("rm -rf {0}".format(dirNames))

    self.run_cmd("DIR=/opt/tbds; for x in $(find $DIR -type l); do rm -rf $(readlink -f $x); done; rm -rf $DIR")
    self.run_cmd("DIR=/etc/tbds; for x in $(find $DIR -type l); do rm -rf $(readlink -f $x); done; rm -rf $DIR")
    self.run_cmd("DIR=/var/log/tbds; for x in $(find $DIR -type l); do rm -rf $(readlink -f $x); done; rm -rf $DIR")
    self.run_cmd("DIR=/data/tbds; for x in $(find $DIR -type l); do rm -rf $(readlink -f $x); done; rm -rf $DIR")

  def main(self):
    # stop agent first
    self.stop_agent()

    # release resources
    self.release_resources()

    # remove yum rpms
    self.remove_services_installed_rpm()

    # remove user defined dirs
    self.remove_dir()

    self.log("Agent clean success !")
    self.log("================================================================================")

if __name__ == '__main__':
  obj = AmbariCleaner()
  obj.main()
