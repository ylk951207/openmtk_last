#!/bin/sh
docker run -d \
	--name net-snmp.$1 \
	-e "ARGS=$2" \
	-v /bin:/bin \
	-v /dev:/dev \
	-v /etc:/etc \
	-v /lib:/lib \
	-v /sbin:/sbin \
	-v /tmp:/tmp \
	-v /usr:/usr \
	-v /var:/var \
	--network host --privileged net-snmp:$1
