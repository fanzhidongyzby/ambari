#!/bin/sh

if [ ! $# -eq 4 ]; then
  exit -1
fi

BLUEPRINT="$1"
HOST="0.0.0.0"
PORT="$2"
USER="$3"
PSW="$4"

FILE="/tmp/tbdsInstall"
cat << EOM > $FILE
blueprint add --file $BLUEPRINT
cluster build --blueprint tdp
cluster autoAssign
cluster create
EOM

/usr/jdk64/jdk*/bin/java  -jar tbds-shell-0.1.DEV.jar --ambari.host=$HOST --ambari.port=$PORT --ambari.user=$USER --ambari.password=$PSW --cmdfile=$FILE

