#!/usr/bin/env python

'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import optparse
import sys
import os
import signal

from ambari_commons.exceptions import FatalException, NonFatalException
from ambari_commons.logging_utils import set_verbose, set_silent, \
  print_info_msg, print_warning_msg, print_error_msg, set_debug_mode_from_options
from ambari_commons.os_check import OSConst
from ambari_commons.os_family_impl import OsFamilyFuncImpl, OsFamilyImpl
from ambari_commons.os_utils import remove_file
from ambari_server.BackupRestore import main as BackupRestore_main
from ambari_server.dbConfiguration import DATABASE_NAMES
from ambari_server.serverConfiguration import configDefaults, get_ambari_properties, PID_NAME
from ambari_server.serverUtils import is_server_runing, refresh_stack_hash
from ambari_server.serverSetup import reset, setup, setup_jce_policy
from ambari_server.serverUpgrade import upgrade, upgrade_stack, set_current
from ambari_server.setupHttps import setup_https

from ambari_server.setupActions import BACKUP_ACTION, LDAP_SETUP_ACTION, LDAP_SYNC_ACTION, PSTART_ACTION, \
  REFRESH_STACK_HASH_ACTION, RESET_ACTION, RESTORE_ACTION, SETUP_ACTION, SETUP_SECURITY_ACTION, START_ACTION, \
  STATUS_ACTION, STOP_ACTION, UPGRADE_ACTION, UPGRADE_STACK_ACTION, SETUP_JCE_ACTION, SET_CURRENT
from ambari_server.setupSecurity import setup_ldap, sync_ldap, setup_master_key, setup_ambari_krb5_jaas
from ambari_server.userInput import get_validated_string_input

from ambari_server_main import server_process_main


class UserActionPossibleArgs(object):
  def __init__(self, i_fn, i_possible_args_numbers, *args, **kwargs):
    self.fn = i_fn
    self.possible_args_numbers = i_possible_args_numbers
    self.args = args
    self.kwargs = kwargs
    self.need_restart = False

  def execute(self):
    self.fn(*self.args, **self.kwargs)

class UserAction(UserActionPossibleArgs):
  def __init__(self, i_fn, *args, **kwargs):
    super(UserAction, self).__init__(i_fn, [1], *args, **kwargs)

class UserActionRestart(UserAction):
  def __init__(self, i_fn, *args, **kwargs):
    super(UserActionRestart, self).__init__(i_fn, *args, **kwargs)

  def execute(self):
    self.need_restart = self.fn(*self.args, **self.kwargs)


def winsetup(options):
  from ambari_windows_service import svcsetup

  setup(options)
  svcsetup()

#
# Starts the TBDS Server as a standalone process.
# Ensures only one instance of the process is running.
#     If this is the second instance of the process, the function fails.
#
@OsFamilyFuncImpl(OSConst.WINSRV_FAMILY)
def start(options):
  from ambari_windows_service import AmbariServerService, ctrlHandler

  status, pid = is_server_runing()
  if status:
    err = "TBDS Server is already running."
    raise FatalException(1, err)

  AmbariServerService.set_ctrl_c_handler(ctrlHandler)

  #Run as a normal process. Invoke the ServiceMain directly.
  childProc = server_process_main(options)

  childProc.wait()

  pid_file_path = os.path.join(configDefaults.PID_DIR, PID_NAME)
  remove_file(pid_file_path)

#
# Starts the TBDS Server.
# Ensures only one instance of the process is running.
#     If this is the second instance of the process, the function fails.
#
@OsFamilyFuncImpl(OsFamilyImpl.DEFAULT)
def start(args):
  status, pid = is_server_runing()
  if status:
    err = "TBDS Server is already running."
    raise FatalException(1, err)

  server_process_main(args)


