from resource_management import *
import sys
import os
import commands
class configinit:

  def update_config(self):
    import params

    print 'create storm.yaml file'
    File(os.path.join(params.conf_dir,'storm.yaml'),
      owner=params.storm_user,
      group=params.storm_group,
      mode=0644,
	  encoding='UTF-8',
      content=Template("storm.yaml.j2")
    )
    File(os.path.join(params.bin_dir,'storm-env.sh'),
      owner=params.storm_user,
      group=params.storm_group,
      mode=0755,
	  encoding='UTF-8',
      content=Template("storm-env.sh.j2")
    )

  def update_nimbus_config(self):
    self.update_config()
    
  def update_supervisor_config(self):
    self.update_config()
    
  def update_ui_server_config(self):
    self.update_config()
