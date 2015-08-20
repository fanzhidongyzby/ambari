#!/usr/bin/env bash

bin=$(dirname "${BASH_SOURCE[0]}")
bin=$(cd "$bin"; pwd)

unset LOG
export LOG=/tmp/certificate.log

. ${bin}/supports.sh

ac_check_login_user "$LINENO" "gaia" "ac_cv_login_user_gaia"
if [[ "x$ac_cv_login_user_gaia" = xyes ]]; then :
else
  ac_exit "$LINENO" "1" "login user must be gaia"
fi

/usr/bin/env expect <<EOF
spawn docker login docker.oa.com:8080
expect "Username: " {
  send "gaia\r"
}
expect "Password: " {
  send "gaia4docker\r"
}
expect "Email: " {
  send "t_gaia_dev@tencent.com\r"
}
expect eof {
  exit
}
EOF

ac_check_file_existence "$LINENO" "$HOME/.dockercfg" "docker_cfg_found"
if [[ "x$docker_cfg_found" = xyes ]]; then :
  ac_exit "$LINENO" "0" "success of docker certification"
else
  ac_exit "$LINENO" "1" "failure of docker certification"
fi