#
# Starts the TBDS Server as a service.
# Start the server as a Windows service. If the TBDS Server is
#     not registered as a service, the function fails. By default, only one instance of the service can
#     possibly run.
#
def svcstart():
  from ambari_windows_service import AmbariServerService

  AmbariServerService.Start()
  pass


#
# Stops the TBDS Server service.
#
@OsFamilyFuncImpl(OSConst.WINSRV_FAMILY)
def stop():
  from ambari_windows_service import AmbariServerService

  AmbariServerService.Stop()

#
# Stops the TBDS Server.
#
@OsFamilyFuncImpl(OsFamilyImpl.DEFAULT)
def stop(args):
  if (args != None):
    args.exit_message = None

  status, pid = is_server_runing()

  if status:
    try:
      os.kill(pid, signal.SIGKILL)
    except OSError, e:
      print_info_msg("Unable to stop TBDS Server - " + str(e))
      return
    pid_file_path = os.path.join(configDefaults.PID_DIR, PID_NAME)
    os.remove(pid_file_path)
    print "TBDS Server stopped"
  else:
    print "TBDS Server is not running"


#
# The TBDS Server status.
#
@OsFamilyFuncImpl(OSConst.WINSRV_FAMILY)
def status(args):
  from ambari_windows_service import AmbariServerService

  args.exit_message = None

  statusStr = AmbariServerService.QueryStatus()
  print "TBDS Server is " + statusStr

#
# The TBDS Server status.
#
@OsFamilyFuncImpl(OsFamilyImpl.DEFAULT)
def status(args):
  args.exit_message = None
  status, pid = is_server_runing()
  pid_file_path = os.path.join(configDefaults.PID_DIR, PID_NAME)
  if status:
    print "TBDS Server running"
    print "Found TBDS Server PID: " + str(pid) + " at: " + pid_file_path
  else:
    print "TBDS Server not running. Stale PID File at: " + pid_file_path


def refresh_stack_hash_action():
  properties = get_ambari_properties()
  refresh_stack_hash(properties)


@OsFamilyFuncImpl(OSConst.WINSRV_FAMILY)
def create_setup_security_actions(args):
  action_list = [
      ['Enable HTTPS for TBDS Server.', UserActionRestart(setup_https, args)],
      ['Encrypt passwords stored in tbds.properties file.', UserAction(setup_master_key)],
      ['Setup TBDS kerberos JAAS configuration.', UserAction(setup_ambari_krb5_jaas)],
  ]
  return action_list

@OsFamilyFuncImpl(OsFamilyImpl.DEFAULT)
def create_setup_security_actions(args):
  action_list = [
      ['Enable HTTPS for TBDS Server.', UserActionRestart(setup_https, args)],
      ['Encrypt passwords stored in tbds.properties file.', UserAction(setup_master_key)],
      ['Setup TBDS kerberos JAAS configuration.', UserAction(setup_ambari_krb5_jaas)],
  ]
  return action_list

def setup_security(args):
  actions = create_setup_security_actions(args)

  #Print menu options
  print '=' * 75
  print 'Choose one of the following options: '

  iAction = 0
  for actionDesc in actions:
    iAction += 1
    print '  [{0}] {1}'.format(iAction, actionDesc[0])
  print '=' * 75

  choice_prompt = 'Enter choice, (1-{0}): '.format(iAction)
  choice_re = '[1-{0}]'.format(iAction)
  choice = get_validated_string_input(choice_prompt, '0', choice_re,
                                      'Invalid choice', False, False)

  try:
    actionDesc = actions[int(choice) - 1]
  except IndexError:
    raise FatalException('Unknown option for setup-security command.')

  action = actionDesc[1]
  action.execute()

  return action.need_restart


#
# Backup / Restore
#
def get_backup_path(args):
  if len(args) == 2:
    path = args[1]
  else:
    path = None
  return path

def backup(args):
  print "Backup requested."
  backup_command = ["BackupRestore", 'backup']
  path = get_backup_path(args)
  if not path is None:
    backup_command.append(path)

  BackupRestore_main(backup_command)

