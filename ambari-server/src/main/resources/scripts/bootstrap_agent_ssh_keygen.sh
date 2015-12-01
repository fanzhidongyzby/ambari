#!/bin/bash
executor=`whoami`
BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`
sshUser=$1
echo "[----- BOOTSTRAP -----]1. start to generate certificate of user:${sshUser}"
homePath=`cat /etc/passwd | grep ${sshUser}: | awk -F':' '{print $6}'`
if [ "${homePath}" == "" ]
  then 
    echo "[----- BOOTSTRAP -----]1.1 create certificate user: ${sshUser}"
    sudo /usr/sbin/groupadd ${sshUser}
    sudo /usr/sbin/useradd -g ${sshUser} -d /home/${sshUser} -s /bin/bash -m ${sshUser}
    homePath="/home/${sshUser}"
fi

# generate sshkey file
if [ "${executor}" == "${sshUser}" ]
  then
    ${currentPath}/bootstrap_agent_ssh_keygen.exp ${homePath}
  else
    su -c "${currentPath}/bootstrap_agent_ssh_keygen.exp ${homePath}" - ${sshUser}
fi
echo "[----- BOOTSTRAP -----]1. end generate certificate"
