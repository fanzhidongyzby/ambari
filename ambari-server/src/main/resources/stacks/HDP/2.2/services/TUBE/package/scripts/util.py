from resource_management import *
import os
import commands


def init_config(env):
    import params
    env.set_params(params)

    # tube conf directory
    tube_conf_path = os.path.join(params.tube_install_path, 'conf')

    # tube master ini file
    master_ini = os.path.join(tube_conf_path, 'master.ini')
    File(master_ini,
         content=Template('master.ini.j2'),
         mode=0644)

    # tube broker ini file
    broker_ini = os.path.join(tube_conf_path, 'server.ini')
    File(broker_ini,
         content=Template('broker.ini.j2'),
         mode=0644)

    broker_ini_source = os.path.join(tube_conf_path, 'server.ini.source')
    File(broker_ini_source,
         content=Template('broker.ini.j2'),
         mode=0644)

    # tube bin directory
    tube_bin_path = os.path.join(params.tube_install_path, 'bin')
    # env file, for java environment
    tube_command_file = os.path.join(tube_bin_path, "env.sh")
    File(tube_command_file,
         content=Template("env.sh.j2"),
         mode=0755)

    start_tool_server = os.path.join(tube_bin_path, "start_tool_server.sh")
    File(start_tool_server,
         content=Template("start_tool_server.sh.j2"),
         mode=0755)

    # topic_tool_client file
    topic_tool_client = os.path.join(tube_bin_path, 'start_tool_client.py')
    File(topic_tool_client,
         content=Template('start_tool_client.py.j2'),
         mode=0744)


def is_service_run(service_name):
    return True if get_service_pid(service_name) else False


def get_service_pid(service_process):
    """return service process id by jps"""
    jps_cmd = format("{java_home}/bin/jps")
    awd_cmd = "{print $1}"
    start_manager_cmd = "sudo {0} | grep {1} | awk '{2}'".format(jps_cmd, service_process, awd_cmd)
    Logger.info(start_manager_cmd)
    (ret, output) = commands.getstatusoutput(start_manager_cmd)
    return output


def zk_connection_string(zk_hosts, port):
    """get zookeeper cluster hosts with port"""
    zk_hosts_port = []
    port = ":" + str(port)
    for host in zk_hosts:
        host += port
        zk_hosts_port.append(host)
    return ','.join(zk_hosts_port)


def service_action(service_name, action):
    """execute different action for service"""
    if service_name is "master":
        command_script = format("{master_script}")
    elif service_name is "broker":
        command_script = format("{broker_script}")
    action_command = "(sudo bash -x {0}  {1}&)  &> /dev/null".format(command_script, action)
    (ret, output) = commands.getstatusoutput(action_command)
    if ret != 0:
        Logger.info("execute {0}  failed ,for {1}".format(action_command, service_name))
        # Logger.error(output)
    else:
        Logger.info("execute {0}  success ,for {1}".format(action_command, service_name))
        # Logger.info(output)


def exe_command(command):
    (ret, output) = commands.getstatusoutput(command)
    return output


if __name__ == '__main__':
    print zk_connection_string(['192.168.1.2', '192.168.1.3'])
