#!/bin/bash

BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`

#create the ambari user
name="tencent"
password="tencent"
home_root="/home"


echo "[BOOTSTRAP]2.1 go to host: ${hostIP}"
if [ ! -d ${home_root} ]; then
  mkdir -p ${home_root}
fi
echo "[BOOTSTRAP]2.2 copy ambari.repo to path /etc/yum.repos.d"
cp ./ambari.repo /etc/yum.repos.d/

if cat /etc/passwd | awk -F : '{print $1}' | grep "^${name}$" >/dev/null 2>&1
  then
    home_root=`cat /etc/passwd | grep ${name}: | awk -F':' '{print $6}' | xargs dirname`
    echo "[BOOTSTRAP]2.3 the ${name} user has always exist"
  else
    yum -y install perl
    pass=$(perl -e 'print crypt($ARGV[0], "wtf")' ${password})
    #pass="wtg/tyWzQ10Ns"
    /usr/sbin/groupadd ${name}
    /usr/sbin/useradd -g ${name} -d ${home_root}/${name} -s /bin/bash -m ${name} -p ${pass}
    echo "[BOOTSTRAP]2.3 create user the ${name}"
fi
if [ ! -d ${home_root}/${name} ]
  then
    mkdir -p ${home_root}/${name}
fi
chown -R ${name}:${name} ${home_root}/${name}

#copy the pub file to tencent's .ssh directory
sshPath="${home_root}/${name}/.ssh"
if [ ! -d ${sshPath} ]
  then
    mkdir -p ${sshPath}
fi
echo "[BOOTSTRAP]2.4 copy id_rsa.pub to ${sshPath}"
cp ${currentPath}/id_rsa.pub ${sshPath}
cat ${sshPath}/id_rsa.pub >> ${sshPath}/authorized_keys
chmod 600 ${sshPath}/authorized_keys
chown ${name}:${name} ${sshPath}/authorized_keys
chmod 700 ${sshPath}
chown ${name}:${name} ${sshPath}

echo "[BOOTSTRAP]2.5 set the user ${name} as superuser"
chmod 440 /etc/sudoers
echo "${name} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
