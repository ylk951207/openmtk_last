#!/usr/bin/pyhton
import time

from common.env import *
from common.misc import *
from common.message import *
from common.sysinfo import *
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

    '''
        if is_registerd == False:
        log_info(LOG_MODULE_APCLIENT, "** Device registration to cAPC is failed. **")
        puci_provisioning_done_file_create()
    '''


def send_ip_address_change_notification(ifname):
    noti_req = APgentSendNotification()

    self.response['ifname'] = ifname

    iflist = [ifname]
    ni_addrs = DeviceNetifacesInfo(iflist)

    self.response['ipv4Address'] = ni_addrs.get_ipv4_addr(ifname)
    self.response['ipv4Netmask'] = ni_addrs.get_ipv4_netmask(ifname)

    device_identify = dict()
    device_identify['serialNumber'] = device_info_get_serial_num()
    noti_req.response['deviceIdentity'] = device_identify

    noti_req.send_notification(CAPC_NOTIFICATION_ADDRESS_CHANGE_URL)
