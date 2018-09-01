from apClient.device_info import *
from common.log import *


def init_start_config():
    init_device_info()


'''
Main Routine
'''
init_log("apClientLog")

init_start_config()

log_info (LOG_MODULE_APCLIENT, '----- Start Client Command Application  ----')

register_device_info()

log_info (LOG_MODULE_APCLIENT, '----- End Client Command Application  ----')

#client = ClientCmdApp()
#client.run()
