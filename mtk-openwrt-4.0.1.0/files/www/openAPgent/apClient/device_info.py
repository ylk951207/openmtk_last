#!/usr/bin/pyhton
import os 
import sys
import json
import socket
import requests
import sqlite3
#import netifaces as ni
import fcntl, socket, struct
from apClient.request import SendRequest
from common.log import *
from common.env import *
from time import sleep

def get_ip_address(ifname):
    f = os.popen('ifconfig '+ ifname +' | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    return f.read()

def init_device_info():
    log_info (LOG_MODULE_APCLIENT, DEVICE_INFO_CONFIG)

    global gDeviceInfo

    gDeviceInfo = ProcDeviceInfo()

    gDeviceInfo.device_id = 0
    gDeviceInfo.name = socket.gethostname()
#    gDeviceInfo.ip_addr = ni.ifaddresses(WAN_ETHDEV)[ni.AF_INET][0]['addr']
    gDeviceInfo.ip_addr = get_ip_address(WAN_ETHDEV) 
    gDeviceInfo.mac_addr = gDeviceInfo._get_hwaddr(WAN_ETHDEV)
    gDeviceInfo.serial_num = gDeviceInfo._get_serial_num(gDeviceInfo.mac_addr)
    gDeviceInfo.counterfeit = 0

    fp = open(DEVICE_INFO_CONFIG,'r')

    while True:
        line = fp.readline()
    	if not line: break
        line = line.replace("\n", "")
    	token = line.split('=')

    	if token[0] == 'vendor_id':
    	    gDeviceInfo.vendor_id = token[1]
    	elif token[0] == 'vendor_name':
    	    gDeviceInfo.vendor_name = token[1]
    	elif token[0] == 'device_type':
    	    gDeviceInfo.device_type = token[1]
    	elif token[0] == 'model_num':
    	    gDeviceInfo.model_num = token[1]
    	elif token[0] == 'user_id':
    	    gDeviceInfo.user_id = token[1]
    	elif token[0] == 'user_passwd':
    	    gDeviceInfo.user_passwd = token[1]
    	elif token[0] == 'status':
    	    gDeviceInfo.status = token[1]
    	elif token[0] == 'map_x':
    	    gDeviceInfo.map_x = token[1]
    	elif token[0] == 'map_y':
    	    gDeviceInfo.map_y = token[1]
        else:
    	    log_warn(LOG_MODULE_APCLIENT, 'Invalid token', token[1])

    fp.close()


class ProcDeviceInfo(object):
    def __init__(self):
        pass

    def update_device_info(self):
        gDeviceInfo.name = socket.gethostname()
        #gDeviceInfo.ip_addr = ni.ifaddresses(WAN_ETHDEV)[ni.AF_INET][0]['addr']
        gDeviceInfo.ip_addr = get_ip_address(WAN_ETHDEV) 
        gDeviceInfo.mac_addr = gDeviceInfo._get_hwaddr(WAN_ETHDEV)
        gDeviceInfo.serial_num = gDeviceInfo._get_serial_num(gDeviceInfo.mac_addr)

    def update_device_id(self, resp_json):
        self.device_id = resp_json['devices']['id']
        log_info(LOG_MODULE_APCLIENT,  "Set ID=", self.device_id)

    def _get_serial_num(self, macaddr):
        token = macaddr.split(':')
        return "AP_SR_NO7777_"+ token[3] + token[4] + token[5]

    def _get_hwaddr(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
        return ':'.join(['%02x' % ord(char) for char in info[18:24]])
#        info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', bytes(ifname[:15], 'utf-8')))
#        return ''.join(['%02x:' % b for b in info[18:24]])[:-1]

    def _make_request_data(self):
        self.data = {\
	              "device_id": gDeviceInfo.device_id, \
	              "name": gDeviceInfo.name, \
	              "vendor_id": gDeviceInfo.vendor_id, \
	              "vendor_name": gDeviceInfo.vendor_name, \
	              "serial_num": gDeviceInfo.serial_num, \
	              "device_type": gDeviceInfo.device_type, \
	              "model_num": gDeviceInfo.model_num, \
	              "ip_addr": gDeviceInfo.ip_addr, \
	              "mac_addr": gDeviceInfo.mac_addr, \
	              "user_id": gDeviceInfo.user_id, \
	              "user_passwd": gDeviceInfo.user_passwd, \
	              "status": gDeviceInfo.status, \
	              "map_x": gDeviceInfo.map_x, \
	              "map_y": gDeviceInfo.map_y, \
	              "counterfeit": gDeviceInfo.counterfeit, \
                 }

        log_info(LOG_MODULE_APCLIENT,  "\n<Send Request>")
        log_info(LOG_MODULE_APCLIENT, "=" * 80)
        log_info(LOG_MODULE_APCLIENT, json.dumps(self.data, indent=2))

        return self.data

    def request_post_device_info(self):
        try:                   
            post_req = SendRequest('POST', self.device_id)
                                   
            post_req.data = self._make_request_data()
            post_req.headers = {'content-type': 'application/json'}
            resp = post_req.send_request(DEVICE_INFO_POST_URL)
                                       
        except requests.exceptions.RequestException as e:
            log_info(LOG_MODULE_APCLIENT,  "RequestException", e)
            return 600  

        return resp.status_code
        
        '''
        if resp.status_code == 200:
            self.update_device_id (post_req.resp_json)

            post_req.data = self._make_request_data()
            post_req.headers = {'content-type': 'application/json'}
            resp = post_req.send_request(APSERVER_DEVICE_INFO_POST_URL)
        '''

    def request_put_device_info(self):
        if self.device_id==0:
            log_err(LOG_MODULE_APCLIENT, APCLIENT_ERR_DEVICE_INFO_PUT_INVALID_DEVICE_ID)

        post_req = SendRequest('PUT', self.device_id)

        post_req.data = self._make_request_data()
        post_req.headers = {'content-type': 'application/json'}

        resp = post_req.send_request(DEVICE_INFO_URL)

        '''
        if resp.status_code == 200:
            resp = post_req.send_request(APSERVER_DEVICE_INFO_URL)
        '''
    def request_get_device_info(self):
        log_info (LOG_MODULE_APCLIENT, 'Get device Info')
        post_req = SendRequest('GET', self.device_id)
        post_req.send_request(DEVICE_INFO_URL)


def register_device_info():
    gDeviceInfo.update_device_info()
    for i in range (0, 360):
        status_code = gDeviceInfo.request_post_device_info()
        if status_code == 200:
            log_info (LOG_MODULE_APCLIENT, "** AP Device has successfully registered to Controller. **")
            break
        sleep(5)

def proc_device_info(data):
    msg = data.split(' ')
    method = msg[0]

    log_info(LOG_MODULE_APCLIENT, 'Received message: %s [method: %s]' % (data, method))

    gDeviceInfo.update_device_info()

    if method == 'GET':
        gDeviceInfo.request_get_device_info()
    elif method == 'POST':
        gDeviceInfo.request_post_device_info()
    elif method == 'PUT':
        gDeviceInfo.request_put_device_info()
    else:
        log_info(LOG_MODULE_APCLIENT, 'Invalid Argument')


