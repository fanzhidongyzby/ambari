#!/usr/bin/expect
##############################################################
## @Company: TENCENT Tech. Co., Ltd.
## @Filename exeRemoteCmd.exp
## @Usage 	 execute remote command by ssh
## @Description execute remote command by ssh
## @Options 
## @History
## @Version V100R00C00
## @Created 2013.04.10
##############################################################

set cmdTimeout [lindex $argv 0]
set runCommand [lindex $argv 1]

spawn /bin/sh -c "${runCommand} && echo \\#SUCCESS\\# || echo \\#fail\\#"

set timeout ${cmdTimeout}
expect {
    "*yes/no)?" {send "yes\n"; exp_continue}
    "Yy|Nn (default=N):" {send "y\n"; exp_continue}
    "*Yy/Nn>" {send "y\n"; exp_continue}
    "*overriding mode 0664*" {send "\n"; exp_continue}
    "*overriding mode 0755*" {send "\n"; exp_continue}
    "Last login:" {}
    "#SUCCESS#" {}
    "#fail#" {exit 1 }
    "*No route to host" {exit 2}
    "Permission denied" {exit 3}
    "*Host key verification failed*" {exit 4}
    timeout { exit 5 }
    eof { exit 6 }
}