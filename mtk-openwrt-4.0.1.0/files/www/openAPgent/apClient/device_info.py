#!/usr/bin/pyhton
import os 
import sys
import json
import socket
import requests
import sqlite3
#import netifaces as ni
import fcntl, socket, struct
from common.request import *
from common.log import *
from common.env import *
#from time import sleep
from conf.ap_device_config import *

def get_ip_address(ifname):
    f = os.popen('ifconfig '+ ifname +' | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    return f.read()[:-1]

def init_device_info():
    log_info (LOG_MODULE_APCLIENT, DEVICE_INFO_CONFIG)

    global gDeviceInfo

    gDeviceInfo = ProcDeviceInfo()

    gDeviceInfo.device_id = 0
    gDeviceInfo.name = socket.gethostname()
    gDeviceInfo.ip_addr = get_ip_address(WAN_ETHDEV) 
    gDeviceInfo.mac_addr = gDeviceInfo._get_hwaddr(WAN_ETHDEV)
    gDeviceInfo.serial_num = gDeviceInfo._get_serial_num()
    gDeviceInfo.counterfeit = 0

    gDeviceInfo.vendor_id = AP_VENDOR_ID
    gDeviceInfo.vendor_name = AP_VENDOR_NAME
    gDeviceInfo.device_type = AP_DEVICE_TYPE
    gDeviceInfo.model_num = AP_MODEL_NUMBER
    gDeviceInfo.user_id = AP_USER_ID
    gDeviceInfo.user_passwd = AP_USER_PASSWD
    gDeviceInfo.status = AP_STATUS
    gDeviceInfo.map_x = AP_MAP_X
    gDeviceInfo.map_y = AP_MAP_Y
    gDeviceInfo.capabilities = AP_CAPABILITIES

class ProcDeviceInfo(object):
    def __init__(self):
        pass

    def update_device_info(self):
        gDeviceInfo.name = socket.gethostname()
        #gDeviceInfo.ip_addr = ni.ifaddresses(WAN_ETHDEV)[ni.AF_INET][0]['addr']
        gDeviceInfo.ip_addr = get_ip_address(WAN_ETHDEV) 
        gDeviceInfo.mac_addr = gDeviceInfo._get_hwaddr(WAN_ETHDEV)
        gDeviceInfo.serial_num = gDeviceInfo._get_serial_num()

    def update_device_id(self, resp_json):
        self.device_id = resp_json['devices']['id']
        log_info(LOG_MODULE_APCLIENT,  "Set ID=", self.device_id)

    def _get_serial_num(self):
        mac_addr = self._get_hwaddr(WAN_ETHDEV)
        token = mac_addr.split(':')
        return "AP_SR_NO7777_"+ token[3] + token[4] + token[5]

    def _get_hwaddr(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
        return ':'.join(['%02x' % ord(char) for char in info[18:24]])
#        info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', bytes(ifname[:15], 'utf-8')))
#        return ''.join(['%02x:' % b for b in info[18:24]])[:-1]

    def _get_uptime(self):
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            return uptime_seconds

    def _make_request_data(self):
        self.data = {
	                "id": gDeviceInfo.device_id,
	                "name": gDeviceInfo.name,
	                "vendorId": gDeviceInfo.vendor_id,
	                "vendorName": gDeviceInfo.vendor_name,
	                "serialNumber": gDeviceInfo.serial_num,
	                "type": gDeviceInfo.device_type,
	                "model": gDeviceInfo.model_num,
	                "ip": gDeviceInfo.ip_addr,
	                "mac": gDeviceInfo.mac_addr,
	                "userId": gDeviceInfo.user_id,
	                "userPasswd": gDeviceInfo.user_passwd,
	                "status": gDeviceInfo.status,
	                "mapX": gDeviceInfo.map_x,
	                "mapY": gDeviceInfo.map_y,
	                "counterfeit": gDeviceInfo.counterfeit,
	                "uptime" : gDeviceInfo._get_uptime(),
	                "capabilities" : gDeviceInfo.capabilities
                 }

        log_info(LOG_MODULE_APCLIENT, "=" * 80)
        log_info(LOG_MODULE_APCLIENT,  "<Make Request Message>")
        log_info(LOG_MODULE_APCLIENT, json.dumps(self.data, indent=2))

        return self.data

    def request_post_device_info(self, url):
        try:                   
            post_req = APgentSendRequest('POST')
                                   
            post_req.data = self._make_request_data()
            post_req.headers = {'content-type': 'application/json'}
            resp = post_req.send_request(CAPC_DEVICE_INFO_POST_URL)
                                       
        except requests.exceptions.RequestException as e:
            log_info(LOG_MODULE_APCLIENT,  "RequestException", e)
            return 600  

        return resp.status_code


def register_device_info():
    gDeviceInfo.update_device_info()
    for i in range (0, 360):
        status_code = gDeviceInfo.request_post_device_info(CAPC_DEVICE_INFO_POST_URL)
        if status_code == 200:
            log_info (LOG_MODULE_APCLIENT, "** AP Device has successfully registered to Controller. **")
            break
        elif status_code == 451:
            log_info(LOG_MODULE_APCLIENT, "** AP Device already exists. **")
            break

def proc_device_info(data):
    msg = data.split(' ')
    method = msg[0]

    log_info(LOG_MODULE_APCLIENT, 'Received message: %s [method: %s]' % (data, method))

    gDeviceInfo.update_device_info()

    if method == 'POST':
        gDeviceInfo.request_post_device_info(CAPC_DEVICE_INFO_POST_URL)
    else:
        log_info(LOG_MODULE_APCLIENT, 'Invalid Argument')


