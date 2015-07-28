#!/bin/bash
echo "--------clean tbds server"
echo "step 1: server stop"
sudo tbds-server stop

echo "step2: yum erase tbds-server"
sudo yum erase -y tbds-server

echo "step3: rm dir"
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

echo "--------clean pg"
echo "step 1: stop pg"
service postgresql stop

echo "step 2: "
yum remove -y post*

echo "step3: clean pg"
# remove all postgresql-files
sudo rm -rf /var/lib/pgsql/
sudo rm -rf /var/run/post*
sudo rm -rf /var/lock/subsys/postgresql*

# remove all ipcs of postgresql when it's killed -9
for x in `ipcs -m | grep postgres | awk '{print $2}'` ; do ipcrm -m $x ; done
for x in `ipcs -s | grep postgres | awk '{print $2}'` ; do ipcrm -s $x ; done


echo "step5: yum clean all"
sudo yum clean all


echo "Cluster clean success !!!"