#!/bin/bash
BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`

hostIP=$1
sshUser=$2
sshPass=$3
echo "[BOOTSTRAP]2 start to init environment of host: ${hostIP}"
homePath=`cat /etc/passwd | grep tencent: | awk -F':' '{print $6}'`
#copy and execute ambari_agent_env.sh
if [ "${homePath}" == "" ]
  then 
    echo "[===== BOOTSTRAP-ERROR =====]tencent user has not exists"
    exit -1
fi
if [ ! -f ${homePath}/.ssh/id_rsa.pub ]; then
  echo "[===== BOOTSTRAP-ERROR =====]${homePath}/.ssh/id_rsa.pub does not exists"
  exit -1; 
fi
cp ${homePath}/.ssh/id_rsa.pub ${currentPath}
cp ${homePath}/.ssh/id_rsa ${currentPath}
cp /etc/yum.repos.d/ambari.repo ${currentPath}
tar -czvf ${currentPath}/bootstrap_agent_setup.tar.gz ./id_rsa.pub ./id_rsa ./bootstrap_agent_env_script.sh ./ambari.repo
${currentPath}/uploadFile.exp ${hostIP} ${sshUser} ${sshPass} ${currentPath}/bootstrap_agent_setup.tar.gz /tmp 150
if [ $? -ne 0 ];then
  echo "[===== BOOTSTRAP-ERROR =====]copy the bootstrap_agent_setup.tar.gz to ${hostIP} failed"
  exit -1
fi
#check the tty
if [ "${sshUser}" == "root" ]
  then 
    ttyCheck="chmod 755 /etc/sudoers;sed -i 's/[#]\{0,\}Defaults *requiretty/#Defaults requiretty/g' /etc/sudoers;chmod 440 /etc/sudoers"
    ${currentPath}/execRemoteCmd.exp ${hostIP} ${sshUser} ${sshPass} 150 "${ttyCheck}"
fi
remoteCmd="cd /tmp;sudo tar -xzvf bootstrap_agent_setup.tar.gz >/dev/null;sudo rm -f bootstrap_agent_setup.tar.gz;sudo chmod 777 bootstrap_agent_env_script.sh;sudo ./bootstrap_agent_env_script.sh"
${currentPath}/execRemoteCmd.exp ${hostIP} ${sshUser} ${sshPass} 150 "${remoteCmd}"
if [ $? -ne 0 ];then
  echo "[===== BOOTSTRAP-ERROR =====]execute cmd (${remoteCmd}) failed"
  exit -1
fi
echo "[BOOTSTRAP]2 host: ${hostIP} deploy finish"