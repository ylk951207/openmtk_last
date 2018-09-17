import os
from common.env import *
from common.log import *
from apClient.device_info import *
from apClient.docker_container_init import *
from apClient.client import *


def apclient_initialize():
    init_device_info()

    init_docker_docker_container()


'''
Main Routine
'''
init_log("apClientLog")

pid = str(os.getpid())
file(APCLIENT_PID_PATH, 'w').write(pid)

log_info (LOG_MODULE_APCLIENT, '----- Start Client Command Application  ----')

if not os.path.exists(PROVISIONING_DONE_FILE):
    apclient_initialize()

    register_device_info()

'''
 Main Loop
'''
client = ClientCmdApp()
client.run()
