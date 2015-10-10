#!/bin/sh

distVersion=2.4.0.0

cd ./ambari-metrics
mvn clean
mvn install package rpm:rpm -pl 'ambari-metrics-common' -pl 'ambari-metrics-host-monitoring' -o -Dfindbugs.skip -DskipTests -Drat.skip -Dmaven.test.skip -DskipAssembly -DnewVersion=$distVersion -Dpython.ver="python >= 2.6"
cd ..
