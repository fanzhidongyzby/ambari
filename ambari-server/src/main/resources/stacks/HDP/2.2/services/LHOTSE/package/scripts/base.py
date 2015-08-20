import sys
import os
from resource_management import *
from configinit import configinit

class Base(Script):

  

  def install(self, env):
    print 'install lhotse'
    excludePackage = ['lhotse-runner*','mysql-server*','mysql','lhotse-service*','lhotse-web*','vsftpd*']
    self.install_packages(env,excludePackage)
    self.start(env)

    import params
    Links(params.new_lhotse_install_path_base, params.lhotse_install_path_base)
    Links(params.new_lhotse_log_path_base, params.lhotse_log_path_base)
    Links(params.new_lhotse_config_path_base, params.lhotse_config_path_base)

  def start(self, env):
    import params
    print 'call self.config'
    self.configure(env)
    

    print 'start the base';
    print params.java_home
    val= os.system("su lhotse -c '/usr/local/lhotse_base/start_base.sh " + params.java_home + "'")
    print val
     

  def configure(self, env):
    print 'create the config file call configinit()';
    import params
    env.set_params(params)
    configinit().update_base_config()

  def stop(self, env):
    import params
    env.set_params(params)
    print 'Stop the base';
    val= os.system("su lhotse -c '/usr/local/lhotse_base/stop_base.sh'")
    print val
    print 'call self.config'
    

  def status(self, env):
    import params
    env.set_params(params)    

    File(params.check_status_script,
         mode=0755,
        content=StaticFile('checkStatus.sh')
    )
 
    cmd = format("bash -x {check_status_script} {lhotse_base_proc_name} 1 lhotse")
    
    var= os.system(cmd)
    print var

    if var == 0:
        return 0
    else: 
        print "base is down"
        raise ComponentIsNotRunning()

if __name__ == "__main__":
  Base().execute()

