#!/bin/bash
echo "step 1: server stop"
sudo tbds-server stop

echo "step 2: reset db"
sudo tbds-server reset

echo "step3: yum erase tbds-server"
sudo yum erase tbds-server

echo "step4: rm dir"
sudo rm -R /var/lib/tbds*
sudo rm -R /usr/lib/tbds*
sudo rm -R /var/log/tbds*
sudo rm -R /var/run/tbds*
sudo rm -R /usr/bin/tbds*
sudo rm -R /usr/sbin/tbds*
sudo rm -R /usr/lib/python2.6/site-packages/tbds*
sudo rm -R /usr/lib/python2.6/site-packages/resource_management
sudo rm -R /etc/tbds*

sudo rm -R /var/lib/ambari*
sudo rm -R /usr/lib/ambari*
sudo rm -R /var/log/ambari*
sudo rm -R /var/run/ambari*
sudo rm -R /usr/bin/ambari*
sudo rm -R /usr/sbin/ambari*
sudo rm -R /usr/lib/python2.6/site-packages/ambari*
sudo rm -R /usr/lib/python2.6/site-packages/resource_management
sudo rm -R /etc/ambari*

echo "step5: yum clean all"
sudo yum clean all