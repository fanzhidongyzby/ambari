#!/bin/bash
status=$(tbds-server status | grep "not running" | wc -l)
if [[ "$status" == "1" ]]; then
  echo "server is stoped ..."
  exit -1
fi

echo "----------   STOP ALL THE SERVICES   ----------"
# get server ip
server='127.0.0.1'

# get cluster name
cluster=`curl --user admin:admin http://$server:8080/api/v1/clusters 2> /dev/null | grep cluster_name | awk -F '"' '{print $4}'`
echo "get cluster name = "$cluster

# stop all the services
echo "send request to stop all the service"
request=`curl -H "ContentType:application/json" -H "X-requested-By: florianfan" -X PUT -d '{"ServiceInfo":{"state":"INSTALLED"}}' --user admin:admin http://$server:8080/api/v1/clusters/$cluster/services?ServiceInfo/state=STARTED 2> /dev/null | grep href | awk -F '"' '{print $4}' `

# wait services stopped
echo "request sent ok, waiting services to be stopped ..."
if [[ "$request" != "" ]]; then
	# wait services stopped
	times=1
	while true; do
		status=`curl --user admin:admin $request 2> /dev/null | grep request_status | awk -F '"' '{print $4}'`
		if [[ "$status" == "IN_PROGRESS" || "$status" == "PENDING" ]]; then
			echo -n \>
			sleep 5
			times=$((times+1))
			if [[ $times -eq 60 ]]; then
			  echo -e "\nservices stopped timeout! please stop all the services manually."
			  exit 1
			fi
		elif [[ "$status" == "COMPLETED" ]]; then
			echo -e "\nservices stopped success !!!"
			break
		else
			echo -e "\nservices stopped failed, status = $status"
			exit 1
			break
		fi
	done
fi
echo "services stopped OK !"

echo "----------   CLEAN AGENTS ON ALL THE HOSTS  ----------"
> /var/lib/tbds-server/resources/scripts/clean/hosts
for host in `curl --user admin:admin "http://0.0.0.0:8080/api/v1/hosts?minimal_response=true" 2> /dev/null | grep host_name | awk -F':' '{print $2}' | sed "s/[ \"]//g"`
do
  echo ${host} >> /var/lib/tbds-server/resources/scripts/clean/hosts
done

echo "agents on following hosts will be cleaned:"
cat /var/lib/tbds-server/resources/scripts/clean/hosts

echo "begin to clean agents ..."
count=10
for host in `cat hosts`
do
  ./service_cleaner ${host} &>/dev/null &
  p_num=`ps -wef | grep service_cleaner | grep -v grep -c`
  echo "${host} is cleaning..."

  while [ $p_num -ge $count ]
  do
      p_num=`ps -wef | grep service_cleaner | grep -v grep -c`
      sleep 5
  done
done

echo "waiting agents cleaning over ..."

wait
echo "agents clean OK !"
