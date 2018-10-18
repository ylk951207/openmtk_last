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
        self.req_devname = request['devname']

    def _wifi_interface_enable_proc(self, enable):
        if enable == True:
            log_info(LOG_MODULE_APCLIENT, "ifup for ifname: " + self.req_ifname)
            output, error = subprocess_open('ifconfig %s up '%self.req_ifname)
        else:
            log_info(LOG_MODULE_APCLIENT, "** ifconfig %s down **" + self.req_ifname)
            output, error = subprocess_open('ifconfig %s down '%self.req_ifname)

    def _wifi_module_reload(self):
        log_info(LOG_MODULE_APCLIENT, "** /sbin/wifi reload %s **" %self.req_devname)
        cmd_str = "/sbin/wifi reload %s" %self.req_devname
        output, error = subprocess_open(cmd_str)

    def wifi_module_restart_proc(self):
        current_state = device_get_wireless_state(self.req_ifname)
        log_info(LOG_MODULE_APCLIENT, "WIFI current state: " + str(current_state) + " req_enable: " + str(self.req_enable))
        if current_state == True:
            if self.req_enable == False:
                self._wifi_interface_enable_proc(self.req_enable)
                return
            self._wifi_module_reload()
        else:
            if self.req_enable == True:
                self._wifi_module_reload()

def wifi_module_reload_all_devices():
    log_info(LOG_MODULE_APCLIENT, "** /sbin/wifi reload **")
    output, error = subprocess_open("/sbin/wifi reload")

def wifi_module_restart_proc(command, request):
    log_info(LOG_MODULE_APCLIENT, 'Received message: command(%s), request(%s)' % (command, str(request)))

    wmr = WifiModuleRestart(request)
    wmr.wifi_module_restart_proc()
