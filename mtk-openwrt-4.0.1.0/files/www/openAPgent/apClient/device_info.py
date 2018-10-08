#!/usr/bin/pyhton
from common.request import *
from common.log import *
from common.env import *
from common.misc import *


def request_post_device_info(device_info, url):
    post_req = APgentSendRequest('POST')
    post_req.data = device_info._make_device_info_data()
    post_req.headers = {'content-type': 'application/json'}
    return post_req.send_request(CAPC_DEVICE_INFO_POST_URL)

def register_device_info():
    device_info = DeviceInformation(0)

    for i in range (0, 360):
        device_info.update_device_info()
        status_code = request_post_device_info(device_info, CAPC_DEVICE_INFO_POST_URL)
        if status_code == 200:
            log_info (LOG_MODULE_APCLIENT, "** AP Device has successfully registered to Controller. **")
            break
        elif status_code == 451:
            log_info(LOG_MODULE_APCLIENT, "** AP Device already exists. **")
            break


