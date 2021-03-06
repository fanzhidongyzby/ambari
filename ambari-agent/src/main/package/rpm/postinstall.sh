# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License


case "$1" in
  1) # Action install
    if [ -f "/var/lib/ambari-agent/install-helper.sh" ]; then
        /var/lib/ambari-agent/install-helper.sh install
    fi
    mkdir -p /etc/sudoers.d
    echo "Defaults:root !requiretty" > /etc/sudoers.d/ambari-agent
    chmod 440 /etc/sudoers.d/ambari-agent
    chkconfig --add ambari-agent
  ;;
  2) # Action upgrade
    if [ -d "/etc/ambari-agent/conf.save" ]; then
        cp -f /etc/ambari-agent/conf.save/* /etc/ambari-agent/conf
        mv /etc/ambari-agent/conf.save /etc/ambari-agent/conf_$(date '+%d_%m_%y_%H_%M').save
    fi

    if [ -f "/var/lib/ambari-agent/install-helper.sh" ]; then
        /var/lib/ambari-agent/install-helper.sh upgrade
    fi
  ;;
esac


BAK=/etc/ambari-agent/conf/ambari-agent.ini.old
ORIG=/etc/ambari-agent/conf/ambari-agent.ini

if [ -f $BAK ]; then
  SERV_HOST=`grep -e hostname\s*= $BAK | sed -r -e 's/hostname\s*=//' -e 's/\./\\\./g'`
  sed -i -r -e "s/(hostname\s*=).*/\1$SERV_HOST/" $ORIG
  rm $BAK -f
fi


exit 0
