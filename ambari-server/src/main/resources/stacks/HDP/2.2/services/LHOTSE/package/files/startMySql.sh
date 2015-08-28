#!/bin/bash

echo "Invoke startMysql.sh"

MYSQL_DB_HOST=$1
MYSQL_DB_DATA_DIR=$2
MYSQL_DB_SCHEMA=$3
LHOTSE_DB_USER=$4
LHOTSE_DB_PASSWORD=$5

echo "Param list: $MYSQL_DB_HOST   $MYSQL_DB_DATA_DIR   $MYSQL_DB_SCHEMA   $LHOTSE_DB_USER   $LHOTSE_DB_PASSWORD"

NETWORK_FILE=/etc/sysconfig/network
DEFAULT_MYSQL_USER=mysql
LHOTSE_DATABASE_NAME=lhotse_open
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
cp my.cnf.tmp /etc/my.cnf
rm -rf my.cnf.tmp

echo "Customize the configuration successfully"

# Start mysql
service mysqld start
IS_RUNNING=`service mysqld status | grep pid | wc -l`
if [ "$IS_RUNNING" == 0 ]; then
   echo "Start mysql failed, just exit"
   exit 1
fi

echo "Mysql daemon starts successfully"

# Create the lhotse database
mysql -uroot -e "CREATE DATABASE $LHOTSE_DATABASE_NAME"

echo "Create $LHOTSE_DATABASE_NAME with result $?"

# Load the lhotse database schema
mysql -uroot $LHOTSE_DATABASE_NAME < $MYSQL_DB_SCHEMA

echo "Load schema data with result $?"

# Create the lhotse database user
mysql -uroot -e "CREATE USER $LHOTSE_DB_USER IDENTIFIED BY '$LHOTSE_DB_PASSWORD'"

echo "Create user $LHOTSE_DB_USER with result $?"

# Grant the database can be accessed from any machines
mysql -uroot -e "GRANT ALL PRIVILEGES ON $LHOTSE_DATABASE_NAME.* TO '$LHOTSE_DB_USER'@'%'"

echo "Grant privileges for all hosts with result $?"

# Grant the database can be accessed from the db host machine
mysql -uroot -e "GRANT ALL PRIVILEGES ON $LHOTSE_DATABASE_NAME.* TO '$LHOTSE_DB_USER'@'$MYSQL_DB_HOST' IDENTIFIED BY '$LHOTSE_DB_PASSWORD'"

echo "Grant privileges for $MYSQL_DB_HOST with result $?"

# Grant the database can be accessed from local machine
mysql -uroot -e "GRANT ALL PRIVILEGES ON $LHOTSE_DATABASE_NAME.* TO '$LHOTSE_DB_USER'@'localhost' IDENTIFIED BY '$LHOTSE_DB_PASSWORD'"

echo "Grant privileges for locallhost with result $?"
mysql -uroot -e "use test;create table test_table(user_name varchar(50), city varchar(50)) ENGINE=InnoDB DEFAULT CHARSET=utf8"
mysql -uroot -e "use test;insert into test_table values('name1','SZ'),('name2','SZ'),('name3','BJ'),('name4','SH'),('name5','SZ'),('name6','NY'),('name7','GZ'),('name8','SH')"
mysql -uroot -e "use test;create table test_table_result(statis_date int(11),city varchar(50),cnt int(11)) ENGINE=InnoDB DEFAULT CHARSET=utf8"
# Flush all privileges
mysql -uroot -e "FLUSH PRIVILEGES"

# Stop the mysql database
service mysqld stop
