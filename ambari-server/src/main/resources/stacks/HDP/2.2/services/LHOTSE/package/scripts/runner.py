import os
import sys
import commands
from resource_management import *
from mysql_service import mysql_service
from configinit import configinit

class Runner(Script):
  def install(self, env):
    import params

    print 'Install the Runner Slave';
    self.install_packages(env)

    self.configure(env)

    print 'after install init log'
    if os.path.exists('/usr/local/lhotse_runners/initLogScript.sh'):
        val= os.system("su hdfs -c '/usr/local/lhotse_runners/initLogScript.sh /usr/local/lhotse_runners'")
        print val
    else:
        print 'initLogScript.sh is not exist'

    Links(params.new_lhotse_install_path_runner, params.lhotse_install_path_runner)
    Links(params.new_lhotse_log_path_runner, params.lhotse_log_path_runner)
    Links(params.new_lhotse_config_path_runner, params.lhotse_config_path_runner)
    Links(params.new_lhotse_config_path_runner_cgi, params.lhotse_config_path_runner_cgi)


  def stop(self, env):
    import params
    env.set_params(params)

    print 'Stop the Runner';
    val= os.system("su hdfs -c '/usr/local/lhotse_runners/stop_jar.sh'")
    print val

    #delete conf file
    cmd = format("rm {web_httpd_conf_path}/runner.conf")
    (ret, output) = commands.getstatusoutput(cmd)
    print "delete runner.conf output"
    print output
    print ret

    commands.getstatusoutput("service httpd restart")

  def start(self, env):    
    import params
    print params.java_home

    self.configure(env)

    print 'start the httpd service'
    commands.getstatusoutput("service httpd restart")

    print 'Start the Runner';
    val= os.system("cd /usr/local/lhotse_runners; su hdfs -c '/usr/local/lhotse_runners/start_jar.sh " + params.java_home +"'")
    print val


  def status(self, env):
    import params
    env.set_params(params)    

    File(params.check_status_script,
        mode=0755,
        content=StaticFile('checkStatus.sh')
    )
 
    cmd = format("bash -x {check_status_script} {lhotse_runner_proc_name} 1")
    
    var= os.system(cmd)

    if var == 0:
        return 0
    else:
        print "runner is down"
        raise ComponentIsNotRunning()

  def configure(self, env):
    print 'create config';
    import params
    env.set_params(params)
    
    configinit().update_runner_config(env)

    
if __name__ == "__main__":
  Runner().execute()
