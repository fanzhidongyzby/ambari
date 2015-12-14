from resource_management import *
import sys
import os
import commands
class configinit:

  def update_base_config(self):
    import params
    print params.base_config_path
  
    print 'create log4j.properties'
    File(os.path.join(params.base_config_path,'log4j.properties'),
      owner='lhotse',
      group='lhotse',
      mode=0644,
      content=Template("base.log4j.properties.j2")
    )

    print 'create lhotse.properties file'
    File(os.path.join(params.base_config_path,'lhotse.properties'),
      owner='lhotse',
      group='lhotse',
      mode=0644,
      content=Template("base.lhotse.properties.j2")
    )

    print 'create hadoop-metrics2.properties file'
    File(os.path.join(params.base_config_path,'hadoop-metrics2.properties'),
      owner='lhotse',
      group='lhotse',
      mode=0644,
      content=Template("base.hadoop-metrics2.properties.j2")
    )
    
    File(os.path.join(params.base_config_path,'setting.php'),
      owner='lhotse',
      group='lhotse',
      mode=0644,
      content=Template("setting.php.j2")
    )

  def update_runner_config(self,env):
    import params
    
    print 'create configRunner.sh'
    File(params.config_runner_script,
         mode=0755,
         content=StaticFile('configRunner.sh')
    )

    print 'create lhotse_base.properties'
    File(os.path.join(params.runner_config_path,'lhotse_base.properties'),
      owner='hdfs',
      group='hdfs',
      mode=0644,
      content=Template("runner.lhotse_base.properties.j2")
    )
    
    print 'create runner.conf'
    File(os.path.join(params.runner_httpd_conf_path,'runner.conf'),
      owner='hdfs',
      group='hdfs',
      mode=0644,
      content=Template("runner.httpd.settings.j2")
    )
    
    print 'update hadoop-env.sh java_home'
    env.set_params(params)
    cmd = format("bash -x {config_runner_script} {java_home} {lhotse_runner_cgi_port}")
    print cmd
    (ret, output) = commands.getstatusoutput(cmd)
    print output
    print ret
    if ret != 0:
        print 'update httpd config fail'
        sys.exit(1)


    var = os.path.isfile(params.lhotse_runner_hadoop_env)
    if not var:
      print '/etc/hadoop/conf/hadoop-env.sh not exist'


  def update_service_config(self):
    import params

    print 'create system.properties'
    File(os.path.join(params.service_config_path,'system.properties'),
      owner='hdfs',
      group='hdfs',
      mode=0644,
      content=Template("service.system.properties.j2")
    )

  def update_web_config(self):
    import params

    print 'create setting.php'
    File(os.path.join(params.web_config_path,'setting.php'),
      owner='hdfs',
      group='hdfs',
      mode=0644,
      content=Template("web.setting.php.j2")
    )
    
    print 'create lhotse_web.conf'
    File(os.path.join(params.runner_httpd_conf_path,'lhotse_web.conf'),
      owner='hdfs',
      group='hdfs',
      mode=0644,
      content=Template("lhotse.web.httpd.settings.j2")
    )
    
  def update_db_config(self):
    import params

    print 'create lhotse_schema.sql'
    File(os.path.join(Script.get_tmp_dir(),'lhotse_schema.sql'),
      owner='hdfs',
      group='hdfs',
      mode=0644,
	  encoding='UTF-8',
      content=Template("lhotse.schema.sql.j2")
    )
