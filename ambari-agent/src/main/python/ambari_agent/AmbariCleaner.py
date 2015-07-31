#!/usr/bin/env python
import os
import sys
import commands
import socket

from resource_management import *
from ambari_agent.HostInfo import HostInfo, HostInfoLinux
sys.path.append("/var/lib/ambari-agent/cache/custom_actions/scripts/")
from check_host import CheckHost

class AmbariCleaner(Script):

  def hostcheck(self):
    h = HostInfo()
    struct = {}
    h.register(struct,False,False)
    print struct

  def servicecheck(self):
    cmd = "sudo python /var/lib/ambari-agent/cache/custom_actions/scripts/check_host.py ACTIONEXECUTE /usr/lib/python2.6/site-packages/ambari_agent/service_info.json /var/lib/ambari-agent/cache/common-services/HDFS/2.1.0.2.0/package /tmp/my.txt INFO /var/lib/ambari-agent/data/tmp"
    self.run_cmd(cmd)

  def cleaner_services(self):
    self.hostcheck()
    self.servicecheck()

    cmd = "sudo python /usr/lib/python2.6/site-packages/ambari_agent/HostCleanupManually.py --skip \"users\" 1>/tmp/ambari_clean.log"
    self.run_cmd(cmd)

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

    if self.isServerHost():
       return

    cmd = "sudo rm -rf /var/lib/ambari*"
    self.run_cmd(cmd)

    cmd = "sudo rm -rf /usr/lib/ambari*"
    self.run_cmd(cmd)

    cmd = "sudo rm -rf /var/log/ambari*"
    self.run_cmd(cmd)

    cmd = "sudo rm -rf /var/run/ambari*"
    self.run_cmd(cmd)

    cmd = "sudo rm -rf /usr/bin/ambari*"
    self.run_cmd(cmd)

    cmd = "sudo rm -rf /usr/sbin/ambari*"
    self.run_cmd(cmd)

    cmd = "sudo rm -rf /usr/lib/python2.6/site-packages/ambari*"
    self.run_cmd(cmd)

    cmd = "sudo rm -rf /usr/lib/python2.6/site-packages/resource_management"
    self.run_cmd(cmd)

    cmd = "sudo rm -rf /etc/ambari*"
    self.run_cmd(cmd)

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

  def main(self):
    self.cleaner_services()

    self.erasemetrics()

    self.eraseagent()

    self.yum_clean()

    self.remove_dir()

if __name__ == '__main__':
   obj = AmbariCleaner()
   obj.main()
