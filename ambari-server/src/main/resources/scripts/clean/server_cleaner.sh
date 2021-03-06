#!/bin/bash
echo "[$(date "+%F %T")]"

echo "----------   CLEAN TBDS SERVER  ----------"
echo "stop tbds server ..."
tbds-server stop
ps aux | grep -E "org\.apache\.ambari\.server\.controller\.AmbariServer" | grep -v grep | awk '{print "kill -9 "$2}' | sh

echo "stop postgresql ..."
service postgresql stop
ps aux | grep "/usr/pgsql-9.3/bin" | grep -v grep | awk '{print "kill -9 "$2}' | sh
ipcs -m | grep postgres | awk '{print "ipcrm -m "$2}' | sh
ipcs -s | grep postgres | awk '{print "ipcrm -s "$2}' | sh
ipcs -q | grep postgres | awk '{print "ipcrm -q "$2}' | sh

echo "uninstall tbds-server ..."
yum remove -y -v postgresql*
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

echo "remove ssh files on server ..."
rm -f /home/tencent/.ssh/*

echo "[$(date "+%F %T")]"
echo "server cleaned success !!!"
echo "================================================================================"
