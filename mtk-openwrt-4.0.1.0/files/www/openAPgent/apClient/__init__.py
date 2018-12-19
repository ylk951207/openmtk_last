import os
import threading

from common.env import *
from common.misc import *

from apClient.client import *
from apClient.device_info import *


'''
Main Routine
'''
init_log("apClientLog")

pid = str(os.getpid())
file(APCLIENT_PID_PATH, 'w').write(pid)

log_info (LOG_MODULE_APCLIENT, '----- Start Client Command Application  ----')

ClientInitialize()

'''
Device Registration to cAPC
'''
if not os.path.exists(PROVISIONING_DONE_FILE):
    register_device_info()

'''
 Main Loop
'''
client_t = threading.Thread(target=client_run)
client_t.start()

'''
Send provisiong start to cAPC
'''
post_provisiong_start()