#!/bin/bash
echo "----------   CLEAN TBDS SERVER  ----------"
echo "stop tbds server ..."
tbds-server stop
ps aux | grep AmbariServer | grep -v grep | awk '{print "kill -9 "$2}' | sh

echo "stop postgresql ..."
service postgresql stop
for x in `ps aux | grep "/usr/pgsql-9.3/bin/postmaster" | grep -v grep | awk '{print $2}'`; do kill -9 $x; done
for x in `ipcs -m | grep postgres | awk '{print $2}'`; do ipcrm -m $x; done
for x in `ipcs -s | grep postgres | awk '{print $2}'`; do ipcrm -s $x; done

echo "uninstall tbds-server ..."
yum remove -y postgresql*
yum clean all

echo "remove postgresql data files ..."
rm -rf /var/lib/pgsql/
rm -rf /var/run/post*
rm -rf /var/lock/subsys/postgresql*
rm -f /tmp/.s.PGSQL.*

echo "remove residual files on server ..."
rm -rf /var/lib/tbds-server
rm -rf /usr/lib/tbds-server
rm -rf /var/log/tbds-server
rm -rf /var/run/tbds-server
rm -rf /usr/sbin/tbds-server
rm -rf /usr/sbin/tbds-server.py
rm -rf /etc/tbds-server

rm -rf /usr/bin/ambari-python-wrap
rm -rf /usr/lib/python2.6/site-packages/ambari_server
rm -rf /usr/lib/python2.6/site-packages/ambari_commons
rm -rf /usr/lib/python2.6/site-packages/ambari_jinja2
rm -rf /usr/lib/python2.6/site-packages/resource_management

echo "server cleaned success !!!"