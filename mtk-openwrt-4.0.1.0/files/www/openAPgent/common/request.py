#!/usr/bin/env python
import os, sys
import time
import json
import logging
import requests
import ssl
import socket
import subprocess

from common.log import *
from common.env import *

class APgentSendRequest(object):
    def __init__(self, method):
        self.method = method

    '''
     Django restframework only can support HTTP protocol by request module.
    '''
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

    '''
    This function can support HTTPS protocol.
    '''
    def send_secure_request(url, port):
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


class APgentSendNotification(object):
    def __init__(self):
        self.response = dict()

    def send_notification(self, url):
        log_info(LOG_MODULE_REQUEST, '<Send Notification>')
        headers = {'content-type': 'application/json'}

        try:
            response = requests.post(url, data=json.dumps(self.response), headers=headers)
        except Exception as e:
            log_error(LOG_MODULE_REQUEST, "*** requests.post() error: " + str(e))
        else:
            log_info(LOG_MODULE_REQUEST, "Send notification done..(status: %d)" %response.status_code)

    def set_notification_value(self, status_code, response_msg):
        if status_code != 200:
            response = response_msg.response
            try:
                explanation = response.json()['message']
            except ValueError:
                explanation = (response.content or '').strip()
        else:
            explanation = response_msg

        self.response['resultCode'] = status_code
        self.response['resultMessage'] = explanation
        log_info(LOG_MODULE_REQUEST, "Set Notification header  = ", str(self.response))

        return self.response

class ApServerLocalMassage():
    def __init__(self, port):
        self.port = port

    def send_request_apnotifier(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', self.port))
        sock.send(str(data))
        sock.close()
        log_info(LOG_MODULE_REQUEST, "send_request_apnotifier() data: " + str(data))

    def send_message_to_apnotifier(self, module, command, request):
        data = {
            'module' : module,
            'command' : command,
            'body' : request
        }

        self.send_request_apnotifier (data)

    def execute_apnotifier(self, module, command, request):
        log_info(LOG_MODULE_REQUEST, "Excute apNotifier >> ")
        args_list = [sys.executable, 'docker_notifier.py']
        args_list.append('-c')
        args_list.append(str(command))
        args_list.append('-r')
        args_list.append(str(request))

        p = subprocess.Popen(args_list, cwd='/www/openAPgent/sal/python/', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p