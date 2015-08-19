#!/bin/sh


#for i in `find . -type f -name "*ambari*" -or -name "*.py" -or -name "*.sh" -or -name "*.java" |grep -v .git | grep -v target |grep -v jar|grep -v png`;do dos2unix $i; done

rm -rf ambari-agent/target/ambari-agent-2.1.1.0/ambari_agent/*
cp -r ambari-agent/src/main/python/ambari_agent/* ambari-agent/target/ambari-agent-2.1.1.0/ambari_agent

mvn versions:set -DnewVersion=2.1.1.0
pushd ambari-metrics
mvn versions:set -DnewVersion=2.1.1.0
popd
mvn install package rpm:rpm -Dfindbugs.skip -DskipTests -Drat.skip -Dmaven.test.skip -DskipAssembly -DnewVersion=2.1.1.0 -Dpython.ver="python >= 2.6" -X
