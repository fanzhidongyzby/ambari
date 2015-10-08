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
from resource_management.libraries.functions.security_commons import build_expectations, \
  cached_kinit_executor, get_params_from_filesystem, validate_security_config_properties, \
  FILE_TYPE_XML
from hbase import hbase
from hbase_service import hbase_service
import upgrade
from setup_ranger_hbase import setup_ranger_hbase

         
class HbaseRegionServer(Script):

  def get_stack_to_component(self):
    return {"HDP": "hbase-regionserver"}

  def install(self, env):
    self.install_packages(env)

    import params
    Links(params.new_hbase_install_path, params.hbase_install_path)
    Links(params.new_hbase_config_path, params.hbase_config_path)

  def uninstall(self, env):
    Toolkit.uninstall_service("hbase")

  def configure(self, env):
    import params
    env.set_params(params)

    hbase(name='regionserver')
      
  def pre_rolling_restart(self, env):
    import params
    env.set_params(params)
    upgrade.prestart(env, "hbase-regionserver")

  def post_rolling_restart(self, env):
    import params
    env.set_params(params)
    upgrade.post_regionserver(env)

  def start(self, env, rolling_restart=False):
    import params
    env.set_params(params)
    self.configure(env) # for security
    setup_ranger_hbase()  
    hbase_service( 'regionserver',
      action = 'start'
    )

    Links(params.new_hbase_log_path, params.hbase_log_path)

  def stop(self, env, rolling_restart=False):
    import params
    env.set_params(params)

    hbase_service( 'regionserver',
      action = 'stop'
    )

  def status(self, env):
    import status_params
    env.set_params(status_params)
    pid_file = format("{pid_dir}/hbase-{hbase_user}-regionserver.pid")
    check_process_status(pid_file)

  def security_status(self, env):
    import status_params

    env.set_params(status_params)
    if status_params.security_enabled:
      props_value_check = {"hbase.security.authentication" : "kerberos",
                           "hbase.security.authorization": "true"}
      props_empty_check = ['hbase.regionserver.keytab.file',
                           'hbase.regionserver.kerberos.principal']
      props_read_check = ['hbase.regionserver.keytab.file']
      hbase_site_expectations = build_expectations('hbase-site', props_value_check, props_empty_check,
                                                   props_read_check)

      hbase_expectations = {}
      hbase_expectations.update(hbase_site_expectations)

      security_params = get_params_from_filesystem(status_params.hbase_conf_dir,
                                                   {'hbase-site.xml': FILE_TYPE_XML})
      result_issues = validate_security_config_properties(security_params, hbase_expectations)
      if not result_issues:  # If all validations passed successfully
        try:
          # Double check the dict before calling execute
          if ( 'hbase-site' not in security_params
               or 'hbase.regionserver.keytab.file' not in security_params['hbase-site']
               or 'hbase.regionserver.kerberos.principal' not in security_params['hbase-site']):
            self.put_structured_out({"securityState": "UNSECURED"})
            self.put_structured_out(
              {"securityIssuesFound": "Keytab file or principal are not set property."})
            return

          cached_kinit_executor(status_params.kinit_path_local,
                                status_params.hbase_user,
                                security_params['hbase-site']['hbase.regionserver.keytab.file'],
                                security_params['hbase-site']['hbase.regionserver.kerberos.principal'],
                                status_params.hostname,
                                status_params.tmp_dir)
          self.put_structured_out({"securityState": "SECURED_KERBEROS"})
        except Exception as e:
          self.put_structured_out({"securityState": "ERROR"})
          self.put_structured_out({"securityStateErrorInfo": str(e)})
      else:
        issues = []
        for cf in result_issues:
          issues.append("Configuration file %s did not pass the validation. Reason: %s" % (cf, result_issues[cf]))
        self.put_structured_out({"securityIssuesFound": ". ".join(issues)})
        self.put_structured_out({"securityState": "UNSECURED"})
    else:
      self.put_structured_out({"securityState": "UNSECURED"})

  def decommission(self, env):
    print "Decommission not yet implemented!"
    

if __name__ == "__main__":
  HbaseRegionServer().execute()