def restore(args):
  print "Restore requested."
  restore_command = ["BackupRestore", 'restore']
  path = get_backup_path(args)
  if not path is None:
    restore_command.append(path)

  BackupRestore_main(restore_command)


@OsFamilyFuncImpl(OSConst.WINSRV_FAMILY)
def init_parser_options(parser):
  parser.add_option('-f', '--init-script-file', dest="init_db_script_file",
                    default="resources" + os.sep + "Ambari-DDL-SQLServer-CREATE.sql",
                    help="File with database setup script")
  parser.add_option('-r', '--drop-script-file', dest="cleanup_db_script_file",
                    default="resources" + os.sep + "Ambari-DDL-SQLServer-DROP.sql",
                    help="File with database cleanup script")
  parser.add_option('-j', '--java-home', dest="java_home", default=None,
                    help="Use specified java_home.  Must be valid on all hosts")
  parser.add_option("-v", "--verbose",
                    action="store_true", dest="verbose", default=False,
                    help="Print verbose status messages")
  parser.add_option("-s", "--silent",
                    action="store_true", dest="silent", default=False,
                    help="Silently accepts default prompt values")
  parser.add_option('-g', '--debug', action="store_true", dest='debug', default=False,
                    help="Start tbds-server in debug mode")
  parser.add_option('-y', '--suspend-start', action="store_true", dest='suspend_start', default=False,
                    help="Freeze tbds-server Java process at startup in debug mode")

  parser.add_option('-a', '--databasehost', dest="database_host", default=None,
                    help="Hostname of database server")
  parser.add_option('-n', '--databaseport', dest="database_port", default=None,
                    help="Database server listening port")
  parser.add_option('-d', '--databasename', dest="database_name", default=None,
                    help="Database/Schema/Service name or ServiceID")
  parser.add_option('-w', '--windowsauth', action="store_true", dest="database_windows_auth", default=None,
                    help="Integrated Windows authentication")
  parser.add_option('-u', '--databaseusername', dest="database_username", default=None,
                    help="Database user login")
  parser.add_option('-p', '--databasepassword', dest="database_password", default=None,
                    help="Database user password")
  parser.add_option('--jdbc-driver', default=None, dest="jdbc_driver",
                    help="Specifies the path to the JDBC driver JAR file")
  parser.add_option('--repo-url', default=None, dest="repo_url",
                    help="Specifies the path to YUM repo url")
  parser.add_option('--hostname', default=None, dest="hostname",
                    help="Specifies the hostname")

  parser.add_option('--use-default', default="yes", dest="use_default",
                      help="use default value to setup yes, no")

  # -b, -i, -k and -x the remaining available short options
  # -h reserved for help

