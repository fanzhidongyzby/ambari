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
import commands
from resource_management import *
class init_pg(Script):
  def init(self, env):
    print 'step0: alter postgres password';
    cmd = format("psql -h {pg_server_hosts} -p {pg_server_port} -U postgres -c \"ALTER USER postgres WITH PASSWORD 'postgres';\"" )
    self.run(cmd)

    print 'step1: set password'
    cmd = format("export PGPASSWORD='postgres'")
    self.run(cmd)

    print 'step2: init meta db'
    cmd = format("psql -h {pg_server_hosts} -p {pg_server_port} -U postgres  -f {tdw_meta_init_script}")
    self.run(cmd)

    print 'step3: tdw_meta_global_db.sql'
    cmd = format("psql -h {pg_server_hosts} -p {pg_server_port} -U postgres -f {tdw_meta_global_db_script}")
    self.run(cmd)

    print 'step4: tdw_meta_query_info_db.sql'
    cmd = format("psql -h {pg_server_hosts} -p {pg_server_port} -U postgres -f {tdw_meta_query_info_db_script}")
    self.run(cmd)

    print 'step5: tdw_meta_pbjar_db.sql'
    cmd = format("psql -h {pg_server_hosts} -p {pg_server_port} -U postgres -f {tdw_meta_pbjar_db_script}")
    self.run(cmd)
    
    print 'step6: tdw_meta_segment_db.sql'
    cmd = format("psql -h {pg_server_hosts} -p {pg_server_port} -U postgres -f {tdw_meta_segment_db_script}")
    self.run(cmd)
    
    print 'step7: init pg user'
    cmd =format(" psql -h {pg_server_hosts} -p {pg_server_port} -U postgres -c \"CREATE ROLE {pg_server_user}; ALTER ROLE {pg_server_user} WITH LOGIN CREATEDB CREATEROLE CREATEUSER INHERIT PASSWORD '{pg_server_password}';\"")
    self.run(cmd)

    print 'step8: init hive user'
    cmd = format("psql -h {pg_server_hosts} -p {pg_server_port} -U postgres -d global -c \"insert into tdwuser(user_name,passwd,dba_priv) values('{hive_plc_user}','{hive_plc_password}',true);\"")
    self.run(cmd)

    print 'step9: update seg_split address'
    cmd = format("psql -h {pg_server_hosts} -p {pg_server_port} -U postgres -d global -c \"update seg_split set seg_addr='jdbc:postgresql://{pg_server_port}:5432/seg_1';\"")


  def create_pg_user(self,env):

    print 'start pg for create new pg user'
    cmd = format("psql -h {pg_server_hosts} -p {pg_server_port} -U postgres -d global -c \"insert into tdwuser(user_name,passwd,dba_priv) values('{hive_plc_user}','{hive_plc_password}',true);\"")
    self.run(cmd)


  def run(self,cmd):
    print cmd
#    cmd = format("psql -h $1 -p $2 -U postgres -c \"ALTER USER postgres WITH PASSWORD 'postgres';\"" )
    (ret, output) = commands.getstatusoutput(cmd)
    print ret
    print output
    
    if ret != 0 and output.find("already exists")<0 :
      sys.exit(1)

if __name__ == "__main__":
  init_pg().execute()
