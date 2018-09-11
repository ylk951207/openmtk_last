import os
from common.env import *
from common.log import *
from apClient.device_info import *
from apClient.client import *


def init_start_config():
    init_device_info()


'''
Main Routine
'''
init_log("apClientLog")

pid = str(os.getpid())
file(APCLIENT_PID_PATH, 'w').write(pid)

init_start_config()

log_info (LOG_MODULE_APCLIENT, '----- Start Client Command Application  ----')

register_device_info()

client = ClientCmdApp()
client.run()
