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

nginx_conf = config['configurations']['nginx-conf-env']['content']
default_conf = default('/configurations/default-conf-env/content', '')


nginx_start_command = "/etc/init.d/nginx start"
nginx_stop_command = "/etc/init.d/nginx stop"

nginx_conf_path = "/etc/nginx/"
default_conf_path = "/etc/nginx/conf.d/"

nginx_service = "nginx"

nginx_status_key = "running"


nginx_server_host = socket.gethostbyname(socket.gethostname())
nginx_server_port = default('/configurations/nginx-config/nginx.port',8086)

#dse
dse_server_hosts = default("/clusterHostInfo/dse_server_hosts", ["127.0.0.1"])
dse_server_port = default('/configurations/dse-env/dse.server.port', 54301)
dse_server_host_port = utils().bind_hosts_port(dse_server_hosts,dse_server_port,';','server ')