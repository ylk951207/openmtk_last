#!/usr/bin/env python
import json
import requests
import ssl
import socket
from rest_framework.exceptions import *

from common.env import *
from common.misc import *


class RespNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
#    default_detail = _('Not found.')


'''
openAPgent Send Request
'''
class APgentSendRequest(object):
    def __init__(self, method):
        self.method = method

    '''
     Django restframework only can support HTTP protocol by request module.
    '''
    def send_request(self, url):
        log_info(LOG_MODULE_REQUEST, '<Send Request: %s>' %str(url))
        log_info(LOG_MODULE_REQUEST, 'method=', self.method, 'URL=', url)

        try:
            if self.method == 'POST':
                response = requests.post(url, data=json.dumps(self.data), headers=self.headers)
            elif self.method == 'PUT':
                response = requests.put(url, data=json.dumps(self.data), headers=self.headers)
            elif self.method == 'GET':
                response = requests.get(url)
            else:
                log_info(LOG_MODULE_REQUEST, "Invalid method")
        except Exception as e:
            log_error(LOG_MODULE_REQUEST, "*** requests.post() error: %s" %str(e))
            if e.response:
                log_error(LOG_MODULE_REQUEST, "*** requests.post() error response: %s" % str(e.response))
                return e.response.status_code
            else:
                return 600
        else:
            log_info(LOG_MODULE_REQUEST, "Send request success (status: %d)" %response.status_code)
            self.response_debug(response)
            return response.status_code

    def response_debug(self, response):
        log_info(LOG_MODULE_REQUEST, '=' * 80)
        log_info(LOG_MODULE_REQUEST, '<Get Response>')
        log_info(LOG_MODULE_REQUEST, 'status_code:', response.status_code)
        log_info(LOG_MODULE_REQUEST, 'self.resp.url:')
        log_info(LOG_MODULE_REQUEST, response.url)
        log_info(LOG_MODULE_REQUEST, 'self.resp.header:')
        log_info(LOG_MODULE_REQUEST, response.headers)
        log_info(LOG_MODULE_REQUEST, 'self.resp.content:')
        log_info(LOG_MODULE_REQUEST, response.content)
        resp_json = response.json()
        log_info(LOG_MODULE_REQUEST, 'self.resp.json():')
        log_info(LOG_MODULE_REQUEST, resp_json)
        
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


'''
openAPgent Send Notification
'''
class APgentSendNotification(object):
    def __init__(self):
        self.response = dict()

    def send_notification(self, url):
        log_info(LOG_MODULE_REQUEST, '<Send Notification: %s>' %str(url))
        log_info(LOG_MODULE_REQUEST, "<Send Data> %s" %self.response)
        headers = {'content-type': 'application/json'}

        try:
            response = requests.post(url, data=json.dumps(self.response), headers=headers)
        except Exception as e:
            log_error(LOG_MODULE_REQUEST, "*** requests.post() error: %s" %str(e))
            if e.response:
                log_error(LOG_MODULE_REQUEST, "*** requests.post() error response: %s" % str(e.response))
                return e.response.status_code
            else:
                return 600
        else:
            log_info(LOG_MODULE_REQUEST, "Send notification success (status: %d)" %response.status_code)
            return response.status_code

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

        return self.response

'''
openAPgent Send Response Message
'''
class APgentResponseMessgae(object):
    def __init__(self):
        self.response = dict()

    def set_response_value(self, status_code, response_msg, is_successful):
        if status_code != 200:
            response = response_msg.response
            try:
                explanation = response.json()['message']
            except ValueError:
                explanation = (response.content or '').strip()
        else:
            explanation = response_msg

        self.response['status_code'] = status_code
        self.response['error_msg'] = explanation
        self.response['isSuccessful'] = is_successful
        log_debug(LOG_MODULE_RESPONSE, "Set Response = ", str(self.response))

        return self.response

    @property
    def status_code(self):
        return self.response['status_code']

    @property
    def error_msg(self):
        return self.response['error_msg']

    @property
    def is_successful(self):
        return self.response['isSuccessful']

    def make_response_body(self, body_data):
        if not body_data:
            body_data = dict()

        body_data['header'] =  {
            'resultCode': self.status_code,
            'resultMessage': self.error_msg,
            'isSuccessful': self.is_successful
        }
        log_debug(LOG_MODULE_RESPONSE, "Response Body = ", str(body_data))
        return body_data

def response_make_simple_success_body(body_data):
    resp_msg = APgentResponseMessgae()
    resp_msg.set_response_value(200, "Successful", True)
    data = resp_msg.make_response_body(body_data)
    return data

def response_make_simple_error_body(status_code, msg, body_data):
    resp_msg = APgentResponseMessgae()

    resp_msg.response['status_code'] = status_code
    resp_msg.response['error_msg'] = msg
    resp_msg.response['isSuccessful'] = False

    data = resp_msg.make_response_body(body_data)
    return data


'''
apServer Send Local Messages
'''
class ApServerLocalMassage():
    def __init__(self, port):
        self.port = port

    def send_request_apnotifier(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', self.port))
        sock.send(str(data))
        sock.close()
        log_info(LOG_MODULE_REQUEST, "send_request_apnotifier() data: " + str(data))

    def send_message_to_apnotifier(self, command, request):
        data = {
            'command' : command,
            'body' : request
        }

        self.send_request_apnotifier (data)
