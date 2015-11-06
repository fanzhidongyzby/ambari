from resource_management import *
import os
import commands


def init_config(env):
    import params
    env.set_params(params)

    # tdbus conf directory
    tdbus_conf_path = os.path.join(params.tdbus_install_path, 'conf')

    # flume.conf file
    flume_conf = os.path.join(tdbus_conf_path, 'flume.conf')
    File(flume_conf,
         content=Template('flume.conf.j2'),
         mode=0644)

    # flume-env.sh file
    flume_env = os.path.join(tdbus_conf_path, 'flume-env.sh')
    File(flume_env,
         content=Template('flume-env.sh.j2'),
         mode=0755)

    # tdbus conf directory
    tdbus_bin_path = os.path.join(params.tdbus_install_path, 'bin')

    start_tdbus = os.path.join(tdbus_bin_path, 'start_tdbus.sh')
    File(start_tdbus,
         content=Template('start_tdbus.sh.j2'),
         mode=0755)

    stop = os.path.join(tdbus_bin_path, 'stop.sh')
    File(stop,
         content=Template('stop.sh.j2'),
         mode=0755)

    topic_tool_client = os.path.join(tdbus_bin_path, 'tube_topic_tool_client.py')
    File(topic_tool_client,
         content=Template('tube_topic_tool_client.py.j2'),
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
    if action is "start":
        command_script = format("{start_script}")
    elif action is "stop":
        command_script = format("{stop_script}")
    action_command = "sudo bash -x {0}".format(command_script)
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
