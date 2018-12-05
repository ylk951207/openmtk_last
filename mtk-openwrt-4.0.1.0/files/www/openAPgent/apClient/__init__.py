import os
from multiprocessing import Process
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
client_p = Process(target=client_run)
'''
Send provisiong start to cAPC
'''
prov_start_p = Process(target=post_provisiong_start)

client_p.start()
prov_start_p.start()

# prov_start_p.join()
# client_p.join()
