#!/usr/bin/env bash

bin=$(dirname "${BASH_SOURCE[0]}")
bin=$(cd "$bin"; pwd)

unset LOG
export LOG=/tmp/setup-env.log

. ${bin}/supports.sh

node_type=$1

if [[ "x$node_type" = "xmaster" ]] || [[ "x$node_type" = "xslave" ]]; then :
else
  ac_exit "$LINENO" "1" "argument should be master or slave"
fi

# Login user must be root
ac_check_login_user "$LINENO" "root" "ac_cv_login_user_root"
if [[ "x$ac_cv_login_user_root" = xyes ]]; then :
else
  ac_exit "$LINENO" "1" "login user must be root"
fi

{ eval interface_name=${interface_name:-eth1}
eval docker_version=${docker_version:-1.6.0}
eval docker_md5sum=${docker_md5sum:-533f9ec}
eval base_dir=${base_dir:-/gaia};
} || ac_exit "$LINENO" "1"

ac_get_interface_ip "$LINENO" "$interface_name" "own_ip"
if [[ "${own_ip:-unset}" = unset ]]; then :
  ac_exit "$LINENO" "1" "no ip address for $interface_name"
fi

# hostname
unset my_hostname
my_hostname=$(hostname)
ac_compose_name "docker" "$own_ip" "target_hostname"
if [[ "$my_hostname" != "$target_hostname" ]]; then :
  ac_exit "$LINENO" "1" "$own_ip: hostname should be $target_hostname"
fi

# resolv.conf
unset string_in_resolv_conf

ac_check_string_in_file "$LINENO" "nameserver 10.177.153.14" "/etc/resolv.conf" "string_in_resolv_conf"
if [[ "x$string_in_resolv_conf" = xyes ]]; then :
else
  cat >> /etc/resolv.conf <<EOF
nameserver 10.177.153.14
EOF
fi

unset string_in_resolv_conf

ac_check_string_in_file "$LINENO" "nameserver 10.196.137.14" "/etc/resolv.conf" "string_in_resolv_conf"
if [[ "x$string_in_resolv_conf" = xyes ]]; then :
else
  cat >> /etc/resolv.conf <<EOF
nameserver 10.196.137.14
EOF
fi

unset string_in_resolv_conf

ac_check_string_in_file "$LINENO" "domain tencent-distribute.com" "/etc/resolv.conf" "string_in_resolv_conf"
if [[ "x$string_in_resolv_conf" = xyes ]]; then :
else
  cat >> /etc/resolv.conf <<EOF
domain tencent-distribute.com
EOF
fi

# kernel
ac_check_kernel_version "$LINENO" "3" "10" "kernel_match"
if [[ "x$kernel_match" = xyes ]]; then :
else
  ac_exit "$LINENO" "1" "$own_ip: kernel is less than 3.10"
fi

# NAT module
ac_check_kernel_module "$LINENO" "iptable_nat" "kernelmodule_iptable_nat"
if [[ "x$kernelmodule_iptable_nat" = xyes ]]; then :
else
  ac_exit "$LINENO" "1" "$own_ip: can not find iptable nat module"
fi

# mount /gaia disk
ac_check_mount_disk "$LINENO" "/gaia" "mount_gaia_result"
if [[ "x$mount_gaia_result" = xyes ]]; then :
else
  ac_exit "$LINENO" "1" "$own_ip: can not find /gaia mounted"
fi

# swap state
ac_check_swap "$LINENO" "swap_state"
if [[ "x$swap_state" = xyes ]]; then :
else
  ac_exit "$LINENO" "1" "$own_ip: swap should be shutdown"
fi

# user gaia
ac_check_user_existence "$LINENO" "gaia" "gaia_user"
if [[ "x$gaia_user" = xyes ]]; then :
else
  ac_exit "$LINENO" "1" "$own_ip: user gaia is not existed"
fi

