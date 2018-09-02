#!/usr/bin/env python
import os, sys
import time
import logging
import socket
from apNotifier.docker_proc import *
from apNotifier.puci_proc import *
from common.log import *
from common.env import *


class CommandSocket():
    def __init__(self, addr, port):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((addr, port))
        self.sock.listen(5)


MAX_SOCK_MSG_LENGTH=65535
'''
apClient Command Handler
'''
class NotifierCmdApp():
    def __init__(self):
        pass

    def run(self):
        cmd_sock=CommandSocket('', APNOTIFIER_CMD_PORT)

        log_info (LOG_MODULE_APNOTIFIER, '----- Start Notifier Command Application  ----')

        while True:
            sock, addr = cmd_sock.sock.accept()
            log_info(LOG_MODULE_APNOTIFIER, '[Got connection from', addr)

            data = sock.recv(MAX_SOCK_MSG_LENGTH)

            if data:
                log_info(LOG_MODULE_APNOTIFIER, 'data:', data, 'len:', len(data))
                data = eval(data)
                module = data['module']
                if module == 'DOCKER':
                    docker_cmd_proc(data['command'], data['body'])
                elif module == 'PUCI':
                    puci_cmd_proc(data['command'], data['body'])

            log_info(LOG_MODULE_APNOTIFIER, '---- Socket close ----')
            sock.close()
