from resource_management.libraries.script import Script
from resource_management.libraries.functions.default import default
# server configurations
config = Script.get_config()

# JAVA HOME
java_home = default("/hostLevelParams/java_home", "/usr/jdk64/jdk1.7.0_67")