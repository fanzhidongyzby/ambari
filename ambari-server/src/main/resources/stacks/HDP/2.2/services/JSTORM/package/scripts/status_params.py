#!/usr/bin/env python
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
from resource_management.libraries.script import Script
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions import default, format

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()


#script
check_status_script = "{0}/checkStatus.sh".format(tmp_dir)

#process name
proc_nimbus_name = "com.tencent.jstorm.daemon.nimbus.NimbusServer"
proc_supervisor_name = "com.tencent.jstorm.daemon.supervisor.Supervisor"
proc_ui_server_name = "com.tencent.jstorm.ui.core.UIServer"

