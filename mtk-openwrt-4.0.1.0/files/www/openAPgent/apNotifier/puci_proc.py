#!/usr/bin/env python
import os
import subprocess
import shlex

from common.log import *
from common.env import *
from common.request import *


def subprocess_open(command):
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (stdoutdata, stderrdata) = popen.communicate()
    return stdoutdata, stderrdata


def puci_module_restart(request):
    config_file = request['config_file']
    if 'ifname' in request.keys():
        ifname = request['ifname']
    else:
        ifname = None

    log_info(LOG_MODULE_APNOTIFIER, "Service uci config restart : " + config_file)

    if config_file == 'network' and ifname:
        log_info(LOG_MODULE_APNOTIFIER, "ifdown/ifup for ifname: " + ifname)
        output, error = subprocess_open('ifdown ' + ifname)
        output, error = subprocess_open('ifup ' + ifname)
    else:
        command = '/etc/init.d/' + config_file + ' restart'
        log_info(LOG_MODULE_SAL, "===" , command + "===")
        output, error = subprocess_open(command)

    # TODO Notification

    return output, error

def puci_cmd_proc(command, request):
    log_info(LOG_MODULE_APNOTIFIER, 'Received message: %s [request: %s]' % (command, str(request)))

    if command == SAL_PUCI_MODULE_RESTART:
        puci_module_restart(request)
    else:
        log_info(LOG_MODULE_APNOTIFIER, 'Invalid Argument')