# docker version
if [[ "x$node_type" = "xslave" ]]; then :
  { $as_echo "$as_me:$LINENO: checking docker version" >&5
  $as_echo_n "checking docker version... " >&6;}
  as_version=$(docker --version 2>/dev/null)
  if [[ "$as_version" = "Docker version ${docker_version}, build ${docker_md5sum}" ]]; then
    { $as_echo "$as_me:$LINENO: result : yes" >&5
    $as_echo "yes" >&6;}
  else
    { $as_echo "$as_me:$LINENO: result : no" >&5
    $as_echo "no" >&6;}

    ac_exit "$LINENO" "1" "$own_ip: docker version mismatch"
  fi

  ac_check_file_executable "$LINENO" "/etc/init.d/docker" "docker_service_executable"
  if [[ "x$docker_service_executable" = xyes ]]; then :
  else
    ac_exit "$LINENO" "1" "$own_ip: docker service file is not existed"
  fi

  ac_check_string_in_file "$LINENO" "/gaia/docker/var/lib/docker/$prog" "/etc/init.d/docker" "docker_log_string"
  if [[ "x$docker_log_string" = xyes ]]; then :
  else
    { $as_echo "$as_me:$LINENO: change docker service file" >&5
    $as_echo_n "change docker service file... " >&6;}
    if sed -i 's~logfile=\(.*\)~logfile=/gaia/docker/var/lib/docker/$prog~g' /etc/init.d/docker >&5 2>&1; then :
      { $as_echo "$as_me:$LINENO: result : yes" >&5
      $as_echo "yes" >&6;}
    else
      { $as_echo "$as_me:$LINENO: result : no" >&5
      $as_echo "no" >&6;}

      ac_exit "$LINENO" "1" "$own_ip: can not change /etc/init.d/docker"
    fi
  fi

  ac_check_dir_existence "$LINENO" "/gaia/docker/var/lib/docker" "docker_log_found"
  if [[ "x$docker_log_found" = xyes ]]; then :
  else
    ac_mkdir_p "$LINENO" "/gaia/docker/var/lib/docker" "mkdir_docker_log"
    if [[ "x$mkdir_docker_log" = xyes ]]; then :
    else
      ac_exit "$LINENO" "1" "$own_ip: can not make directory /gaia/docker/var/lib/docker"
    fi
  fi

  ac_service_method "$LINENO" "docker" "stop" "stop_docker"
  if [[ "x$stop_docker" = xyes ]]; then :
  else
    ac_exit "$LINENO" "1" "$own_ip: can not stop docker service"
  fi

  { $as_echo "$as_me:$LINENO: remove /var/lib/docker" >&5
    $as_echo_n "remove /var/lib/docker... " >&6;}
  if rm -rf /var/lib/docker >&5 2>&1; then :
    { $as_echo "$as_me:$LINENO: result : yes" >&5
    $as_echo "yes" >&6;}
  else
    { $as_echo "$as_me:$LINENO: result : no" >&5
    $as_echo "no" >&6;}

    ac_exit "$LINENO" "1" "$own_ip: can not remove /var/lib/docker"
  fi

  { $as_echo "$as_me:$LINENO: linking /var/lib/docker to /gaia/docker/var/lib/docker" >&5
    $as_echo_n "linking /var/lib/docker to /gaia/docker/var/lib/docker... " >&6;}
  if ln -sf /gaia/docker/var/lib/docker /var/lib/ >&5 2>&1; then :
    { $as_echo "$as_me:$LINENO: result : yes" >&5
    $as_echo "yes" >&6;}
  else
    { $as_echo "$as_me:$LINENO: result : no" >&5
    $as_echo "no" >&6;}

    ac_exit "$LINENO" "1" "$own_ip: can not link /var/lib/ to /gaia/docker/var/lib/docker"
  fi

  # cgconfig
  ac_check_string_in_file "$LINENO" "memory.use_hierarchy=\"0\";" "/etc/cgconfig.conf" "cgconfig_conf_string_found"
  if [[ "x$cgconfig_conf_string_found" = xyes ]]; then :
  else
    cat >> /etc/cgconfig.conf <<EOF
