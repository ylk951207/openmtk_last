#!/usr/bin/env python
import docker

from common.log import *
from common.env import *
from common.request import *
from common.misc import *

class WifiModuleRestart(object):
    def __init__(self, request):
        self.req_ifname = request['ifname']
        self.req_enable = request['enable']

    def _wifi_interface_enable_proc(self, enable):
        if enable == True:
            log_info(LOG_MODULE_APCLIENT, "ifup for ifname: " + self.req_ifname)
            output, error = subprocess_open('ifconfig %s up '%self.req_ifname)
        else:
            log_info(LOG_MODULE_APCLIENT, "ifdown for ifname: " + self.req_ifname)
            output, error = subprocess_open('ifconfig %s down '%self.req_ifname)

    def _wifi_module_reload(self):
        log_info(LOG_MODULE_APCLIENT, "** wifi restart **")
        output, error = subprocess_open('/sbin/wifi reload')

    def wifi_module_restart_proc(self):
        current_state = device_get_wireless_state(self.req_ifname)
        if current_state == True:
            if self.req_enable == False:
                self._wifi_interface_enable_proc(self.req_enable)
                return
            self._wifi_module_reload()
        else:
            if self.req_enable == True:
                self._wifi_interface_enable_proc(self.req_enable)


def wifi_cmd_proc(command, request):
    log_info(LOG_MODULE_APCLIENT, 'Received message: command(%s), request(%s)' % (command, str(request)))

    wmr = WifiModuleRestart(request)

    if command == SAL_WIFI_MODULE_RESTART:
        wmr.wifi_module_restart_proc()
    else:
        log_info(LOG_MODULE_APCLIENT, 'Invalid Argument')