@OsFamilyFuncImpl(OsFamilyImpl.DEFAULT)
def init_parser_options(parser):
  optparse.Option('-f', '--init-script-file',
                    default='/var/lib/tbds-server/'
                            'resources/Ambari-DDL-Postgres-EMBEDDED-CREATE.sql',
                    help="File with setup script")
  parser.add_option('-r', '--drop-script-file', default="/var/lib/"
                                                        "tbds-server/resources/"
                                                        "Ambari-DDL-Postgres-EMBEDDED-DROP.sql",
                    help="File with drop script")
  parser.add_option('-u', '--upgrade-script-file', default="/var/lib/"
                                                           "tbds-server/resources/upgrade/ddl/"
                                                           "Ambari-DDL-Postgres-UPGRADE-1.3.0.sql",
                    help="File with upgrade script")
  parser.add_option('-t', '--upgrade-stack-script-file', default="/var/lib/"
                                                                 "tbds-server/resources/upgrade/dml/"
                                                                 "Ambari-DML-Postgres-UPGRADE_STACK.sql",
                    help="File with stack upgrade script")
  parser.add_option('-j', '--java-home', default=None,
                    help="Use specified java_home.  Must be valid on all hosts")
  parser.add_option("-v", "--verbose",
                    action="store_true", dest="verbose", default=False,
                    help="Print verbose status messages")
  parser.add_option("-s", "--silent",
                    action="store_true", dest="silent", default=False,
                    help="Silently accepts default prompt values")
  parser.add_option('-g', '--debug', action="store_true", dest='debug', default=False,
                    help="Start tbds-server in debug mode")
  parser.add_option('-y', '--suspend-start', action="store_true", dest='suspend_start', default=False,
                    help="Freeze tbds-server Java process at startup in debug mode")
  parser.add_option('--all', action="store_true", default=False, help="LDAP sync all option.  Synchronize all LDAP users and groups.",
                    dest="ldap_sync_all")
  parser.add_option('--existing', action="store_true", default=False,
                    help="LDAP sync existing option.  Synchronize existing TBDS users and groups only.", dest="ldap_sync_existing")
  parser.add_option('--users', default=None, help="LDAP sync users option. Specifies the path to a CSV file of user names to be synchronized.",
                    dest="ldap_sync_users")
  parser.add_option('--groups', default=None, help="LDAP sync groups option.  Specifies the path to a CSV file of group names to be synchronized.",
                    dest="ldap_sync_groups")
  parser.add_option('--database', default=None, help="Database to use embedded|oracle|mysql|postgres", dest="dbms")
  parser.add_option('--databasehost', default=None, help="Hostname of database server", dest="database_host")
  parser.add_option('--databaseport', default=None, help="Database port", dest="database_port")
  parser.add_option('--databasename', default=None, help="Database/Service name or ServiceID",
                    dest="database_name")
  parser.add_option('--postgresschema', default=None, help="Postgres database schema name",
                    dest="postgres_schema")
  parser.add_option('--databaseusername', default=None, help="Database user login", dest="database_username")
  parser.add_option('--databasepassword', default=None, help="Database user password", dest="database_password")
  parser.add_option('--sidorsname', default="sname", help="Oracle database identifier type, Service ID/Service "
                                                          "Name sid|sname", dest="sid_or_sname")
  parser.add_option('--jdbc-driver', default=None, help="Specifies the path to the JDBC driver JAR file for the " \
                                                        "database type specified with the --jdbc-db option. Used only with --jdbc-db option.",
                    dest="jdbc_driver")
  parser.add_option('--jdbc-db', default=None, help="Specifies the database type [postgres|mysql|oracle] for the " \
                                                    "JDBC driver specified with the --jdbc-driver option. Used only with --jdbc-driver option.",
                    dest="jdbc_db")
  parser.add_option('--cluster-name', default=None, help="Cluster name", dest="cluster_name")
  parser.add_option('--version-display-name', default=None, help="Display name of desired repo version", dest="desired_repo_version")
  parser.add_option('--repo-url', default=None, dest="repo_url",
                    help="Specifies the path to YUM repo url")
  parser.add_option('--hostname', default=None, dest="hostname",
                    help="Specifies the hostname")

  parser.add_option('--use-default', default="yes", dest="use_default",
                      help="use default value to setup yes, no")


@OsFamilyFuncImpl(OSConst.WINSRV_FAMILY)
def are_cmd_line_db_args_blank(options):
  if (options.database_host is None \
          and options.database_name is None \
          and options.database_windows_auth is None \
          and options.database_username is None \
          and options.database_password is None):
    return True
  return False

@OsFamilyFuncImpl(OsFamilyImpl.DEFAULT)
def are_cmd_line_db_args_blank(options):
  if options.dbms is None \
      and options.database_host is None \
      and options.database_port is None \
      and options.database_name is None \
      and options.database_username is None \
      and options.database_password is None:
    return True
  return False


