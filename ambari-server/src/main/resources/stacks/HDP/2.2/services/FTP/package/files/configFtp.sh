#!/bin/bash

FTP_DATA_DIR=$1
FTP_LISTEN_PORT=$2
FTP_USER_NAME=$3
FTP_USER_PASSWORD=$4

DEFAULT_SYS_USER=virtual
DEFAULT_FTP_CONF=/etc/vsftpd/vsftpd.conf
DEFAULT_CHROOT_LIST=/etc/vsftpd/chroot_list
DEFAULT_USER_LIST=/etc/vsftpd/user_list
DEFAULT_VIRTUAL_USER_CONFIG_DIR=/etc/vsftpd/vuser_config
DEFAULT_PAMD_FILE=/etc/pam.d/vsftpd

# Check whether the cgi listen port already exists
PORT_EXIST=`netstat -nltp | grep "${FTP_LISTEN_PORT}" | awk '{print $4}' | grep -E "\:${FTP_LISTEN_PORT}\$" | wc -l`
if [ $PORT_EXIST -ge 1 ]; then
        echo "$FTP_LISTEN_PORT already be used by other app, please choose another one."
        exit -1
fi

# Create the home directory
if [ -d "$FTP_DATA_DIR" ]; then
   rm -rf $FTP_DATA_DIR
fi
mkdir -p $FTP_DATA_DIR
chmod 700 $FTP_DATA_DIR

# Create the vsftpd.conf and generate the file content
if [ -f "$DEFAULT_FTP_CONF" ]; then 
   rm -rf $DEFAULT_FTP_CONF
fi

touch $DEFAULT_FTP_CONF

echo    "anonymous_enable=NO"                                       >           $DEFAULT_FTP_CONF
echo    "local_enable=YES"                                          >>          $DEFAULT_FTP_CONF
echo    "write_enable=YES"                                          >>          $DEFAULT_FTP_CONF
echo    "local_umask=02"                                            >>          $DEFAULT_FTP_CONF
echo    "dirmessage_enable=YES"                                     >>          $DEFAULT_FTP_CONF
echo    "xferlog_enable=YES"                                        >>          $DEFAULT_FTP_CONF
echo    "connect_from_port_20=YES"                                  >>          $DEFAULT_FTP_CONF
echo    "xferlog_file=/var/log/vsftpd.log"                          >>          $DEFAULT_FTP_CONF
echo    "xferlog_std_format=YES"                                    >>          $DEFAULT_FTP_CONF
echo    "idle_session_timeout=600"                                  >>          $DEFAULT_FTP_CONF
echo    "data_connection_timeout=120"                               >>          $DEFAULT_FTP_CONF
echo    "async_abor_enable=YES"                                     >>          $DEFAULT_FTP_CONF
echo    "ascii_upload_enable=YES"                                   >>          $DEFAULT_FTP_CONF
echo    "ascii_download_enable=YES"                                 >>          $DEFAULT_FTP_CONF
echo    "ftpd_banner=Welcome to FTP service."                       >>          $DEFAULT_FTP_CONF
echo    "chroot_local_user=YES"                                     >>          $DEFAULT_FTP_CONF
echo    "chroot_list_enable=YES"                                    >>          $DEFAULT_FTP_CONF
echo    "chroot_list_file=$DEFAULT_CHROOT_LIST"                     >>          $DEFAULT_FTP_CONF
echo    "listen=YES"                                                >>          $DEFAULT_FTP_CONF
echo    "pam_service_name=vsftpd"                                   >>          $DEFAULT_FTP_CONF
echo    "userlist_enable=YES"                                       >>          $DEFAULT_FTP_CONF
echo    "tcp_wrappers=YES"                                          >>          $DEFAULT_FTP_CONF
echo    "listen_port=$FTP_LISTEN_PORT"                              >>          $DEFAULT_FTP_CONF
echo    "# virtual user only configurations"                        >>          $DEFAULT_FTP_CONF
echo    "guest_enable=YES"                                          >>          $DEFAULT_FTP_CONF
echo    "guest_username=virtual"                                    >>          $DEFAULT_FTP_CONF
echo    "virtual_use_local_privs=YES"                               >>          $DEFAULT_FTP_CONF
echo    "user_config_dir=$DEFAULT_VIRTUAL_USER_CONFIG_DIR"          >>          $DEFAULT_FTP_CONF

# Create the virutal system account
useradd $DEFAULT_SYS_USER -d $FTP_DATA_DIR -s /sbin/nologin
chown -R $DEFAULT_SYS_USER.$DEFAULT_SYS_USER $FTP_DATA_DIR

# Create the ftp user and password config file
if [ -d "$DEFAULT_VIRTUAL_USER_CONFIG_DIR" ]; then
    rm -rf $DEFAULT_VIRTUAL_USER_CONFIG_DIR
fi
mkdir -p $DEFAULT_VIRTUAL_USER_CONFIG_DIR

if [ -f "$DEFAULT_VIRTUAL_USER_CONFIG_DIR/vuser" ]; then
    rm -rf $DEFAULT_VIRTUAL_USER_CONFIG_DIR/vuser
