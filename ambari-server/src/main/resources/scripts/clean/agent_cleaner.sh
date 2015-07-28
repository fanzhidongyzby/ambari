#!/bin/bash


echo "-------stop all services"
# get args
force=false
if [[ "$1" == "--force" ]]; then
	force=true
fi

# get server ip
server='127.0.0.1'

# get cluster name
cluster=`curl --user admin:admin http://$server:8080/api/v1/clusters 2> /dev/null | grep cluster_name | awk -F '"' '{print $4}'`

# stop all the services
request=`curl -H "ContentType:application/json" -H "X-rfequested-By: florianfan" -X PUT -d '{"ServiceInfo":{"state":"INSTALLED"}}' --user admin:admin http://$server:8080/api/v1/clusters/$cluster/services?ServiceInfo/state=STARTED 2> /dev/null | grep href | awk -F '"' '{print $4}' `

# stop flag
stop_ok=true

if [[ $request != "" ]]; then
	# wait services stopped
	echo -n "Stopping all the services"
	while true; do
		status=`curl --user admin:admin $request 2> /dev/null | grep request_status | awk -F '"' '{print $4}'`
		if [[ "$status" == "IN_PROGRESS" ]]; then
			echo -n \>
			sleep 5
		elif [[ "$status" == "COMPLETED" ]]; then
			echo -e "\nStoppong services success"
			break
		else
			echo -e "\nStopping services failed, status = $status"
			stop_ok=false
			break
		fi
	done

else
	if ! $force; then
		echo "Services maybe stopped, operation break. user option --force to continue"
		exit -1
	fi
	stop_ok=false;
fi


if ! $stop_ok; then
	if ! $force; then
		echo "Problem exists when stopping services, operation break. user option --force to continue"
		exit -1
	fi
	echo "Operation continue with problems exist ..."
fi



echo "-------get hosts info from tbds server"
> /var/lib/tbds-server/resources/scripts/clean/hosts
echo "get hosts"

clustername=`curl --user admin:admin "http://0.0.0.0:8080/api/v1/clusters?minimal_response=true" 2> /dev/null | grep cluster_name | awk -F':' '{print $2}' | sed  "s/[ \"]//g"`
echo $clustername

for host in `curl --user admin:admin "http://0.0.0.0:8080/api/v1/clusters/$clustername/hosts?minimal_response=true" 2> /dev/null | grep host_name | awk -F':' '{print $2}' | sed "s/[ \"]//g"`
do
  echo ${host} >> /var/lib/tbds-server/resources/scripts/clean/hosts
 
done
  

echo "----------clean agent"


BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`

loginUser="tencent"
loginPass="tencent"

if [ -d "/tmp/clean/" ]
then
   echo "/tmp/clean/ exist"
else
  sudo mkdir /tmp/clean
fi

count=10
for host in `cat hosts`
do
  ./service_cleaner.exp ${host} ${loginUser} ${loginPass} 1>>/tmp/clean/${host}.log 2>&1 &
  sleep 5
  p_num=`ps -wef|grep service_cleaner | grep -v grep -c`
  echo "$p_num:: ${host}"

  while [ $p_num -ge $count ]
  do
      echo "$count"
      p_num=`ps -wef|grep service_cleaner | grep -v grep -c`
      sleep 5
      echo "$p_num:: sleep 2s..."
  done
done
wait