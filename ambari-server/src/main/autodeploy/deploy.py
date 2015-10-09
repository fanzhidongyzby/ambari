#!/usr/bin/python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import commands
import time
import socket
import fileinput
import json

from command import *
from log import logger

def exe(cmd, test = False):
  logger.debug("RUNING command: {0}".format(cmd))
  # str = raw_input("confirm to continue(Y/no): ")
  # if str == "no":
  #   sys.exit(0)
  (status, output) = commands.getstatusoutput(cmd)
  if not test:
    if status != 0:
      logger.error("command exec error, return code = {0}".format(status))
      logger.error(output)
      sys.exit(-1)
    logger.debug(output)
    return output
  else:
    return status == 0, output

def readHosts(path):
  lines = []
  for line in fileinput.input(path):
    line = line.strip()
    if (line == ""):
      continue

    colNum = len(line.split())
    if colNum == 1:
      line += " tencent tencent"
    elif colNum == 2:
      line += " tencent"

    lines.append(line)

  if len(lines) == 0:
    logger.error("host config error, no host defined in file {0}".format(path))
    sys.exit(-1)

  return lines


def initCommand():
  cmd = Command()
  # cmd.addOption(Option("port", defaultValue = "8080", shortName = "-P")) # user name
  # cmd.addOption(Option("user", defaultValue = "admin")) # user name
  # cmd.addOption(Option("password", defaultValue = "admin")) # user password
  cmd.user = "admin"
  cmd.password = "admin"
  cmd.port = "8080"

  cmd.addOption(Option("repo", optional = False, comment = "set yum repo url")) # yum repo url

  cmd.addOption(Option("hosts", optional = False, shortName = "-H", comment = "set host list file name in directory hosts")) # host ip, user, password

  cmd.addOption(Option("license", optional = False, comment = "add product license")) # license key

  cmd.addOption(Option("case", optional = False, shortName = "-c", comment = "select bigdata product case")) # cases

  cmd.parse()

  if cmd.version:
    print "tbds deploy tools: version 1.0.0"
    sys.exit(0)
  elif cmd.help:
    print cmd.helpInfo()
    sys.exit(0)

  logger.debug(cmd)
  return cmd