def are_db_auth_options_ok(db_windows_auth, db_username, db_password):
  if db_windows_auth is True:
    return True
  else:
    if db_username is not None and db_username is not "" and db_password is not None and db_password is not "":
      return True
  return False

@OsFamilyFuncImpl(OSConst.WINSRV_FAMILY)
def are_cmd_line_db_args_valid(options):
  if (options.database_host is not None and options.database_host is not "" \
      #and options.database_name is not None \         # tbds by default is ok
      and are_db_auth_options_ok(options.database_windows_auth,
                                 options.database_username,
                                 options.database_password)):
    return True
  return False

@OsFamilyFuncImpl(OsFamilyImpl.DEFAULT)
def are_cmd_line_db_args_valid(options):
  if options.dbms is not None \
      and options.database_host is not None \
      and options.database_port is not None \
      and options.database_name is not None \
      and options.database_username is not None \
      and options.database_password is not None:
    return True
  return False


@OsFamilyFuncImpl(OSConst.WINSRV_FAMILY)
def init_debug(options):
  if options.debug:
    sys.frozen = 'windows_exe' # Fake py2exe so we can debug

@OsFamilyFuncImpl(OsFamilyImpl.DEFAULT)
def init_debug(options):
  pass


@OsFamilyFuncImpl(OSConst.WINSRV_FAMILY)
def fix_database_options(options, parser):
  pass

@OsFamilyFuncImpl(OsFamilyImpl.DEFAULT)
def fix_database_options(options, parser):
  if options.dbms == 'embedded':
    print "WARNING: HostName for postgres server " + options.database_host + \
          " will be ignored: using localhost."
    options.database_host = "localhost"
    options.dbms = 'postgres'
    options.persistence_type = 'local'
    options.database_index = 0
  elif options.dbms is not None and options.dbms not in DATABASE_NAMES:
    parser.print_help()
    parser.error("Unsupported Database " + options.dbms)
  elif options.dbms is not None:
    options.dbms = options.dbms.lower()

  # correct port
  if options.database_port is not None:
    correct = False
    try:
      port = int(options.database_port)
      if 65536 > port > 0:
        correct = True
    except ValueError:
      pass
    if not correct:
      parser.print_help()
      parser.error("Incorrect database port " + options.database_port)

  # jdbc driver and db options validation
  if options.jdbc_driver is None and options.jdbc_db is not None:
    parser.error("Option --jdbc-db is used only in pair with --jdbc-driver")
  elif options.jdbc_driver is not None and options.jdbc_db is None:
    parser.error("Option --jdbc-driver is used only in pair with --jdbc-db")
  if options.sid_or_sname.lower() not in ["sid", "sname"]:
    print "WARNING: Valid values for sid_or_sname are 'sid' or 'sname'. Use 'sid' if the db identifier type is " \
          "Service ID. Use 'sname' if the db identifier type is Service Name"
    parser.print_help()
    exit(-1)
  else:
    options.sid_or_sname = options.sid_or_sname.lower()


@OsFamilyFuncImpl(OSConst.WINSRV_FAMILY)
def create_user_action_map(args, options):
  action_map = {
    SETUP_ACTION: UserAction(winsetup, options),
    START_ACTION: UserAction(svcstart),
    PSTART_ACTION: UserAction(start, options),
    STOP_ACTION: UserAction(stop),
    RESET_ACTION: UserAction(reset, options),
    STATUS_ACTION: UserAction(status, options),
    UPGRADE_ACTION: UserAction(upgrade, options),
    LDAP_SETUP_ACTION: UserAction(setup_ldap),
    SETUP_SECURITY_ACTION: UserActionRestart(setup_security, options),
  }
  return action_map

