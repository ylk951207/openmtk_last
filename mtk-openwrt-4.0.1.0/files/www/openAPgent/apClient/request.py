#!/usr/bin/env python
import os, sys
import time
import json
import logging
import requests
from common.log import *
from common.env import *

class SendRequest(object):
    def __init__(self, method, device_id):
        self.method = method
        self.device_id = device_id

    def send_request(self, url):
        log_info(LOG_MODULE_REQUEST, '<Send Request>')
        log_info(LOG_MODULE_REQUEST, 'method=', self.method, 'URL=', url)
        
        if self.method == 'POST':
            self.resp = requests.post(url, data=json.dumps(self.data), headers=self.headers)
        elif self.method == 'PUT':
            self.resp = requests.put(url + self.device_id, data=json.dumps(self.data), headers=self.headers)
        elif self.method == 'GET':
            self.resp = requests.get(url + self.device_id)
        else:
            log_info(LOG_MODULE_REQUEST, "Invalid method\n")

        self.resp_json = self.resp.json()
        self.response_debug()

        return self.resp

    def response_debug(self):
        log_info(LOG_MODULE_REQUEST, '=' * 80)
        log_info(LOG_MODULE_REQUEST, '<Get Response>')
        log_info(LOG_MODULE_REQUEST, 'status_code:', self.resp.status_code)
        log_info(LOG_MODULE_REQUEST, 'self.resp.url:')
        log_info(LOG_MODULE_REQUEST, self.resp.url)
        log_info(LOG_MODULE_REQUEST, 'self.resp.header:')
        log_info(LOG_MODULE_REQUEST, self.resp.headers)
        log_info(LOG_MODULE_REQUEST, 'self.resp.content:')
        log_info(LOG_MODULE_REQUEST, self.resp.content)
        log_info(LOG_MODULE_REQUEST, 'self.resp.json():')
        log_info(LOG_MODULE_REQUEST, self.resp_json)
        
        log_info(LOG_MODULE_REQUEST, '=' * 80)