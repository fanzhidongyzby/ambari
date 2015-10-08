#!/bin/bash
me=`whoami`
if [[ "$me" != "root" ]]; then
  echo "You need to be root privilege to run this test"
  exit 1
fi

echo "Before install a new cluster, old cluster will be clean ..."
tbds-server clean 

echo "Running one button deploy to install new cluster minimal ..."
./deploy.py -r 10.149.25.14:8080/hdp-mirror -H hosts-test -l "NJSXE4TZ-NJ5GQYLO-M4WTCMBN-GIYDCNRP-GA3C6MZQ" -c minimal

