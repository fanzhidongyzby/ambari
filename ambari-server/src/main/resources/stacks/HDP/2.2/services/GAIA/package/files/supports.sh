#!/usr/bin/env bash

as_space=' '
as_tab='    '
as_quote='\'''
as_doublequote='"'
as_echo='printf %s\n'
as_echo_n='printf %s'
as_me=$(basename $0)

if [[ "${LOG:-unset}" = unset ]]; then
  $as_echo "$as_me:$LINENO: Please set LOG variable"
  exit 1
fi

exec 5>$LOG
exec 6>&1
exec 7>/dev/null


# ac_exit lineno code message
ac_exit()
{
  as_lineno=${as_lineno:-"$1"}
  as_message=$3
  if [[ "${as_message:+set}" = set ]]; then :
    as_option=" with message ${as_message}"
  fi

  if [[ $2 -ne 0 ]]; then
    { $as_echo "$as_me:${as_lineno:-$LINENO}: failure on last operation with code $2" >&5
    $as_echo "failure on last operation with code $2$as_option" >&6;}
    eval exit $2
  else
    { $as_echo "$as_me:${as_lineno:-$LINENO}: success on last operation with code $2" >&5
    $as_echo "success on last operation with code $2$as_option" >&6;}
    eval exit 0
  fi
}

# ac_check_login_user lineno user result
ac_check_login_user()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking login user is $2" >&5
  $as_echo_n "checking login user is $2... " >&6;}
  if eval \${$3:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $3=no
    if [[ "$(id -u -n)" = $2 ]]; then
      eval $3=yes
    fi
  fi
  
  eval ac_res=\$$3
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_check_file_existence lineno file result
ac_check_file_existence()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking for $2" >&5
  $as_echo_n "checking for $2... " >&6;} 
  if eval \${$3:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $3=no
    if [[ -f "$2" ]]; then
      eval $3=yes
    fi
  fi

  eval ac_res=\$$3
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_dir_existence lineno dir result
ac_check_dir_existence()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking for $2" >&5
  $as_echo_n "checking for $2... " >&6;} 
  if eval \${$3:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $3=no
    if [[ -d "$2" ]]; then
      eval $3=yes
    fi
  fi

  eval ac_res=\$$3
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_file_executable lineno file result
ac_check_file_executable()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking for $2 and its executable permission" >&5
  $as_echo_n "checking for $2 and its executable permission... " >&6;}
  if eval \${$3:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $3=no
    if [[ -f "$2" ]] && [[ -x "$2" ]]; then
      eval $3=yes
    fi
  fi

  eval ac_res=\$$3
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_check_string_in_file lineno string file result
ac_check_string_in_file()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking $as_doublequote$2$as_doublequote in $3" >&5
  $as_echo_n "checking $as_doublequote$2$as_doublequote in $3... " >&6;}
  if eval \${$4:+":"} false; then :
    $as_echo_n "(cache) " >&6
  else
    eval $4=no
    if [[ -n "$(grep "$2" "$3" 2>/dev/null)" ]]; then
      eval $4=yes
    fi
  fi

  eval ac_res=\$$4
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_compose_name prefix ip result
ac_compose_name()
{
  eval unset $3
  eval $3="$1-$(echo $2|sed 's:\.:-:g')"
}

