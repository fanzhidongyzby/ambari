#!/bin/bash
echo "----------   CLEAN TBDS SERVER  ----------"
echo "stop tbds server ..."
tbds-server stop
ambari-agent stop

echo "stop postgresql ..."
service postgresql stop

echo "delete processes and ipcs of postgres in case of someone has kill-9 postgresql"
for x in `ps aux | grep "/usr/pgsql-9.3/bin/postmaster" | grep -v grep | awk '{print $2}'`; do kill -9 $x; done
for x in `ipcs -m | grep postgres | awk '{print $2}'`; do ipcrm -m $x; done
for x in `ipcs -s | grep postgres | awk '{print $2}'`; do ipcrm -s $x; done

echo "uninstall all the rpm packages ..."
RPMS=`yum list installed 2>/dev/null | grep -E "TDP|HDP" | awk '{print $1}'`
echo "removing rpms of TDP|HDP repo ..."
RPMS_RM_OK=`echo $RPMS | xargs yum remove -y &>/dev/null; echo $?`
if [[ $RPMS_RM_OK -ne 0 ]]; then
  for x in $RPMS; do echo "removing $x ..."; yum remove -y $x 2>&1 >/dev/null | grep -i error; done
fi

yum remove -y postgresql*

yum clean all

echo "remove postgresql data files ..."
rm -rf /var/lib/pgsql/
rm -rf /var/run/post*
rm -rf /var/lock/subsys/postgresql*

echo "remove links on server ..."
DIR=/opt/tbds; for x in $(find $DIR -type l); do rm -rf $(readlink -f $x); done; rm -rf $DIR
DIR=/etc/tbds; for x in $(find $DIR -type l); do rm -rf $(readlink -f $x); done; rm -rf $DIR
DIR=/var/log/tbds; for x in $(find $DIR -type l); do rm -rf $(readlink -f $x); done; rm -rf $DIR
DIR=/data/tbds; for x in $(find $DIR -type l); do rm -rf $(readlink -f $x); done; rm -rf $DIR

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

rm -rf /var/lib/ambari*
rm -rf /usr/lib/ambari*
rm -rf /var/log/ambari*
rm -rf /var/run/ambari*
rm -rf /usr/bin/ambari*
rm -rf /usr/sbin/ambari*
rm -rf /usr/lib/python2.6/site-packages/ambari*
rm -rf /usr/lib/python2.6/site-packages/resource_management
rm -rf /etc/ambari*

echo "remove gaia files ..."
rm -rf /gaia/*

echo "remove hadoop files ..."
rm -rf /usr/hdp

echo "server cleaned success !!!"