#!/bin/bash
BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`

hostIP=$1
sshUser=$2
sshPass=$3
echo "[BOOTSTRAP]2 start to init environment of host: ${hostIP}"
homePath=`cat /etc/passwd | grep ${sshUser}: | awk -F':' '{print $6}'`
#copy and execute ambari_agent_env.sh
if [ "${homePath}" == "" ]
  then 
    echo "tencent user has not exists"
    exit -1
fi
if [ ! -f ${homePath}/.ssh/id_rsa.pub ]; then
  echo "[BOOTSTRAP-ERROR]id_rsa.pub does not exists"
  exit -1; 
fi
cp ${homePath}/.ssh/id_rsa.pub ${currentPath}
cp /etc/yum.repos.d/ambari.repo ${currentPath}
tar -czvf ${currentPath}/bootstrap_agent_setup.tar.gz ./id_rsa.pub ./bootstrap_agent_env_script.sh ./ambari.repo
${currentPath}/bootstrap_agent_env_setup.exp ${currentPath}/bootstrap_agent_setup.tar.gz ${hostIP} ${sshUser} ${sshPass}
echo "[BOOTSTRAP]2 host: ${hostIP} deploy finish"