import os


'''
Common
'''

WORKDIR=os.getcwd()


'''
Configuration Files
'''

DEVICE_INFO_CONFIG=WORKDIR+"/conf/ap_device_config.py"


'''
Controller
'''

CAPC_SERVER_IP='capc.withusp.com'
CAPC_SERVER_PORT='7733'

CAPC_SERVER_URL='http://' + CAPC_SERVER_IP + ':' + CAPC_SERVER_PORT


CAPC_DEVICE_INFO_POST_URL=CAPC_SERVER_URL+'/v1/devices/registration/'

CAPC_NOTIFICATION_IMAGE_POST_URL = CAPC_SERVER_URL+'/v1/notifications/virtualization/images'
CAPC_NOTIFICATION_PROVISIONING_FINISH_URL = CAPC_SERVER_URL+'/v1/notifications/provisioning-finish'

'''
apClient
'''
APCLIENT_PID_PATH="/var/run/apClient.pid"
APNOTIFIER_CMD_PORT=8008

PROVISIONING_DONE_FILE="/tmp/provisioning-done"


'''
apClient Command 
'''
SAL_PYTHON_DOCKER_IMAGE_CREATE          = "1"
SAL_PUCI_MODULE_RESTART                 = "2"
SAL_WIFI_MODULE_RESTART                 = "3"


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

APSERVER_LOG_PATH="/var/log/apServer.log"
APCLIENT_LOG_PATH="/var/log/apClient.log"

