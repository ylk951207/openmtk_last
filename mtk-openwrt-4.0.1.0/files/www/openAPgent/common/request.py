#!/usr/bin/env python
import os, sys
import time
import json
import logging
import requests
import ssl
import socket

from common.log import *
from common.env import *

class SendRequest(object):
    def __init__(self, method):
        self.method = method

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


def sendHttpsRequest():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((url, 443))
    sock = ssl.wrap_socket(sock, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE,
                        ssl_version=ssl.PROTOCOL_SSLv23)
    sock.sendall("GET / HTTP/1.1\r\nHost: github.com\r\nConnection: close\r\n\r\n")

    while True:

        new = sock.recv(4096)
        if not new:
            sock.close()
            break
        print new


class SendNotification(object):
    def __init__(self):
        pass

    def send_notification(self, url):
        log_info(LOG_MODULE_REQUEST, '<Send Notification>')

        self.resp = requests.post(url, data=json.dumps(self.data), headers=self.headers)
        self.resp_json = self.resp.json()

        return self.resp
