#!/bin/bash
executor=`whoami`
BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`
password="tencent"
echo "[BOOTSTRAP]1. start to generate certificate of user:${sshUser}"
sshUser=$1
homePath=`cat /etc/passwd | grep tencent: | awk -F':' '{print $6}'`
if [ "${homePath}" == "" ]
  then 
    echo "[BOOTSTRAP]1.1 create certificate user: ${sshUser}"
    yum -y install perl
    pass=$(perl -e 'print crypt($ARGV[0], "wtf")' ${password})
    sudo /usr/sbin/groupadd tencent
    sudo /usr/sbin/useradd -g tencent -d /home/tencent -s /bin/bash -m tencent -p ${pass}
    homePath="/home/tencent"
fi

# generate sshkey file
sudo yum -y install expect
if [ "${executor}" == "${sshUser}" ]
  then
    ${currentPath}/bootstrap_agent_ssh_keygen.exp ${homePath}
  else
    su -c "${currentPath}/bootstrap_agent_ssh_keygen.exp ${homePath}" - ${sshUser}
fi
echo "[BOOTSTRAP]1. end generate certificate"
