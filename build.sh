#!/bin/sh

distVersion=2.4.0.0

mvn clean

#for i in `find . -type f -name "*ambari*" -or -name "*.py" -or -name "*.sh" -or -name "*.java" |grep -v .git | grep -v target |grep -v jar|grep -v png`;do dos2unix $i; done

rm -rf ambari-agent/target/ambari-agent-$distVersion/ambari_agent
rm -rf ambari-client/python-client/target/python-client-$distVersion/ambari_client
rm -rf ambari-shell/ambari-python-shell/target/ambari-python-shell-$distVersion/ambari_shell

mkdir -p ambari-agent/target/ambari-agent-$distVersion/
mkdir -p ambari-client/python-client/target/python-client-$distVersion/
mkdir -p ambari-shell/ambari-python-shell/target/ambari-python-shell-$distVersion/

cp -r ambari-agent/src/main/python/ambari_agent/  ambari-agent/target/ambari-agent-$distVersion/
cp -r ambari-client/python-client/src/main/python/ambari_client ambari-client/python-client/target/python-client-$distVersion/
cp -r ambari-shell/ambari-python-shell/src/main/python/ambari_shell ambari-shell/ambari-python-shell/target/ambari-python-shell-$distVersion/

ln -s ~/jerryjzhang/ambari-build/ambari-web/node_modules ambari-web/node_modules
ln -s ~/jerryjzhang/ambari-build/ambari-admin/node_modules ambari-admin/src/main/resources/ui/admin-web/node_modules
ln -s ~/jerryjzhang/ambari-build/ambari-admin/node ambari-admin/src/main/resources/ui/admin-web/node
ln -s ~/jerryjzhang/ambari-build/ambari-admin/target ambari-admin/target

mvn versions:set -DnewVersion=$distVersion
pushd ambari-metrics
mvn versions:set -DnewVersion=$distVersion
popd
mvn install package rpm:rpm -Dfindbugs.skip -DskipTests -Drat.skip -Dmaven.test.skip -DskipAssembly -DnewVersion=$distVersion -Dpython.ver="python >= 2.6" -X
# mvn install -pl ambari-agent package rpm:rpm -Dfindbugs.skip -DskipTests -Drat.skip -Dmaven.test.skip -DskipAssembly -DnewVersion=$distVersion -Dpython.ver="python >= 2.6" -X
