import os


'''
Common
'''

WORKDIR=os.getcwd()

APGENT_DB_FILE = WORKDIR+"db.sqlite3"

'''
Configuration Files
'''

DEVICE_INFO_CONFIG=WORKDIR+"/conf/device_info.default"


'''
Controller
'''

SERVER_IP='192.168.1.184'
SERVER_PORT='8090'

SERVER_URL='http://' + SERVER_IP + ':' + SERVER_PORT

DEVICE_INFO_URL=SERVER_URL+'/v1/devices/'
DEVICE_INFO_POST_URL=SERVER_URL+'/v1/devices/registration/'


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

APSERVER_LOG_PATH="/var/log/apServer.log"
APCLIENT_LOG_PATH="/var/log/apClient.log"

'''
Client
'''
APCLIENT_CMD_PORT=8010
#APCLIENT_PID_PATH="%s/apClient.pid"%WORKDIR
APCLIENT_PID_PATH="/var/run/apClient.pid"


'''
Interface
'''

LAN_ETHDEV='eth0'
WAN_ETHDEV='eth1'


IFNAME_LENGTH=30

PROC_NET_DEV_PATH="/proc/net/dev"

