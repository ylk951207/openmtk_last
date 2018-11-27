import os


'''
Common
'''

WORKDIR=os.getcwd()


'''
Configuration Files
'''

DEVICE_INFO_CONFIG=WORKDIR+"/config/ap_device_config.py"


'''
Controller
'''

CAPC_SERVER_IP='capc.withusp.com'
CAPC_SERVER_PORT='80'

CAPC_SERVER_URL='http://' + CAPC_SERVER_IP + ':' + CAPC_SERVER_PORT


CAPC_DEVICE_INFO_POST_URL=CAPC_SERVER_URL+'/v1/devices/registration/'

CAPC_NOTIFICATION_PROVISIONING_FINISH_URL = CAPC_SERVER_URL+'/v1/notifications/provisioning-finish'
CAPC_NOTIFICATION_IMAGE_POST_URL = CAPC_SERVER_URL+'/v1/notifications/virtualization/images'
CAPC_NOTIFICATION_ADDRESS_CHANGE_URL = CAPC_SERVER_URL+'/v1/notifications/interfaces/address-change'

'''
apClient
'''
APCLIENT_PID_PATH="/var/run/apClient.pid"
APNOTIFIER_CMD_PORT=8008

PROVISIONING_DONE_FILE="/tmp/provisioning-done"

APCLIENT_WORKER_CMD="cd /www/openAPgent; python -m utils/apclient_worker "

'''
apClient Command 
'''
SAL_PROVISIONING_DONE           = 1
SAL_PUCI_MODULE_RESTART         = 2
SAL_PYTHON_DOCKER_IMAGE_CREATE  = 3
SAL_WIFI_MODULE_RESTART         = 4
SAL_SYSTEM_REBOOT               = 5



'''
Interface
'''
LAN_ETHDEV='eth0'
WAN_ETHDEV='eth1'

IFNAME_LENGTH=30

PROC_NET_DEV_PATH="/proc/net/dev"


'''
Logging
'''
LOG_MODULE_SAL='sal'
LOG_MODULE_APSERVER='apServer'
LOG_MODULE_APCLIENT='apClient'
LOG_MODULE_REQUEST='Request'
LOG_MODULE_RESPONSE='Response'
LOG_MODULE_SERVICE="service"
LOG_MODULE_DOCKER="docker"

APSERVER_LOG_PATH="/var/log/apServer.log"
APCLIENT_LOG_PATH="/var/log/apClient.log"


'''
Firewall
'''
TEMP_FIREWALL_USER_FILE = '/etc/firewall.user.tmp'
FIREWALL_USER_FILE = '/etc/firewall.user'


'''
Virtualization
'''
CONTAINER_BACKUP_STR=".old_container"

DEST_PORT_PREFIX_PRIMARY = "11"
DEST_PORT_PREFIX_SECONDARY = "22"
# TODO: Consider protocol UDP, TCP...
MODULE_PORT_MAPPING_TABLE = {
    'net-snmp' : ['161'],
}
#    'dnsmasq' : ['53', '67'],

'''
Wireless
'''
WIRELESS_MEDIATEK_CONFIG_PATH='/etc/wireless/mediatek/'

MT7615_1_DAT_CONFIG_FILE="mt7615e.1.dat"
MT7622_1_DAT_CONFIG_FILE="mt7622.1.dat"

FIVE_GIGA_DEVICE_NAME = "MT7615.1"
TWO_GIGA_DEVICE_NAME = "MT7622.1"

'''
DHCP
'''
UCI_DHCP_CONFIG_FILE = "dhcp"
UCI_DHCP_COMMON_CONFIG = "dhcp_common"
UCI_DHCP_INTERFACE_POOL_CONFIG = "dhcp_interface_pool"
UCI_DHCP_INTERFACE_V6POOL_CONFIG = "dhcp_interface_v6pool"
UCI_DHCP_STATIC_LEASE_CONFIG = "dhcp_static_leases"
UCI_DHCP_V6POOL_STR = "v6Settings"


DHCP_LEASE_FILE="/tmp/dhcp.leases"
DHCP_RESOLV_AUTO_CONFIG_FILE="/tmp/resolv.conf.auto"

LAN_DNS_SERVER_KEY = "lanDnsServer"
WAN_DNS_SERVER_KEY = "wanDnsServer"
