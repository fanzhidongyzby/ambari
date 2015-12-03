#!/bin/bash
BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`
sshUser=$1
homePath=`cat /etc/passwd | grep ${sshUser}: | awk -F':' '{print $6}'`
if [ "${homePath}" == "" ]
  then 
    echo "[===== BOOTSTRAP-ERROR =====]${sshUser} user has not exists"
    exit -1
fi

# get sshkey file
cat ${homePath}/.ssh/id_rsa
