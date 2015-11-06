from resource_management.libraries.script import Script
from resource_management.libraries.functions.default import default
# server configurations
config = Script.get_config()

#web ide
webide_host = default("/clusterHostInfo/web_ide_hosts", ["localhost"])[0]
webide_listen_port = default("/configurations/webide/listen.port", 80)
webide_app_listen_port = default("/configurations/webide/app.listen.port", 9090)

webide_web_url = "http://" + webide_host + ":" + str(webide_listen_port) + "/webide"