fi

touch $DEFAULT_VIRTUAL_USER_CONFIG_DIR/vuser

echo    "$FTP_USER_NAME"                                            >>          $DEFAULT_VIRTUAL_USER_CONFIG_DIR/vuser
echo    "$FTP_USER_PASSWORD"                                        >>          $DEFAULT_VIRTUAL_USER_CONFIG_DIR/vuser


# Create user information database
db_load -T -t hash -f $DEFAULT_VIRTUAL_USER_CONFIG_DIR/vuser $DEFAULT_VIRTUAL_USER_CONFIG_DIR/vuser.db

chmod 600 $DEFAULT_VIRTUAL_USER_CONFIG_DIR/vuser.db
chmod 600 $DEFAULT_VIRTUAL_USER_CONFIG_DIR/vuser

# 
if [ -f "$DEFAULT_PAMD_FILE" ]; then 
    rm -rf $DEFAULT_PAMD_FILE
fi

touch $DEFAULT_PAMD_FILE

echo    "#%PAM-1.0"                                                                                                              >             $DEFAULT_PAMD_FILE
echo    "auth    sufficient      pam_userdb.so db=/etc/vsftpd/vuser_config/vuser"                                                >>            $DEFAULT_PAMD_FILE
echo    "account sufficient      pam_userdb.so db=/etc/vsftpd/vuser_config/vuser"                                                >>            $DEFAULT_PAMD_FILE
echo    "session    optional     pam_keyinit.so    force revoke"                                                                 >>            $DEFAULT_PAMD_FILE
echo    "auth       required     pam_listfile.so item=user sense=deny file=/etc/vsftpd/ftpusers onerr=succeed"                   >>            $DEFAULT_PAMD_FILE
echo    "auth       required     pam_shells.so"                                                                                  >>            $DEFAULT_PAMD_FILE
echo    "auth       include      password-auth"                                                                                  >>            $DEFAULT_PAMD_FILE
echo    "account    include      password-auth"                                                                                  >>            $DEFAULT_PAMD_FILE
echo    "session    required     pam_loginuid.so"                                                                                >>            $DEFAULT_PAMD_FILE
echo    "session    include      password-auth"                                                                                  >>            $DEFAULT_PAMD_FILE

# Generate the user right options
if [ -f "$DEFAULT_VIRTUAL_USER_CONFIG_DIR/$FTP_USER_NAME" ]; then
    rm -rf $DEFAULT_VIRTUAL_USER_CONFIG_DIR/$FTP_USER_NAME
fi

touch $DEFAULT_VIRTUAL_USER_CONFIG_DIR/$FTP_USER_NAME

echo    "local_root=$FTP_DATA_DIR"                                                                                               >             $DEFAULT_VIRTUAL_USER_CONFIG_DIR/$FTP_USER_NAME
echo    "anonymous_enable=NO"                                                                                                    >>            $DEFAULT_VIRTUAL_USER_CONFIG_DIR/$FTP_USER_NAME
echo    "write_enable=YES"                                                                                                       >>            $DEFAULT_VIRTUAL_USER_CONFIG_DIR/$FTP_USER_NAME
echo    "local_umask=022"                                                                                                        >>            $DEFAULT_VIRTUAL_USER_CONFIG_DIR/$FTP_USER_NAME
echo    "anon_upload_enable=NO"                                                                                                  >>            $DEFAULT_VIRTUAL_USER_CONFIG_DIR/$FTP_USER_NAME
echo    "anon_mkdir_write_enable=NO"                                                                                             >>            $DEFAULT_VIRTUAL_USER_CONFIG_DIR/$FTP_USER_NAME
echo    "idle_session_timeout=600"                                                                                               >>            $DEFAULT_VIRTUAL_USER_CONFIG_DIR/$FTP_USER_NAME
echo    "data_connection_timeout=120"                                                                                            >>            $DEFAULT_VIRTUAL_USER_CONFIG_DIR/$FTP_USER_NAME
echo    "max_clients=10"                                                                                                         >>            $DEFAULT_VIRTUAL_USER_CONFIG_DIR/$FTP_USER_NAME
echo    "max_per_ip=5"                                                                                                           >>            $DEFAULT_VIRTUAL_USER_CONFIG_DIR/$FTP_USER_NAME
echo    "local_max_rate=1048576"                                                                                                 >>            $DEFAULT_VIRTUAL_USER_CONFIG_DIR/$FTP_USER_NAME

# Generate the chroot_list content
if [ -f "$DEFAULT_CHROOT_LIST" ]; then
    rm -rf $DEFAULT_CHROOT_LIST
fi

touch $DEFAULT_CHROOT_LIST

echo   "$DEFAULT_SYS_USER $FTP_DATA_DIR"                       >             $DEFAULT_CHROOT_LIST

# Add user virtual to user_list
echo   "$DEFAULT_SYS_USER"                                     >>            $DEFAULT_USER_LIST

# Restart and stop the vsftpd service
service vsftpd restart
service vsftpd stop
