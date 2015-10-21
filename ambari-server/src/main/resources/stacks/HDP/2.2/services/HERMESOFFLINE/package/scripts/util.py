from resource_management import *
import os
import commands


def init_config(env):
    import params
    env.set_params(params)

    # hermes conf directory
    hermes_conf_path = os.path.join(params.hermes_install_path, 'conf')

    # hermes_adapter file
    hermes_adapter = os.path.join(hermes_conf_path, 'adapter.properties')
    File(hermes_adapter,
         content=Template('adapter.properties.j2'),
         mode=0644)

    # hermes properties file
    hermes_properties = os.path.join(hermes_conf_path, 'hermes.properties')
    File(hermes_properties,
         content=Template('hermes.properties.j2'),
         mode=0644)

    # hermes properties file
    hermes_log4j = os.path.join(hermes_conf_path, 'log4j.properties')
    File(hermes_log4j,
         content=Template('log4j.properties.j2'),
         mode=0644)
    # zk root directory for hermes
    hermes_zk_root = os.path.join(hermes_conf_path, 'zk.root')
    File(hermes_zk_root,
         content=Template('zk.root.j2'),
         mode=0644)
    # service start command
    service_command = os.path.join(params.hermes_install_path, 'start_service.sh')
    File(service_command,
         content=Template('start_service.sh.j2'),
         mode=0644)


def is_service_run(service_name):
    True if get_service_pid(service_name) else False


def get_service_pid(service_name):
    jps_cmd = format("{java_home}/bin/jps")
    awd_cmd = "{print $1}"
    start_manager_cmd = "sudo {0} | grep {1} | awk '{2}'".format(jps_cmd, service_name, awd_cmd)
    Logger.info(start_manager_cmd)
    (ret, output) = commands.getstatusoutput(start_manager_cmd)
    return output


def zk_connection_string(zk_hosts):
    """get zookeeper cluster hosts with port"""
    zk_hosts_port = []
    for host in zk_hosts:
        host += ':2181'
        zk_hosts_port.append(host)
    return ','.join(zk_hosts_port)


def command_exe(command, service_name):
    (ret, output) = commands.getstatusoutput(command)
    if ret != 0:
        Logger.info("execute {0}  failed ,for {1}".format(command, service_name))
        Logger.error(output)
        return False
    else:
        Logger.info("execute {0}  success ,for {1}".format(command, service_name))
        return True


def load_command_script(env, command_script, command_script_template):
        import params
        env.set_params(params)
        # hermes bin directory
        hermes_bin_path = os.path.join(params.hermes_install_path, 'bin')
        # start_manager file
        hermes_command_file = os.path.join(hermes_bin_path, command_script)
        File(hermes_command_file,
         content=Template(command_script_template),
         mode=0744)

if __name__ == '__main__':
    print zk_connection_string(['192.168.1.2', '192.168.1.3'])
