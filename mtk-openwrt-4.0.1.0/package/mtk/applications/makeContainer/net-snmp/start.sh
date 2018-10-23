#!/bin/sh
/bin/cp -af /net-snmp-*/bin/* /usr/bin 2>/dev/null
/bin/cp -af /net-snmp-*/sbin/* /usr/sbin 2>/dev/null
/bin/cp -af /net-snmp-*/mibs/* /usr/share/snmp/mibs 2>/dev/null
#/bin/cp -af /snmpd.conf /etc/config/snmpd
/snmpd.init start
echo "[start.sh] SNMP_ARGS is $SNMP_ARGS"
/usr/sbin/snmpd -a 0.0.0.0:$SNMP_ARGS -c /etc/snmp/snmpd.conf -Lf /dev/null -f
