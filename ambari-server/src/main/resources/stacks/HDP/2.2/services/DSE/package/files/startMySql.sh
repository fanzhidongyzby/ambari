#!/bin/bash

echo "Invoke startMysql.sh"


whoami

MYSQL_DB_HOST=$1
MYSQL_DB_DATA_DIR=$2
MYSQL_DB_USERR=$3
MYSQL_DB_PASSWORD=$4
MYSQL_DB_PORT=$5

echo "Param list: $MYSQL_DB_HOST   $MYSQL_DB_DATA_DIR $MYSQL_DB_PORT $MYSQL_DB_USERR   $MYSQL_DB_PASSWORD"

NETWORK_FILE=/etc/sysconfig/network
DEFAULT_MYSQL_USER=mysql
MYSQL_DATABASE_NAME=dse_configcenter
DEFAULT_SLEEP_SECONDS=5

# Install the mysql packages if it is not installed by ambari
#sudo yum install -y 0 -d 0 mysql*

echo "Stop and clean mysql first"

# Stop the mysql and clear the data if it's running before
IS_RUNNING=`service mysqld status | grep running | wc -l`
if [ "$IS_RUNNING" == 1 ]; then
    service mysqld stop
fi

# Create the database data directory
if [ -d "$MYSQL_DB_DATA_DIR" ]; then
   rm -rf $MYSQL_DB_DATA_DIR
fi
mkdir -p $MYSQL_DB_DATA_DIR

echo "Create the directory successfully"

# Assign the directory operation right to mysql user
chown -R $DEFAULT_MYSQL_USER $MYSQL_DB_DATA_DIR

# Touch the /etc/sysconfig/network file if it doesn't exist, since we need it to start the mysql service
if [ ! -f "$NETWORK_FILE" ]; then
   touch $NETWORK_FILE
fi

echo "Touch the network file"

# Start mysql with specified data directory
cat /etc/my.cnf | awk -v var=$MYSQL_DB_DATA_DIR '{if($MYSQL_DB_DATA_DIR~/^datadir=/){print "datadir="var}else print $0}' > my.cnf.tmp

# Set special port

PORT_EXIST=`cat my.cnf.tmp | grep -iE "^port=$MYSQL_DB_PORT\$" | wc -l`

if [ $PORT_EXIST -le 0 ]
then
        #shoud not add listen in DEFAULT_HTTPD_CONF
       echo "port=$MYSQL_DB_PORT" >> my.cnf.tmp
       cp my.cnf.tmp /etc/my.cnf
       rm -rf my.cnf.tmp 
else
       cat my.cnf.tmp | awk -v var=$MYSQL_DB_PORT '{if($MYSQL_DB_PORT~/^port=/){print "port="var}else print $0}' > my.cnf.tmp.tmp
       cp my.cnf.tmp.tmp /etc/my.cnf
       rm -rf my.cnf.tmp.tmp
fi

echo "Customize the configuration successfully"

# Start mysql
service mysqld start
IS_RUNNING=`service mysqld status | grep running | wc -l`
if [ "$IS_RUNNING" == 0 ]; then
   echo "Start mysql failed, just exit"
   exit 1
fi

echo "Mysql daemon starts successfully"

# Create the lhotse database
mysql -uroot -e "CREATE DATABASE $MYSQL_DATABASE_NAME"

echo "Create $MYSQL_DATABASE_NAME with result $?"

# Create the lhotse database user
mysql -uroot -e "CREATE USER $MYSQL_DB_USERR IDENTIFIED BY '$MYSQL_DB_PASSWORD'"

echo "Create user $MYSQL_DB_USERR with result $?"

# Grant the database can be accessed from any machines
mysql -uroot -e "GRANT ALL PRIVILEGES ON $MYSQL_DATABASE_NAME.* TO '$MYSQL_DB_USERR'@'%'"

echo "Grant privileges for all hosts with result $?"

# Grant the database can be accessed from the db host machine
mysql -uroot -e "GRANT ALL PRIVILEGES ON $MYSQL_DATABASE_NAME.* TO '$MYSQL_DB_USERR'@'$MYSQL_DB_HOST' IDENTIFIED BY '$MYSQL_DB_PASSWORD'"

echo "Grant privileges for $MYSQL_DB_HOST with result $?"

# Grant the database can be accessed from local machine
mysql -uroot -e "GRANT ALL PRIVILEGES ON $MYSQL_DATABASE_NAME.* TO '$MYSQL_DB_USERR'@'localhost' IDENTIFIED BY '$MYSQL_DB_PASSWORD'"

echo "Grant privileges for locallhost with result $?"

#init data

mysql -uroot < '/var/lib/ambari-agent/data/tmp/dbInit.sql'

echo "init data $?"

# Flush all privileges
mysql -uroot -e "FLUSH PRIVILEGES"

# Stop the mysql database
service mysqld stop
