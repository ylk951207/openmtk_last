#!/usr/bin/pyhton
import time

from common.env import *
from common.misc import *
from common.message import *
from common.network import *
from apClient.client import *


MAX_REGISTER_DEVICE_INIT_RETRIES = 180
MAX_DEVICE_REGISTER_SLEEP_TIME = 20


def request_post_device_info(device_info, url):
    post_req = APgentSendRequest('POST')
    post_req.data = device_info._make_device_info_data()
    post_req.headers = {'content-type': 'application/json'}
    return post_req.send_request(CAPC_DEVICE_INFO_POST_URL)

def register_device_info():
    device_info = DeviceInformation(0)
    is_registerd = False
    count = 0

    while True:
        if os.path.exists(PROVISIONING_DONE_FILE):
            break

        device_info.update_device_info()
        status_code = request_post_device_info(device_info, CAPC_DEVICE_INFO_POST_URL)
        if status_code == 200:
            log_info (LOG_MODULE_APCLIENT, "** AP Device has successfully registered to Controller. **")
            is_registerd = True
            break
        elif status_code == 451:
            log_info(LOG_MODULE_APCLIENT, "** AP Device already exists. **")
            is_registerd = True
            break

        count += 1
        if count > MAX_REGISTER_DEVICE_INIT_RETRIES:
            time.sleep (MAX_DEVICE_REGISTER_SLEEP_TIME)

