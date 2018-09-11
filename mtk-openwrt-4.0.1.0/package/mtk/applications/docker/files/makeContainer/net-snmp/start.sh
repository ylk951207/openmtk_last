#!/bin/sh
/bin/cp -af /net-snmp-5.7.3/bin/* /usr/bin
/bin/cp -af /net-snmp-5.7.3/sbin/* /usr/sbin
/bin/cp -af /net-snmp-5.7.3/mibs/* /usr/share/snmp/mibs
/bin/cp -af /snmpd.conf /etc/config/snmpd
/snmpd.init start
/usr/sbin/snmpd -c /etc/snmp/snmpd.conf -Lf /dev/null -f