# ac_package_installed lineno package result
ac_package_installed()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking $2 package" >&5
  $as_echo_n "checking $2 package... " >&6;}
  if eval \${$3:+":"} false; then :
    $as_echo_n "(cache) " >&6
  else
    eval $3=no
    if [[ -n "$(yum list installed|egrep ^"$2")" ]]; then
      eval $3=yes
    fi
  fi

  eval ac_res=\$$3
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_install_package lineno package result
ac_install_package()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: installing $2" >&5
  $as_echo_n "installing $2... " >&6;}

  if eval \${$3:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $3=no
    if yum install -y "$2" >&5 2>&1; then :
      eval $3=yes
    fi
  fi

  eval ac_res=\$$3

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_mkdir_p lineno directory result
ac_mkdir_p()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: making directory $2" >&5
  $as_echo_n "making directory $2... " >&6;}

  if eval \${$3:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $3=no
    if mkdir -p $2 >&5 2>&1; then :
      eval $3=yes
    fi
  fi

  eval ac_res=\$$3

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_get_mask (file or directory) result
ac_get_mask()
{
  eval $2=$(stat -c %a $1)
}

# ac_check_owner lineno (file or directory) user result
ac_check_owner()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking $2 belongs to user $3" >&5
  $as_echo_n "checking $2 belongs to user $3... " >&6;}

  if eval \${$4:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $4=no
    if [[ "$(stat -c %U $2)" = "$3" ]]; then :
      eval $4=yes
    fi
  fi

  eval ac_res=\$$4

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_check_group lineno (file or directory) group result
ac_check_group()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking $2 belongs to group $3" >&5
  $as_echo_n "checking $2 belongs to group $3... " >&6;}

  if eval \${$4:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $4=no
    if [[ "$(stat -c %G $2)" = "$3" ]]; then :
      eval $4=yes
    fi
  fi
  
  eval ac_res=\$$4

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_check_kernel_version lineno major minor result
ac_check_kernel_version()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking kernel version should be not less than $2.$3" >&5
  $as_echo_n "checking kernel version should be not less than $2.$3... " >&6;}

  if eval \${$4:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $4=no
    eval major=$(uname -r|cut -d- -f1|cut -d. -f1)
    eval minor=$(uname -r|cut -d- -f1|cut -d. -f2)
    if [[ $major -ge $2 ]] && [[ $minor -ge $3 ]]; then :
      eval $4=yes
    fi
  fi
  
  eval ac_res=\$$4

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_check_kernel_module lineno module result
ac_check_kernel_module()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking kernel module $2" >&5
  $as_echo_n "checking kernel module $2... " >&6;}

  if eval \${$3:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $3=no
    if [[ -z "$(modprobe $2 2>&1)" ]]; then :
      eval $3=yes
    fi
  fi
  
  eval ac_res=\$$3

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_check_user_existence lineno user result
ac_check_user_existence()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking user $2 existence" >&5
  $as_echo_n "checking user $2 existence... " >&6;}

  if eval \${$3:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $3=no
    if [[ -n "$(cut -d: -f1 /etc/passwd|egrep ^$2$)" ]]; then :
      eval $3=yes
    fi
  fi
  
  eval ac_res=\$$3

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_remove_user_and_home lineno user result
ac_remove_user_and_home()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking remove user $2" >&5
  $as_echo_n "checking remove user $2... " >&6;}

  if eval \${$3:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $3=no
    if userdel -r $2 >&5 2>&1; then :
      eval $3=yes
    fi
  fi
  
  eval ac_res=\$$3

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_add_user lineno user directory group uid result
ac_add_user()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: remove user $2" >&5
  $as_echo_n "remove user $2... " >&6;}

  if eval \${$6:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $6=no
    if useradd -d $3 -m -g $4 -u $5 $2 >&5 2>&1; then :
      eval $6=yes
    fi
  fi
  
  eval ac_res=\$$6

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_set_user_password lineno user password result
ac_set_user_password()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: set user $2 password" >&5
  $as_echo_n "set user $2 password... " >&6;}

  if eval \${$4:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $4=no
    passwd $2 >&5 2>&1 <<EOF
$3
$3
EOF
    if [[ $? -eq 0 ]]; then :
      eval $4=yes
    fi
  fi
  
  eval ac_res=\$$4

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_check_group_existence lineno group result
ac_check_group_existence()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking group $2 existence" >&5
  $as_echo_n "checking group $2 existence... " >&6;}

  if eval \${$3:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $3=no
    if [[ "x$(cut -d: -f1 /etc/group|egrep ^$2$)" = x$2 ]]; then :
      eval $3=yes
    fi
  fi
  
  eval ac_res=\$$3

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_add_group lineno group result
ac_add_group()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: add group $2" >&5
  $as_echo_n "add group $2... " >&6;}

  if eval \${$3:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $3=no
    if groupadd $2 >&5 2>&1; then :
      eval $3=yes
    fi
  fi
  
  eval ac_res=\$$3

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_get_pid_list name result
ac_get_pid_list()
{
  as_list=("$(pidof $1)")
  eval "$2=("${as_list[@]}")"
  unset as_list
}

# ac_java_get_pid_list name result
ac_java_get_pid_list()
{
  as_info_list=()

  for info in $(jps); do
    as_info_list+=("${info}")
  done

  as_list=()
  for (( i = 1; i < ${#as_info_list[@]}; i+=2 )); do
    if [[ "${as_info_list[$i]}" = "$1" ]]; then :
      as_list+=("${as_info_list[$(($i-1))]}")
    fi
  done
  eval "$2=("${as_list[@]}")"
  unset as_list
  unset as_info_list
}

# ac_service_method lineno service method result
ac_service_method()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: $3 $2 service" >&5
  $as_echo_n "$3 $2 service... " >&6;}

  if eval \${$4:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $4=no
    if /etc/init.d/$2 $3 >&5 2>&1; then :
      eval $4=yes
    fi
  fi

  eval ac_res=\$$4

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_systemctl_method lineno service method result
ac_systemctl_method()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: systemctl $3 $2" >&5
  $as_echo_n "systemctl $3 $2... " >&6;}

  if eval \${$4:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $4=no
    if systemctl $3 $2 >&5 2>&1; then :
      eval $4=yes
    fi
  fi

  eval ac_res=\$$4

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_copy lineno option src dst result
ac_copy()
{
  as_lineno=${as_lineno:-"$1"}

  { $as_echo "$as_me:${as_lineno:-$LINENO}: copy $3 to $4 with option $2" >&5
  $as_echo_n "copy $3 to $4 with option $2... " >&6;}

  if eval \${$5:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $5=no
    if cp $2 $3 $4 >&5 2>&1; then :
      eval $5=yes
    fi
  fi

  eval ac_res=\$$5

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_move lineno src dst result
ac_move()
{
  as_lineno=${as_lineno:-"$1"}

  { $as_echo "$as_me:${as_lineno:-$LINENO}: move $2 to $3" >&5
  $as_echo_n "move $2 to $3... " >&6;}

  if eval \${$4:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $4=no
    if mv -f $2 $3 >&5 2>&1; then :
      eval $4=yes
    fi
  fi

  eval ac_res=\$$4

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_change_owner lineno option owner (file or directory) result
ac_change_owner()
{
  as_lineno=${as_lineno:-"$1"}

  { $as_echo "$as_me:${as_lineno:-$LINENO}: change $4 owner to $3" >&5
  $as_echo_n "change $4 owner to $3... " >&6;}

  if eval \${$5:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $5=no
    if chown $2 $3 $4 >&5 2>&1; then :
      eval $5=yes
    fi
  fi

  eval ac_res=\$$5

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_change_group lineno option group (file or directory) result
ac_change_group()
{
  as_lineno=${as_lineno:-"$1"}

  { $as_echo "$as_me:${as_lineno:-$LINENO}: change $4 group to $3" >&5
  $as_echo_n "change $4 group to $3... " >&6;}

  if eval \${$5:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $5=no
    if chgrp $2 $3 $4 >&5 2>&1; then :
      eval $5=yes
    fi
  fi

  eval ac_res=\$$5

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_change_mode lineno option (file or directory) result
ac_change_mode()
{
  as_lineno=${as_lineno:-"$1"}

  { $as_echo "$as_me:${as_lineno:-$LINENO}: change $3 mode to $2" >&5
  $as_echo_n "change $3 mode to $2... " >&6;}

  if eval \${$4:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $4=no
    if chmod $2 $3 >&5 2>&1; then :
      eval $4=yes
    fi
  fi

  eval ac_res=\$$4

  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_untar_package lineno package directory result
ac_untar_package()
{
  as_lineno=${as_lineno:-"$1"}

  { $as_echo "$as_me:${as_lineno:-$LINENO}: untar $2 to $3" >&5
  $as_echo_n "untar $2 to $3... " >&6;}

  if eval \${$4:+":"} false; then :
    $as_echo_n "(cached) " >&6
  else
    eval $4=no
    if tar xvf $2 -C $3 >&5 2>&1; then :
      eval $4=yes
    fi
  fi

  eval ac_res=\$$4
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_get_interface_ip lineno interface result
ac_get_interface_ip()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: get $2 interface ip address" >&5
  $as_echo_n "get $2 interface ip address... " >&6;}
  if eval \${$3:+":"} false; then :
    eval as_ip=\$$3
  else
    eval $3=$(ip addr list $2|grep "inet${as_space}"|awk '{print $2}'|cut -d/ -f1|head -n 1)
    eval as_ip=\$$3
  fi
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $as_ip" >&5
  $as_echo "$as_ip" >&6;}
  unset as_ip
  unset as_lineno
}

# ac_check_running lineno name result
ac_check_running()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking $2 has been runnning" >&5
  $as_echo_n "checking $2 has been runnning... " >&6;}
  
  ac_get_pid_list "$2" "pid_list"
  eval $3=no
  if [[ ${#pid_list[@]} -gt 0 ]]; then :
    eval $3=yes
  fi

  eval ac_res=\$$3
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
  unset pid_list
}

# ac_check_script_running lineno name result
ac_check_script_running()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking $2 has been runnning" >&5
  $as_echo_n "checking $2 has been runnning... " >&6;}
  
  # pgrep is a kind of process grep method
  eval as_list=("$(pgrep -f $2)")
  eval $3=no
  if [[ ${#as_list[@]} -gt 0 ]]; then :
    eval $3=yes
  fi

  eval ac_res=\$$3
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
  unset as_list
}

# ac_java_check_running lineno name result
ac_java_check_running()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking $2 has been runnning" >&5
  $as_echo_n "checking $2 has been runnning... " >&6;}
  
  ac_java_get_pid_list "$2" "java_pid_list"
  eval $3=no
  if [[ ${#java_pid_list[@]} -gt 0 ]]; then :
    eval $3=yes
  fi

  eval ac_res=\$$3
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
  unset java_pid_list
}

# trim_variable string result
trim_variable()
{
  eval $2=\"$(echo $1|sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')\"
}

# export_variable variable_file
export_variable()
{
  while read -r line; do
    if [[ "$line" = \#* ]] || [[ "${line:-empty}" = empty ]]; then
      continue
    fi

    # variable=value
    name=$(echo $line|cut -d= -f1)
    value=$(echo $line|cut -d= -f2)

    trim_variable "$name" "name"
    trim_variable "$value" "value"

    if [[ "${name:+set}" = set ]] && [[ "${name:+set}" = set ]]; then :
      export $name=$value
    fi
  done<$1
}

# ac_check_swap lineno result
ac_check_swap()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking swap state" >&5
  $as_echo_n "checking swap state... " >&6;}
  
  eval $2=no
  if [[ $(cat /proc/swaps|wc -l) -eq 1 ]]; then :
    eval $2=yes
  fi

  eval ac_res=\$$2
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_check_mount_disk lineno disk result
ac_check_mount_disk()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking mount disk $2" >&5
  $as_echo_n "checking mount disk $2... " >&6;}
  
  eval $3=no
  if [[ $(cat /proc/mounts|awk -v disk_name="$2" '{a[$2]++}END{print a[disk_name]}') -eq 1 ]]; then :
    eval $3=yes
  fi

  eval ac_res=\$$3
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# ac_check_user_in_group lineno user group result
ac_check_user_in_group()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: checking user $2 in group $3" >&5
  $as_echo_n "checking user $2 in group $3... " >&6;}
  
  eval as_user_group=("$(id -nG $2)")
  eval $4=no
  for name in ${as_user_group[@]}; do
    if [[ "x$name" = "x$3" ]]; then :
      eval $4=yes
      break
    fi
  done

  eval ac_res=\$$4
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_user_group
  unset as_lineno
}

# ac_add_user_to_group lineno user group result
ac_add_user_to_group()
{
  as_lineno=${as_lineno:-"$1"}
  { $as_echo "$as_me:${as_lineno:-$LINENO}: add $2 to $3 group" >&5
  $as_echo_n "add $2 to $3 group... " >&6;}
  
  eval $4=no
  if gpasswd -a gaia docker >&5 2>&1; then :
    eval $4=yes
  fi

  eval ac_res=\$$4
  { $as_echo "$as_me:${as_lineno:-$LINENO}: result : $ac_res" >&5
  $as_echo "$ac_res" >&6;}
  unset as_lineno
}

# basic_check lineno bindir
basic_check()
{
  as_lineno=${as_lineno:-"$1"}
  as_bin_dir=$2

  # Login user
  ac_check_login_user "${as_lineno:-$LINENO}" "gaia" "user_gaia_login"
  if [[ "x$user_gaia_login" = xyes ]]; then :
  else
    ac_exit "${as_lineno:-$LINENO}" "1" "login user is not gaia"
  fi

  # setup.conf
  ac_check_file_existence "${as_lineno:-$LINENO}" "${as_bin_dir}/setup.conf" "setup_conf_found"
  if [[ "x$setup_conf_found" = xyes ]]; then :
  else
    ac_exit "${as_lineno:-$LINENO}" "1" "can not find ${as_bin_dir}/setup.conf"
  fi

  # machine.lst
  ac_check_file_existence "${as_lineno:-$LINENO}" "${as_bin_dir}/machine.lst" "machine_list_found"
  if [[ "x$machine_list_found" = xyes ]]; then :
  else
    ac_exit "${as_lineno:-$LINENO}" "1" "can not find ${as_bin_dir}/machine.lst"
  fi

  # mount /gaia disk
  ac_check_mount_disk "${as_lineno:-$LINENO}" "/gaia" "mount_gaia_result"
  if [[ "x$mount_gaia_result" = xyes ]]; then :
  else
    ac_exit "${as_lineno:-$LINENO}" "1" "can not find /gaia mounted"
  fi

  unset as_lineno
  unset as_bin_dir
}