# ./deploy.py -r 10.149.25.14:8080/hdp-mirror -H hosts-test -l "NJSXE4TZ-NJ5GQYLO-M4WTCMBN-GIYDCNRP-GA3C6MZQ" -c minimal
if __name__ == '__main__':

  me = exe("whoami")
  if me != "root":
    logger.error("you need root privalege to run this command")
    sys.exit(-1)

  # init command options
  try:
    cmd = initCommand()
  except Exception, e:
    logger.error(e)
    sys.exit(-1)

  # read hosts list
  hosts = readHosts("hosts/" + cmd.hosts)
  logger.debug("get host list: {0}".format(hosts))
  
  ######################################################################################################

  # install server
  logger.info("Installing tbds-server ...")
  exe("yum install -y tbds-server")

  # change port

  # change username and password

  # setup
  logger.info("Seting up tbds-server with yum repo: {0}".format(cmd.repo))
  exe("tbds-server setup --repo-url={0}".format(cmd.repo))

  # start
  logger.info("Starting tbds-server ...")
  exe("tbds-server start")


  ######################################################################################################

  # perpare REST command template
  curl = "curl --user {0}:{1} -H 'X-Requested-By:{0}' {2} 'http://0.0.0.0:{3}/api/v1{4}' 2> /dev/null".format(cmd.user, cmd.password, "{0}", cmd.port, "{1}")
  curlGet = curl.format("", "{0}")
  curlPost = curl.format("-d '{0}'", "{1}")
  curlPostJson = curl.format("-H 'Content-type:application/json' -d '{0}'", "{1}")
  curlPut = curl.format("-X PUT", "{0}")
  curlDelete = curl.format("-X DELETE", "{0}")

  logger.info("Waiting tbds-server to be ready ...")
  counter = 0
  while True:
    (ready, info) = exe(curlGet.format("/hosts"), test = True)
    if not ready:
      time.sleep(1)
      counter += 1
      if counter > 30:
        logger.error("Waiting tbds-server ready timeout !")
        sys.exit(-1)
    else:
      break


  ######################################################################################################
  logger.info("Adding license {0} to cluster".format(cmd.license))

  # save license
  exe(curlPost.format(cmd.license, "/license"))

  ######################################################################################################

  logger.info("Registering hosts configured in {0}".format(cmd.hosts))
  # send request to add hosts: {"status":"OK","log":"Running Bootstrap now.","requestId":1}
  addHostsBody = {"verbose": True, "sshKey":"", "hosts": hosts, "user": "root", "userRunAs": "root"}
  addHostsRequest = json.loads(exe(curlPostJson.format(json.dumps(addHostsBody), "/bootstrap")))
  if addHostsRequest.get("status") != "OK":
    logger.error("add hosts request send to server failed")
    sys.exit(-1)
  requestId = addHostsRequest.get("requestId")

  # watching the request to finish SUCCUSS
  while True:
    # {"status":"ERROR","hostsStatus":[{"hostName":"10.151.0.12","status":"DONE","statusCode":"0","log":""}]}
    addHostsRequestInfo = json.loads(exe(curlGet.format("/bootstrap/" + str(requestId))))
    status = addHostsRequestInfo.get("status")
    if status == "RUNNING":
      time.sleep(5)
    elif status == "ERROR":
      hostsStatus = addHostsRequestInfo.get("hostsStatus")
      if hostsStatus:
        for host in hostsStatus:
          if host.get("status") == "FAILED":
            hostName = host.get("hostName")
            log = host.get("log")
            logger.error("\nHost {0} add failed, log:\n{1}".format(hostName, log))
      else:
        logger.error("Hosts add failed")
      sys.exit(-1)
    elif status == "SUCCESS":
      break

  ######################################################################################################

  logger.info("Running blueprint to install tbds case {0}".format(cmd.case))
  # cluster prepare ok, use blueprint to install
  exe("./blueprint.sh cases/{0} {1} {2} {3}".format(cmd.case, cmd.port, cmd.user, cmd.password))

  ######################################################################################################

  logger.info("Waiting the cluster to be started ...")
  # get the only clusterName
  clusters = json.loads(exe(curlGet.format("/clusters"))).get("items")
  if len(clusters) != 1:
    logger.error("only-but one cluster created by blueprint")
    sys.exit(-1)

  clusterName = clusters[0].get("Clusters").get("cluster_name")

  # get the only request
  requests = json.loads(exe(curlGet.format("/clusters/{0}/requests".format(clusterName)))).get("items")
  if len(requests) != 1:
    logger.error("only-but one request could exist in cluster {0}".format(clusterName))
    sys.exit(-1)

  # check install complete
  href = "/clusters/{0}/requests/{1}".format(clusterName, requests[0].get("Requests").get("id"))
  bar = '''i={0}; echo -en "\\033[1A"; echo -n "[{1}: $i%] "; for((j=0;j<i;j++)); do echo -n "="; done; echo'''
  clusterReady = None
  print ""
  while True:
    request = json.loads(exe(curlGet.format(href))).get("Requests")
    title = request.get("request_context")
    percent = int(request.get("progress_percent"))
    status = request.get("request_status")

    if status == "IN_PROGRESS" or status == "PENDING":
      time.sleep(60)
    elif status == "COMPLETED":
      clusterReady = True
    else:
      logger.error("Excepted status {0} returned when install cluster {1}".format(status, clusterName))
      clusterReady = False

    print exe(bar.format(percent, title))

    if clusterReady != None:
      break

  localhost = socket.gethostbyname(socket.gethostname())
  webUrl = exe("echo -e '{0}:{1} @ \\033[4mhttp://{2}:{3}\\033[0m'".format(cmd.user, cmd.password, localhost, cmd.port))
  if clusterReady == False:
    logger.error("cluster {0} start failed, open url: {1} to check cluster status, or use \"tbds-server clean\" command to remove cluster".format(clusterName, webUrl))
    sys.exit(-1)
  elif clusterReady == True:
    logger.info("cluster {0} started success, open url: {1} to visit tbds".format(clusterName, webUrl))

