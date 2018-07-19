from apClient.client import *
from common.log import *

init_log("apClientLog")

init_start_config()

register_device_info()

client = ClientCmdApp()

client.run()
