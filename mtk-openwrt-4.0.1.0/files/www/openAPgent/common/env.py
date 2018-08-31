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
CAPC_SERVER_PORT='80'

CAPC_SERVER_URL='http://' + CAPC_SERVER_IP + ':' + CAPC_SERVER_PORT

CAPC_DEVICE_INFO_URL=CAPC_SERVER_URL+'/v1/devices/'
CAPC_DEVICE_INFO_POST_URL=CAPC_SERVER_URL+'/v1/devices/registration/'

CAPC_NOTIFICATION_IMAGE_POST_URL = CAPC_SERVER_URL+'/v1/notifications/virtualization/images'
CAPC_NOTIFICATION_CONTAINER_POST_URL = CAPC_SERVER_URL+'/v1/notifications/virtualization/containers'

'''
AP Server
'''
APSERVER_IP='http://127.0.0.1'
APSERVER_PORT=':8001'
APSERVER_URL=APSERVER_IP+APSERVER_PORT
APSERVER_DEVICE_INFO_URL=APSERVER_URL+'/v1/devices/'
APSERVER_DEVICE_INFO_POST_URL=APSERVER_URL+'/v1/devices/'


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

'''
Client
'''
APCLIENT_CMD_PORT=8007
#APCLIENT_PID_PATH="%s/apClient.pid"%WORKDIR
APCLIENT_PID_PATH="/var/run/apClient.pid"


'''
Interface
'''

LAN_ETHDEV='eth0'
WAN_ETHDEV='eth1'


IFNAME_LENGTH=30

PROC_NET_DEV_PATH="/proc/net/dev"



'''
Docker 
'''
SAL_PYTHON_DOCKER_IMAGE_CREATE          = 1
SAL_PYTHON_DOCKER_IMAGE_DETAIL_CREATE   = 2
SAL_PYTHON_DOCKER_CONTAINER_CREATE      = 3

