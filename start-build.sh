#!/bin/bash

export AMBARI_BUILD_HOME=/data/home/docker_common/jerryjzhang/ambari-build

echo "Building $1"

docker run -it --rm -v $1:/ambari \
    -v $AMBARI_BUILD_HOME/m2:/root/.m2 \
    -v $AMBARI_BUILD_HOME/ambari-web/node_modules:/ambari/ambari-web/node_modules \
    -v $AMBARI_BUILD_HOME/ambari-admin/node_modules:/ambari/ambari-admin/src/main/resources/ui/admin-web/node_modules \
    -v $AMBARI_BUILD_HOME/ambari-admin/node:/ambari/ambari-admin/src/main/resources/ui/admin-web/node \
    -w /ambari \
    --entrypoint /bin/bash \
    docker.oa.com:8080/ambari/build:1.7.0