@OsFamilyFuncImpl(OsFamilyImpl.DEFAULT)
def create_user_action_map(args, options):
  action_map = {
        SETUP_ACTION: UserAction(setup, options),
        SETUP_JCE_ACTION : UserActionPossibleArgs(setup_jce_policy, [2], args),
        START_ACTION: UserAction(start, options),
        STOP_ACTION: UserAction(stop, options),
        RESET_ACTION: UserAction(reset, options),
        STATUS_ACTION: UserAction(status, options),
        UPGRADE_ACTION: UserAction(upgrade, options),
        UPGRADE_STACK_ACTION: UserActionPossibleArgs(upgrade_stack, [2, 4], args),
        LDAP_SETUP_ACTION: UserAction(setup_ldap),
        LDAP_SYNC_ACTION: UserAction(sync_ldap, options),
        SET_CURRENT: UserAction(set_current, options),
        SETUP_SECURITY_ACTION: UserActionRestart(setup_security, options),
        REFRESH_STACK_HASH_ACTION: UserAction(refresh_stack_hash_action),
        BACKUP_ACTION: UserActionPossibleArgs(backup, [1, 2], args),
        RESTORE_ACTION: UserActionPossibleArgs(restore, [1, 2], args)
      }
  return action_map


#
# Main.
#
def main(options, args, parser):
  # set silent
  set_silent(options.silent)

  # debug mode
  set_debug_mode_from_options(options)
  init_debug(options)

  #perform checks

  options.warnings = []

  if are_cmd_line_db_args_blank(options):
    options.must_set_database_options = True
  elif not are_cmd_line_db_args_valid(options):
    parser.error('All database options should be set. Please see help for the options.')
  else:
    options.must_set_database_options = False

  #correct database
  fix_database_options(options, parser)

  if len(args) == 0:
    print parser.print_help()
    parser.error("No action entered")

  action_map = create_user_action_map(args, options)

  action = args[0]

  if action == "setup" and options.repo_url is None:
      parser.error("--repo-url must be given")

  try:
    action_obj = action_map[action]
  except KeyError:
    parser.error("Invalid action: " + action)

  matches = 0
  for args_number_required in action_obj.possible_args_numbers:
    matches += int(len(args) == args_number_required)

  if matches == 0:
    print parser.print_help()
    possible_args = ' or '.join(str(x) for x in action_obj.possible_args_numbers)
    parser.error("Invalid number of arguments. Entered: " + str(len(args)) + ", required: " + possible_args)

  options.exit_message = "TBDS Server '%s' completed successfully." % action

  try:
    action_obj.execute()

    if action_obj.need_restart:
      pstatus, pid = is_server_runing()
      if pstatus:
        print 'NOTE: Restart TBDS Server to apply changes' + \
              ' ("tbds-server restart|stop+start")'

    if options.warnings:
      for warning in options.warnings:
        print_warning_msg(warning)
        pass
      options.exit_message = "TBDS Server '%s' completed with warnings." % action
      pass
  except FatalException as e:
    if e.reason is not None:
      print_error_msg("Exiting with exit code {0}. \nREASON: {1}".format(e.code, e.reason))
    sys.exit(e.code)
  except NonFatalException as e:
    options.exit_message = "TBDS Server '%s' completed with warnings." % action
    if e.reason is not None:
      print_warning_msg(e.reason)

  if options.exit_message is not None:
    print options.exit_message

def mainBody():
  parser = optparse.OptionParser(usage="usage: %prog [options] action [stack_id os]",)
  init_parser_options(parser)
  (options, args) = parser.parse_args()

  # set verbose
  set_verbose(options.verbose)
  if options.verbose:
    main(options, args, parser)
  else:
    try:
      main(options, args, parser)
    except Exception as e:
      print_error_msg("Unexpected {0}: {1}".format((e).__class__.__name__, str(e)) +\
      "\nFor more info run tbds-server with -v or --verbose option")
      sys.exit(1)


if __name__ == "__main__":
  try:
    mainBody()
  except (KeyboardInterrupt, EOFError):
    print("\nAborting ... Keyboard Interrupt.")
    sys.exit(1)
