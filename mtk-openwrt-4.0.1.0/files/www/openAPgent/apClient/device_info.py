#!/usr/bin/pyhton
import time

from common.env import *
from common.misc import *
from common.message import *
from common.network import *
from apClient.client import *


MAX_REGISTER_DEVICE_INIT_RETRIES = 180
MAX_DEVICE_REGISTER_SLEEP_TIME = 20
MAX_REQUEST_PROVISIONG_START_COUNT = 10
MAX_DEVICE_PROVISIONG_SLEEP_TIME = 30

def request_provisiong_start():
    post_req = APgentSendRequest('POST')
    post_req.data = {"serialNumber": device_info_get_serial_num()}
    post_req.headers = post_req.headers = {'content-type': 'application/json'}
    return post_req.send_request(CAPC_NOTIFICATION_PROVISIONING_START_URL)

def post_provisiong_start():
    request_provisiong_start()
    while True:
        time.sleep(MAX_DEVICE_PROVISIONG_SLEEP_TIME)
        if os.path.exists(PROVISIONING_RECEIVE_FILE):
            log_info (LOG_MODULE_APCLIENT, "** Successfully Provisioning-start send to Controller. **")
            os.remove(PROVISIONING_RECEIVE_FILE)
            log_info(LOG_MODULE_APCLIENT, "** Remove Provisioning-Receive file. **")
            break
        else:
            log_info(LOG_MODULE_APCLIENT, "** Retry Provisioning-start send to Controller. **")
            request_provisiong_start()

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