group / {
    memory {
        memory.use_hierarchy="0";
    }
}
EOF
  fi

  ac_systemctl_method "$LINENO" "cgconfig" "is-enabled" "cgconfig_enabled"
  if [[ "x$cgconfig_enabled" = xyes ]]; then :
  else
    ac_systemctl_method "$LINENO" "cgconfig" "enable" "enable_cgconfig"
    if [[ "x$enable_cgconfig" = xyes ]]; then :
    else
      ac_exit "$LINENO" "1" "$own_ip: can not enable cgconfig"
    fi
  fi

  ac_service_method "$LINENO" "docker" "start" "start_docker"
  if [[ "x$start_docker" = xyes ]]; then :
  else
    ac_exit "$LINENO" "1" "$own_ip: can not start docker service"
  fi

  # docker group
  ac_check_group_existence "$LINENO" "docker" "group_docker_existence"
  if [[ "x$group_docker_existence" = xyes ]]; then :
  else
    ac_add_group "$LINENO" "docker" "add_group_docker"
    if [[ "x$add_group_docker" = xyes ]]; then :
    else
      ac_exit "$LINENO" "1" "$own_ip: can not add group docker"
    fi
  fi

  # gaia in docker group
  ac_check_user_in_group "$LINENO" "gaia" "docker" "gaia_in_docker"
  if [[ "x$gaia_in_docker" = xyes ]]; then :
  else
    ac_add_user_to_group "$LINENO" "gaia" "docker" "add_gaia_to_docker"
    if [[ "x$add_gaia_to_docker" = xyes ]]; then :
    else
      ac_exit "$LINENO" "1" "$own_ip: can not add gaia to docker group"
    fi
  fi
fi

# supervisor
ac_check_dir_existence "$LINENO" "${base_dir}/monitor_logs" "monitor_logs_dir_found"
if [[ "x$monitor_logs_dir_found" = xyes ]]; then :
else
  ac_mkdir_p "$LINENO" "${base_dir}/monitor_logs" "mkdir_monitor_logs_dir"
  if [[ "x$mkdir_monitor_logs_dir" = xyes ]]; then :
  else
    ac_exit "$LINENO" "1" "$own_ip: can not make directory ${base_dir}/monitor_logs"
  fi
fi

ac_change_owner "$LINENO" "" "gaia" "${base_dir}/monitor_logs" "monitor_logs_owner"
if [[ "x$monitor_logs_owner" = xyes ]]; then :
else
  ac_exit "$LINENO" "1" "$own_ip: can not change ${base_dir}/monitor_logs owner to gaia"
fi

ac_change_group "$LINENO" "" "users" "${base_dir}/monitor_logs" "monitor_logs_group"
if [[ "x$monitor_logs_group" = xyes ]]; then :
else
  ac_exit "$LINENO" "1" "$own_ip: can not change ${base_dir}/monitor_logs group to users"
fi

ac_check_dir_existence "$LINENO" "${base_dir}/monitor_shell" "monitor_shell_dir_found"
if [[ "x$monitor_shell_dir_found" = xyes ]]; then :
else
  ac_mkdir_p "$LINENO" "${base_dir}/monitor_shell" "mkdir_monitor_shell_dir"
  if [[ "x$mkdir_monitor_shell_dir" = xyes ]]; then :
  else
    ac_exit "$LINENO" "1" "$own_ip: can not make directory ${base_dir}/monitor_shell"
  fi
fi

ac_change_owner "$LINENO" "" "gaia" "${base_dir}/monitor_shell" "monitor_shell_owner"
if [[ "x$monitor_shell_owner" = xyes ]]; then :
else
  ac_exit "$LINENO" "1" "$own_ip: can not change ${base_dir}/monitor_shell owner to gaia"
fi

ac_change_group "$LINENO" "" "users" "${base_dir}/monitor_shell" "monitor_shell_group"
if [[ "x$monitor_shell_group" = xyes ]]; then :
else
  ac_exit "$LINENO" "1" "$own_ip: can not change ${base_dir}/monitor_shell group to users"
fi

ac_exit "$LINENO" "0" "$own_ip"

