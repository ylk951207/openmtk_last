#!/bin/sh
docker run -d \
	--name chrony \
	--restart always \
	-v /bin:/bin \
	-v /dev:/dev \
	-v /etc:/etc \
	-v /lib:/lib \
	-v /sbin:/sbin \
	-v /tmp:/tmp \
	-v /usr:/usr \
	-v /var:/var \
	--network host --privileged chrony:$1
