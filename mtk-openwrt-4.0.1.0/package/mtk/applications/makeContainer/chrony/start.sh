#!/bin/sh
/bin/cp /chrony.conf /etc/chrony/chrony.conf
/bin/cp /chronyc-* /usr/bin/chronyc
/bin/cp /chronyd-* /usr/sbin/chronyd
/chronyd.init start
/usr/sbin/chronyd -n -f /var/etc/chrony.conf
