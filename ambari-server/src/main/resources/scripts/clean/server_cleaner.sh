#!/bin/bash
echo "----------   CLEAN TBDS SERVER  ----------"
echo "stop tbds server ..."
tbds-server stop

echo "stop postgresql ..."
service postgresql-9.3 stop

echo "delete processes and ipcs of postgres in case of someone has kill-9 postgresql"
for x in `ps aux | grep "/usr/pgsql-9.3/bin/postmaster" | grep -v grep | awk '{print $2}'`; do kill -9 $x; done
for x in `ipcs -m | grep postgres | awk '{print $2}'` ; do ipcrm -m $x ; done
for x in `ipcs -s | grep postgres | awk '{print $2}'` ; do ipcrm -s $x ; done

echo "uninstall all the rpm packages of TDP-2.2 repo ..."
yum list installed 2>/dev/null | grep "TDP-2.2" | xargs yum remove -y
yum clean all
rm /etc/yum.repos.d/*.repo

echo "remove postgresql data files ..."
rm -rf /var/lib/pgsql/
rm -rf /var/run/post*
rm -rf /var/lock/subsys/postgresql*

echo "remove residual files on server ..."
rm -rf /var/lib/tbds*
rm -rf /usr/lib/tbds*
rm -rf /var/log/tbds*
rm -rf /var/run/tbds*
rm -rf /usr/bin/tbds*
rm -rf /usr/sbin/tbds*
rm -rf /usr/lib/python2.6/site-packages/tbds*
rm -rf /usr/lib/python2.6/site-packages/resource_management
rm -rf /etc/tbds*

echo "server cleaned success !!!"