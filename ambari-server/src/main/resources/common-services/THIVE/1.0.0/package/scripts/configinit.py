from resource_management import *
import sys
import os
import re
class configinit:

  def init_checkstatus_script(self):
    import params
    
    File(params.checkstatus_script, 
      mode=0755,
      content=StaticFile('thive_check_status.sh')
    )

  def update_thive_config(self):
    import params
    print params.thive_config_path
    
    reload(sys)
    sys.setdefaultencoding('utf-8')
  
    print 'create hive-default.xml'
    File(os.path.join(params.thive_config_path,'hive-default.xml'),
      owner='hdfs',
      group='hadoop',
      mode=0755,
      content=Template("thive.hive-default.j2")
    )

    print 'create hive-log4j.properties'
    File(os.path.join(params.thive_config_path,'hive-log4j.properties'),
      owner='hdfs',
      group='hadoop',
      mode=0755,
      content=Template("thive.hive-log4j.j2")
    )


  def init_pg_scripts(self):
    import params

    File(params.initpg_script, 
      mode=0755, 
      content=StaticFile('initpg.sh')
    )

    File(params.clean_doc_script, 
      mode=0755, 
      content=StaticFile('clean_doc.sh')
    )

    File(params.reset_meta_script, 
      mode=0755, 
      content=StaticFile('reset_meta.sql')
    )

    File(params.tdw_meta_global_db_script, 
      mode=0755, 
      content=StaticFile('tdw_meta_global_db.sql')
    )

    File(params.tdw_meta_init_script, 
      mode=0755, 
      content=StaticFile('tdw_meta_init.sql')
    )

    File(params.tdw_meta_pbjar_db_script, 
      mode=0755, 
      content=StaticFile('tdw_meta_pbjar_db.sql')
    )

    File(params.tdw_meta_query_info_db_script, 
      mode=0755, 
      content=StaticFile('tdw_meta_query_info_db.sql')
    )

    File(params.tdw_meta_segment_db_script, 
      mode=0755, 
      content=StaticFile('tdw_meta_segment_db.sql')
    )


  def update_pg_config(self,env):
    import params
    
    print params.pg_config_path

    print 'create postgresql.conf'
    File(os.path.join(params.pg_config_path,'postgresql.conf'),
      owner='hdfs',
      group='hadoop',
      mode=0755,
      content=Template("pg.postgresql.j2")
    )


    print 'create pg_hba.conf'
    print 'create pg_hba.conf'
    print params.pg_server_hosts
    print 'reg ip'
    params.pg_server_hosts_hba = self.reg_ip(params.pg_server_hosts)
    env.set_params(params)
    File(os.path.join(params.pg_config_path,'pg_hba.conf'),
      owner='hdfs',
      group='hadoop',
      mode=0755,
      content=Template("pg.pg_hba.j2")
    )

  def reg_ip(self,ip):
    pat= re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    res = pat.match(ip)
    if res :
      return ip + "/32"
    else:
      return ip

  def update_service_config(self):
    import params

    print 'create system.properties'
    File(os.path.join(params.service_config_path,'system.properties'),
      owner='hdfs',
      group='hadoop',
      mode=0755,
      content=Template("service.system.properties.j2")
    )
