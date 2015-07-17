#!/bin/bash

echo $1
echo $2
echo "init thive pt"


echo "step0: alter postgres password"
psql -h $1 -p $2 -U postgres -c "ALTER USER postgres WITH PASSWORD 'postgres';"

echo "step1: set password"

export PGPASSWORD='postgres'


echo "step2: init meta db"
psql -h $1 -p $2 -U postgres  -f ./tdw_meta_init.sql

echo "step3: tdw_meta_global_db.sql"
psql -h $1 -p $2 -U postgres -f ./tdw_meta_global_db.sql

echo "step4: tdw_meta_query_info_db.sql"

psql -h $1 -p $2 -U postgres -f ./tdw_meta_query_info_db.sql

echo "step5: tdw_meta_pbjar_db.sql"
psql -h $1 -p $2 -U postgres -f ./tdw_meta_pbjar_db.sql

echo "step6: tdw_meta_segment_db.sql"
psql -h $1 -p $2 -U postgres -f ./tdw_meta_segment_db.sql


echo "step7: init pg user"
echo $1
echo $2

psql -h $1 -p $2 -U postgres -c "CREATE $3; ALTER ROLE $3 WITH SUPERUSER LOGIN CREATEDB CREATEROLE CREATEUSER INHERIT PASSWORD '$4';"

echo "step8: init hive user"
echo $5
echo $6

psql -h $1 -p $2 -U postgres -c "insert into tdwuser(user_name,passwd,dba_priv) values('$5','$6',true);"


