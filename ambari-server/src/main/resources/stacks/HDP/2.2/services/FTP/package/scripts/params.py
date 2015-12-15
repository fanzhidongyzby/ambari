"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management.libraries.functions.default import default
from resource_management import *

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

ftp_install_path='/usr/sbin/vsftpd'
new_ftp_install_path='/opt/tbds/ftp'

ftpstart = 'service vsftpd start'
ftpstop = 'service vsftpd stop'

config_ftp_script = format("{tmp_dir}/configFtp.sh")
ftp_service_daemon = "vsftpd"
ftp_server_host = default("/clusterHostInfo/lhotse_ftp_hosts", ["127.0.0.1"])[0]
ftp_server_port = default("/configurations/ftp/ftp.port", 2121)
ftp_server_user = default("/configurations/ftp/ftp.user", 'ftpadmin')
ftp_server_pwd = default("/configurations/ftp/ftp.password", '123456')
ftp_server_root_path = default("/configurations/ftp/root.path", '/data/ftp_data')

