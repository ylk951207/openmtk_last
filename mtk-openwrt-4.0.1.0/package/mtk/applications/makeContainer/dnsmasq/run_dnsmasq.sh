#!/bin/sh
if [ -z "$3" ]; then
	CONTAINER_PATH=""
else
	CONTAINER_PATH=$3/
fi

docker run -d \
	--name dnsmasq_$1 \
	-e "ARGS=$2" \
	-v /bin:/bin \
	-v /dev:/dev \
	-v /etc:/etc \
	-v /lib:/lib \
	-v /sbin:/sbin \
	-v /tmp:/tmp \
	-v /usr:/usr \
	-v /var:/var \
	--network host --privileged ${CONTAINER_PATH}dnsmasq:$1
