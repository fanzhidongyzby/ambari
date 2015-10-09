#!/bin/bash

BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`

#create the ambari user
name="tencent"
home_root="/home"


echo "[BOOTSTRAP]2.1 go to host: `hostname`"
echo "[BOOTSTRAP]2.2 copy ambari.repo to path /etc/yum.repos.d"
cp ./ambari.repo /etc/yum.repos.d/

if cat /etc/passwd | awk -F : '{print $1}' | grep "^${name}$" >/dev/null 2>&1
  then
    home_root=`cat /etc/passwd | grep ${name}: | awk -F':' '{print $6}' | xargs dirname`
    echo "[BOOTSTRAP]2.3 the ${name} user has always exist"
  else
    /usr/sbin/groupadd ${name}
    /usr/sbin/useradd -g ${name} -d ${home_root}/${name} -s /bin/bash -m ${name}
    if [ $? -ne 0 ];then
      echo "[===== BOOTSTRAP-ERROR =====]create user ${name} failed"
      exit -1 
    fi
    echo "[BOOTSTRAP]2.3 create user the ${name} success"
fi
chown -R ${name}:${name} ${home_root}/${name}

#copy the pub file to tencent's .ssh directory
sshPath="${home_root}/${name}/.ssh"
echo "[BOOTSTRAP]2.4 copy id_rsa.pub to ${sshPath}"
mkdir -p ${sshPath}
cp ${currentPath}/id_rsa.pub ${sshPath}
cat ${sshPath}/id_rsa.pub >> ${sshPath}/authorized_keys
chmod 600 ${sshPath}/authorized_keys
chown ${name}:${name} ${sshPath}/authorized_keys
chmod 700 ${sshPath}
chown ${name}:${name} ${sshPath}

echo "[BOOTSTRAP]2.5 set the user ${name} as superuser"
chmod 440 /etc/sudoers
grep -q "${name} ALL=(ALL) NOPASSWD:ALL" /etc/sudoers;
if [[ $? -ne 0 ]]; then
    echo "${name} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
fi

echo "[BOOTSTRAP]2.6 clean the old ambari-agent process"
ambari-agent stop
ps aux | grep ambari_agent | grep -v grep | awk '{print "kill -9 "$2}' | sh
yum remove -y ambari-agent
yum clean all
