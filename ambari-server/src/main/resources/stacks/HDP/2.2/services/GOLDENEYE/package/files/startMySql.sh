#!/bin/bash

echo "Invoke startMysql.sh"

MYSQL_DB_HOST=$1
MYSQL_DB_PORT=$2
MYSQL_DB_DATA_DIR=$3
GOLDENEYE_DB_USER=$4
GOLDENEYE_DB_PASSWORD=$5

GOLDENEYE_GE_SQL=$6
GOLDENEYE_MONITOR_SQL=$7
GOLDENEYE_WEB_HOST=$8

echo "Param list: $MYSQL_DB_HOST   $MYSQL_DB_DATA_DIR  $GOLDENEYE_DB_USER    $GOLDENEYE_DB_PASSWORD   $GOLDENEYE_GE_SQL   $GOLDENEYE_MONITOR_SQL $GOLDENEYE_WEB_HOST"

NETWORK_FILE=/etc/sysconfig/network
DEFAULT_MYSQL_USER=mysql
GOLDENEYE_DATABASE_GE_NAME=gri_ge
GOLDENEYE_DATABASE_MONITOR_NAME=gri_monitor
DEFAULT_SLEEP_SECONDS=5

# Install the mysql packages if it is not installed by ambari
#sudo yum install -y 0 -d 0 mysql*

echo "Stop and clean mysql first"

# Stop the mysql and clear the data if it's running before
IS_RUNNING=`service mysqld status | grep pid | wc -l`
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


# Start mysql with specified port
cat my.cnf.tmp | awk -v var=$MYSQL_DB_PORT '{if($MYSQL_DB_PORT~/^port=/){print "port="var}else print $0}' > my.cnf.tmp.tmp

# Check whether the mysql listen port already exists
PORT_EXIST=`cat my.cnf.tmp.tmp | grep -iE "^port=$MYSQL_DB_PORT\$" | wc -l`
if [ $PORT_EXIST -le 0 ]; then
        #shoud not add listen in DEFAULT_HTTPD_CONF
       echo "port=$MYSQL_DB_PORT" >> my.cnf.tmp.tmp    
fi

cp my.cnf.tmp.tmp /etc/my.cnf
rm -rf my.cnf.tmp.tmp

echo "Customize the configuration successfully"




# Start mysql
service mysqld start
IS_RUNNING=`service mysqld status | grep pid | wc -l`
if [ "$IS_RUNNING" == 0 ]; then
   echo "Start mysql failed, just exit"
   exit 1
fi

echo "Mysql daemon starts successfully"

# Create the golden eye database
mysql -uroot -e "CREATE DATABASE $GOLDENEYE_DATABASE_GE_NAME"

echo "Create $GOLDENEYE_DATABASE_GE_NAME with result $?"

mysql -uroot -e "CREATE DATABASE $GOLDENEYE_DATABASE_MONITOR_NAME"

echo "Create $GOLDENEYE_DATABASE_MONITOR_NAME with result $?"

# Load the lhotse database schema
mysql -uroot $GOLDENEYE_DATABASE_GE_NAME < $GOLDENEYE_GE_SQL

echo "Load $GOLDENEYE_GE_SQL schema data with result $?"

mysql -uroot $GOLDENEYE_DATABASE_MONITOR_NAME < $GOLDENEYE_MONITOR_SQL

echo "Load $GOLDENEYE_MONITOR_SQL schema data with result $?"

# Create the lhotse database user
mysql -uroot -e "CREATE USER $GOLDENEYE_DB_USER  IDENTIFIED BY '$GOLDENEYE_DB_PASSWORD'"

echo "Create user $GOLDENEYE_DB_USER  with result $?"

# Grant the database can be accessed from any machines
mysql -uroot -e "GRANT ALL PRIVILEGES ON $GOLDENEYE_DATABASE_GE_NAME.* TO '$GOLDENEYE_DB_USER'@'%'"

echo "Grant $GOLDENEYE_DATABASE_GE_NAME privileges for all hosts with result $?"

mysql -uroot -e "GRANT ALL PRIVILEGES ON $GOLDENEYE_DATABASE_MONITOR_NAME.* TO '$GOLDENEYE_DB_USER'@'%'"
echo "Grant $GOLDENEYE_DATABASE_MONITOR_NAME privileges for all hosts with result $?"

# Grant the database can be accessed from the db host machine
mysql -uroot -e "GRANT ALL PRIVILEGES ON $GOLDENEYE_DATABASE_GE_NAME.* TO '$GOLDENEYE_DB_USER'@'$MYSQL_DB_HOST' IDENTIFIED BY '$GOLDENEYE_DB_PASSWORD'"

echo "Grant $GOLDENEYE_DATABASE_GE_NAME privileges for $MYSQL_DB_HOST with result $?"

mysql -uroot -e "GRANT ALL PRIVILEGES ON $GOLDENEYE_DATABASE_MONITOR_NAME.* TO '$GOLDENEYE_DB_USER'@'$MYSQL_DB_HOST' IDENTIFIED BY '$GOLDENEYE_DB_PASSWORD'"

echo "Grant $GOLDENEYE_DATABASE_MONITOR_NAME privileges for $MYSQL_DB_HOST with result $?"

#Grant the database to goldeneyey web

mysql -uroot -e "GRANT ALL PRIVILEGES ON $GOLDENEYE_DATABASE_GE_NAME.* TO '$GOLDENEYE_DB_USER'@'$GOLDENEYE_WEB_HOST' IDENTIFIED BY '$GOLDENEYE_DB_PASSWORD'"

echo "Grant $GOLDENEYE_DATABASE_GE_NAME privileges for $MYSQL_DB_HOST with result $?"

mysql -uroot -e "GRANT ALL PRIVILEGES ON $GOLDENEYE_DATABASE_MONITOR_NAME.* TO '$GOLDENEYE_DB_USER'@'$GOLDENEYE_WEB_HOST' IDENTIFIED BY '$GOLDENEYE_DB_PASSWORD'"

echo "Grant $GOLDENEYE_DATABASE_MONITOR_NAME privileges for $MYSQL_DB_HOST with result $?"

# Grant the database can be accessed from local machine
mysql -uroot -e "GRANT ALL PRIVILEGES ON $GOLDENEYE_DATABASE_GE_NAME.* TO '$GOLDENEYE_DB_USER'@'localhost' IDENTIFIED BY '$GOLDENEYE_DB_PASSWORD'"

echo "Grant privileges for locallhost with result $?"

mysql -uroot -e "GRANT ALL PRIVILEGES ON $GOLDENEYE_DATABASE_MONITOR_NAME.* TO '$GOLDENEYE_DB_USER'@'localhost' IDENTIFIED BY '$GOLDENEYE_DB_PASSWORD'"

echo "Grant privileges for locallhost with result $?"

# Flush all privileges
mysql -uroot -e "FLUSH PRIVILEGES"

# Stop the mysql database
service mysqld stop
