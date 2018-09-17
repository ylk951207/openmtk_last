#!/bin/sh
/bin/cp -af /net-snmp-*/bin/* /usr/bin
/bin/cp -af /net-snmp-*/sbin/* /usr/sbin
/bin/cp -af /net-snmp-*/mibs/* /usr/share/snmp/mibs
#/bin/cp -af /snmpd.conf /etc/config/snmpd
/snmpd.init start
/usr/sbin/snmpd -c /etc/snmp/snmpd.conf -Lf /dev/null -f
