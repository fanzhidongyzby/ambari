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
import os
from ambari_commons import OSConst
from resource_management import *

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

import sys
from resource_management import *

class FTP(Script):

    def install(self, env):
       import params
       excludePackage = []
       self.install_packages(env, excludePackage)
       Links(params.new_ftp_install_path, params.ftp_install_path)

    def uninstall(self, env):
       Toolkit.uninstall_service("ftp")

    def configure(self, env):
        import params
        env.set_params(params)
        File(params.config_ftp_script,
             mode=0755,
             content=StaticFile('configFtp.sh')
        )
    
        cmd = format("bash -x {config_ftp_script} {ftp_server_root_path} {ftp_server_port} {ftp_server_user} {ftp_server_pwd}")
        print cmd
        Toolkit.exe(cmd)

    def start(self, env):
       import params
       self.configure(env)
       Toolkit.exe(params.ftpstart)

    def stop(self, env):
        import params
        Toolkit.exe(params.ftpstop)

    def status(self, env):
        import os.path
        import params
        Toolkit.check_service('vsftpd')

if __name__ == "__main__":
    FTP().execute()

