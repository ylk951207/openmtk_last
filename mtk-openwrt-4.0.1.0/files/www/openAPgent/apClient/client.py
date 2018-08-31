#!/usr/bin/env python
import os, sys
import time
import logging
import socket
from apClient.device_info import *
#from apClient.docker_proc import *
from common.log import *
from common.env import *

WORKDIR=os.getcwd()


class CommandSocket():
    def __init__(self, addr, port):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((addr, port))
        self.sock.listen(5)


'''
apClient Command Handler
'''
class ClientCmdApp():
    def __init__(self):
	    pass

    def run(self):
        cmd_sock=CommandSocket('', APCLIENT_CMD_PORT)

        log_info (LOG_MODULE_APCLIENT, '----- Start ClientCmdApp ----')

        while True:
            sock, addr = cmd_sock.sock.accept()
            log_info(LOG_MODULE_APCLIENT, '[Got connection from', addr)

            data = sock.recv(1024)

            if data:
                proc_docker(data['command'], data['body'])
            '''
            [TODO] command segmantation, not only proc_device_info
           
            if data:
                log_info(LOG_MODULE_APCLIENT, 'data:', data, 'len:', len(data))
                data = eval(data)
                module = data['module']
                if module == 'DOCKER':
                    proc_docker(data['command'], data['body'])
                else:
                    proc_device_info(data)
            '''
            log_info(LOG_MODULE_APCLIENT, '---- Socket close ----')
            sock.close()


def init_start_config():
    init_device_info()
