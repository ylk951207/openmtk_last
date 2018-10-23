'''
This file was automatically generated by rmib_compiler.py.
 DO NOT EDIT.
'''


from common.misc import *

CONFIG_TYPE_SCALAR=1
CONFIG_TYPE_LIST=2


def uci_get_section_map(config_name, *args):

  log_info(LOG_MODULE_SAL, "ARGS: " + str(args))

  if config_name == 'system_config_common':
      section_map = {
        'hostname'               :  [ CONFIG_TYPE_SCALAR  , 'system.@system[0].hostname'                 ,' ' ],
        'timezone'               :  [ CONFIG_TYPE_SCALAR  , 'system.@system[0].timezone'                 ,' ' ],
      }
      return section_map

  if config_name == 'system_config_logging':
      section_map = {
        'loggingBufferSize'      :  [ CONFIG_TYPE_SCALAR  , 'system.@system[0].log_size'                 ,' ' ],
        'loggingServerIpAddr'    :  [ CONFIG_TYPE_SCALAR  , 'system.@system[0].log_ip'                   ,' ' ],
        'loggingServerPort'      :  [ CONFIG_TYPE_SCALAR  , 'system.@system[0].log_port'                 ,' ' ],
        'loggingServerProtocol'  :  [ CONFIG_TYPE_SCALAR  , 'system.@system[0].log_proto'                ,' ' ],
        'loggingFilename'        :  [ CONFIG_TYPE_SCALAR  , 'system.@system[0].log_file'                 ,' ' ],
        'loggingOutputLevel'     :  [ CONFIG_TYPE_SCALAR  , 'system.@system[0].conloglevel'              ,' ' ],
        'loggingCronLogLevel'    :  [ CONFIG_TYPE_SCALAR  , 'system.@system[0].cronloglevel'              ,' ' ],
      }
      return section_map

  if config_name == 'system_config_ntp':
      section_map = {
        'enableNtpClient'        :  [ CONFIG_TYPE_SCALAR  , 'system.ntp.enabled'                         ,' ' ],
        'provideNtpServer'       :  [ CONFIG_TYPE_SCALAR  , 'system.ntp.enable_server'                   ,' ' ],
        'ntpServerCandidates'    :  [ CONFIG_TYPE_LIST    , 'system.ntp.server'                          ,' ' ],
      }
      return section_map

  if config_name == 'interface_config':
    if args and args[0]:
      section_map = {
        'portName'               :  [ CONFIG_TYPE_SCALAR  , ".".join(['network', args[0], 'ifname'])     ,' ' ],
        'protocol'               :  [ CONFIG_TYPE_SCALAR  , ".".join(['network', args[0], 'proto'])      ,' ' ],
        'type'                   :  [ CONFIG_TYPE_SCALAR  , ".".join(['network', args[0], 'type'])       ,' ' ],
        'stp'                    :  [ CONFIG_TYPE_SCALAR  , ".".join(['network', args[0], 'stp'])        ,' ' ],
        'igmpSnooping'           :  [ CONFIG_TYPE_SCALAR  , ".".join(['network', args[0], 'igmp_snooping']),' ' ],
        'macAddr'                :  [ CONFIG_TYPE_SCALAR  , ".".join(['network', args[0], 'macaddr'])    ,' ' ],
        'mtu'                    :  [ CONFIG_TYPE_SCALAR  , ".".join(['network', args[0], 'mtu'])        ,' ' ],
        'ipv6Enable'             :  [ CONFIG_TYPE_SCALAR  , ".".join(['network', args[0], 'ipv6'])       ,' ' ],
      }
      return section_map

  if config_name == 'interface_v4addr_config':
    if args and args[0]:
      section_map = {
        'ipv4Address'            :  [ CONFIG_TYPE_SCALAR  , ".".join(['network', args[0], 'ipaddr'])     ,' ' ],
        'ipv4Netmask'            :  [ CONFIG_TYPE_SCALAR  , ".".join(['network', args[0], 'netmask'])    ,' ' ],
        'ipv4Gateway'            :  [ CONFIG_TYPE_SCALAR  , ".".join(['network', args[0], 'gateway'])    ,' ' ],
        'ipv4Broadcast'          :  [ CONFIG_TYPE_SCALAR  , ".".join(['network', args[0], 'broadcast'])  ,' ' ],
        'dnsServer'              :  [ CONFIG_TYPE_LIST    , ".".join(['network', args[0], 'dns'])        ,' ' ],
      }
      return section_map

  if config_name == 'vlan_common_config':
      section_map = {
        'enableVlan'             :  [ CONFIG_TYPE_SCALAR  , 'network.@switch[0].enable_vlan'             ,' ' ],
      }
      return section_map

  if config_name == 'vlan_config':
    if args and args[0]:
      section_map = {
        'vlanId'                 :  [ CONFIG_TYPE_SCALAR  , ".".join(['network', args[0], 'vlan'])       ,' ' ],
        'ports'                  :  [ CONFIG_TYPE_SCALAR  , ".".join(['network', args[0], 'ports'])      ,' ' ],
      }
      return section_map

  if config_name == 'dhcp_common':
      section_map = {
        'domainRequired'         :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].domainneeded'              ,' ' ],
        'authoritative'          :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].authoritative'             ,' ' ],
        'localServer'            :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].local'                     ,' ' ],
        'localDomain'            :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].domain'                    ,' ' ],
        'logQueries'             :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].logqueries'                ,' ' ],
        'dnsForwardings'         :  [ CONFIG_TYPE_LIST    , 'dhcp.@dnsmasq[0].server'                    ,' ' ],
        'rebindProtection'       :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].rebind_protection'         ,' ' ],
        'rebindLocalhost'        :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].rebind_localhost'          ,' ' ],
        'rebindDomain'           :  [ CONFIG_TYPE_LIST    , 'dhcp.@dnsmasq[0].rebind_domain'             ,' ' ],
        'localServiceOnly'       :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].localservice'              ,' ' ],
        'nonWildcard'            :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].nonwildcard'               ,' ' ],
        'listenInterfaces'       :  [ CONFIG_TYPE_LIST    , 'dhcp.@dnsmasq[0].interface'                 ,' ' ],
        'excludeInterfaces'      :  [ CONFIG_TYPE_LIST    , 'dhcp.@dnsmasq[0].notinterface'              ,' ' ],
        'readEthers'             :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].readethers'                ,' ' ],
        'leaseFile'              :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].leasefile'                 ,' ' ],
        'ignoreResolveFile'      :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].noresolv'                  ,' ' ],
        'resolveFile'            :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].resolvfile'                ,' ' ],
        'ignoreHosts'            :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].nohosts'                   ,' ' ],
        'addHostFiles'           :  [ CONFIG_TYPE_LIST    , 'dhcp.@dnsmasq[0].addnhosts'                 ,' ' ],
        'suppressLogging'        :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].quietdhcp'                 ,' ' ],
        'allocIpSequential'      :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].sequential_ip'             ,' ' ],
        'filterPrivate'          :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].boguspriv'                 ,' ' ],
        'filterUseless'          :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].filterwin2k'               ,' ' ],
        'localiseQueries'        :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].localise_queries'          ,' ' ],
        'expandHosts'            :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].expandhosts'               ,' ' ],
        'addServerFile'          :  [ CONFIG_TYPE_SCALAR  , ''                                           ,' ' ],
        'strictOrder'            :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].strictorder'               ,' ' ],
        'bogusNXDomain'          :  [ CONFIG_TYPE_LIST    , 'dhcp.@dnsmasq[0].bogusnxdomain'             ,' ' ],
        'dnsServerPort'          :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].port'                      ,' ' ],
        'dnsQueryPort'           :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].queryport'                 ,' ' ],
        'dhcpLeaseMax'           :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].dhcpleasemax'              ,' ' ],
        'dnsPacketSizeMax'       :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].ednspacket_max'            ,' ' ],
        'dnsForwardMax'          :  [ CONFIG_TYPE_SCALAR  , 'dhcp.@dnsmasq[0].dnsforwardmax'             ,' ' ],
      }
      return section_map

  if config_name == 'dhcp_interface_pool':
    if args and args[0]:
      section_map = {
        'ignore'                 :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'ignore'])        ,' ' ],
        'addrStart'              :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'start'])         ,' ' ],
        'addrLimit'              :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'limit'])         ,' ' ],
        'leaseTime'              :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'leasetime'])     ,' ' ],
        'dynamicDhcp'            :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'dynamicdhcp'])   ,' ' ],
        'force'                  :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'force'])         ,' ' ],
        'v4Netmask'              :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'netmask'])       ,' ' ],
        'dhcpOptions'            :  [ CONFIG_TYPE_LIST    , ".".join(['dhcp', args[0], 'dhcp_option'])   ,' ' ],
      }
      return section_map

  if config_name == 'dhcp_interface_v6pool':
    if args and args[0]:
      section_map = {
        'ra'                     :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'ra'])            ,' ' ],
        'dhcpv6'                 :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'dhcpv6'])        ,' ' ],
        'ndp'                    :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'ndp'])           ,' ' ],
        'dhcpv6Mode'             :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'ra_management']) ,' ' ],
        'raDefault'              :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'ra_default'])    ,' ' ],
        'dnsServer'              :  [ CONFIG_TYPE_LIST    , ".".join(['dhcp', args[0], 'dns'])           ,' ' ],
        'dnsDomain'              :  [ CONFIG_TYPE_LIST    , ".".join(['dhcp', args[0], 'domain'])        ,' ' ],
      }
      return section_map

  if config_name == 'dhcp_static_leases':
    if args and args[0]:
      section_map = {
        'name'                   :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'name'])          ,' ' ],
        'dns'                    :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'dns'])           ,' ' ],
        'mac'                    :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'mac'])           ,' ' ],
        'ipv4Addr'               :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'ip'])            ,' ' ],
        'leasetime'              :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'leasetime'])     ,' ' ],
        'ipv6Suffix'             :  [ CONFIG_TYPE_SCALAR  , ".".join(['dhcp', args[0], 'hostid'])        ,' ' ],
      }
      return section_map

  if config_name == 'snmp_community_config':
    if args and args[0]:
      section_map = {
        'community'              :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0], 'community'])    ,' ' ],
        'communityType'          :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0], 'secname'])      ,' ' ],
        'source'                 :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0], 'source'])       ,' ' ],
        'v1GroupName'            :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_v1", 'group']),' ' ],
        'v1Version'              :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_v1", 'version']),' ' ],
        'v1Secname'              :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_v1", 'secname']),' ' ],
        'v2GroupName'            :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_v2c", 'group']),' ' ],
        'v2Version'              :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_v2c", 'version']),' ' ],
        'v2Secname'              :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_v2c", 'secname']),' ' ],
        'usmGroupName'           :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_usm", 'group']),' ' ],
        'usmVersion'             :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_usm", 'version']),' ' ],
        'usmSecname'             :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_usm", 'secname']),' ' ],
        'access'                 :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_access"])     ,' ' ],
        'accessGroup'            :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_access", 'group']),' ' ],
        'context'                :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_access", 'context']),' ' ],
        'version'                :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_access", 'version']),' ' ],
        'level'                  :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_access", 'level']),' ' ],
        'prefix'                 :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_access", 'prefix']),' ' ],
        'read'                   :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_access", 'read']),' ' ],
        'write'                  :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_access", 'write']),' ' ],
        'notify'                 :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0] + "_access", 'notify']),' ' ],
      }
      return section_map

  if config_name == 'snmp_traphost_config':
    if args and args[0]:
      section_map = {
        'trapHost'               :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0], 'HostName'])     ,' ' ],
        'trapVersion'            :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0], 'Type'])         ,' ' ],
        'trapCommunity'          :  [ CONFIG_TYPE_SCALAR  , ".".join(['snmpd', args[0], 'Community'])    ,' ' ],
      }
      return section_map

  if config_name == 'port_forwarding_config':
    if args and args[0]:
      section_map = {
        'name'                   :  [ CONFIG_TYPE_SCALAR  , ".".join(['firewall', args[0], 'name'])      ,' ' ],
        'protocol'               :  [ CONFIG_TYPE_SCALAR  , ".".join(['firewall', args[0], 'proto'])     ,' ' ],
        'externalZone'           :  [ CONFIG_TYPE_SCALAR  , ".".join(['firewall', args[0], 'src'])       ,' ' ],
        'externalAddr'           :  [ CONFIG_TYPE_SCALAR  , ''                                           ,' ' ],
        'externalPort'           :  [ CONFIG_TYPE_SCALAR  , ".".join(['firewall', args[0], 'src_dport']) ,' ' ],
        'inernalZone'            :  [ CONFIG_TYPE_SCALAR  , ".".join(['firewall', args[0], 'dest'])      ,' ' ],
        'internalAddr'           :  [ CONFIG_TYPE_SCALAR  , ".".join(['firewall', args[0], 'dest_ip'])   ,' ' ],
        'internalPort'           :  [ CONFIG_TYPE_SCALAR  , ".".join(['firewall', args[0], 'dest_port']) ,' ' ],
      }
      return section_map

