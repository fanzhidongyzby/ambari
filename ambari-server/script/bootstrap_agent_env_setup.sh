#!/bin/bash
executor=`whoami`
BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`

hostIP=$1
sshUser=$2
sshPass=$3

ambariHomePath=`cat /etc/passwd | grep ambari: | awk -F':' '{print $6}'`

#copy and execute ambari_agent_env.sh
cp ${ambariHomePath}/.ssh/id_rsa.pub ${currentPath}
tar -czvf ${currentPath}/bootstrap_agent_setup.tar.gz ./id_rsa.pub ./bootstrap_agent_env_script.sh
${currentPath}/bootstrap_agent_env_setup.exp ${currentPath}/bootstrap_agent_setup.tar.gz ${hostIP} ${sshUser} ${sshPass}