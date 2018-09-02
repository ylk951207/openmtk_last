#!/bin/sh
/bin/cp /dnsmasq-* /usr/sbin/dnsmasq
/dnsmasq.init start
/usr/sbin/dnsmasq -C /var/etc/dnsmasq.conf.cfg02411c -k -x /var/run/dnsmasq/dnsmasq.cfg02411c.pid
