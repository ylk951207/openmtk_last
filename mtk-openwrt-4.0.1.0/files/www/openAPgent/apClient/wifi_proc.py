#!/usr/bin/env python
from common.env import *
from common.misc import *
from common.message import *
from common.sysinfo import *

class WifiModuleRestart(object):
    def __init__(self, request):
        self.req_ifname = request['ifname']
        self.req_enable = request['enable']
        self.req_devname = request['devname']

    def _wifi_device_enable_proc(self, enable):
        log_info(LOG_MODULE_APCLIENT, "** wifi up/down devname(%s), up(%d) **" %(self.req_devname, enable))
        if enable == True:
            subprocess_open_nonblock('/sbin/wifi up %s' % self.req_devname)
        else:
            subprocess_open_nonblock('/sbin/wifi down %s' % self.req_devname)
        log_info(LOG_MODULE_APCLIENT, "** wifi up/down done **")

    '''
    def _wifi_interface_enable_proc(self, enable):
        if enable == True:
            log_info(LOG_MODULE_APCLIENT, "ifup for ifname: " + self.req_ifname)
            subprocess_open_nonblock('ifconfig %s up '%self.req_ifname)
        else:
            log_info(LOG_MODULE_APCLIENT, "** ifconfig %s down **" + self.req_ifname)
            subprocess_open_nonblock('ifconfig %s down '%self.req_ifname)
        log_info(LOG_MODULE_APCLIENT, "** Execute ifconfig **")
    '''

    def _wifi_module_reload(self):
        log_info(LOG_MODULE_APCLIENT, "** /sbin/wifi reload for %s**" %self.req_devname)
        command = "/sbin/wifi reload %s" %self.req_devname
        subprocess_open_nonblock(command)
        log_info(LOG_MODULE_APCLIENT, "** Execute wifi reload (command: %s) **" %command)

    def wifi_module_restart_proc(self):
        current_state = device_get_wireless_state(self.req_ifname)
        log_info(LOG_MODULE_APCLIENT, "wifi current state: " + str(current_state) + ", req_enable: " + str(self.req_enable))
        if current_state == True:
            if self.req_enable == False:
                self._wifi_device_enable_proc(0)
            else:
                self._wifi_module_reload()
        else:
            if self.req_enable == True:
                self._wifi_device_enable_proc(1)

def wifi_module_reload_all_devices():
    log_info(LOG_MODULE_APCLIENT, "** /sbin/wifi reload **" )
    command = "/sbin/wifi reload"
    subprocess_open_nonblock(command)
    log_info(LOG_MODULE_APCLIENT, "** Execute wifi reload (command: %s) **" % command)

def wifi_module_restart_proc(request):
    log_info(LOG_MODULE_APCLIENT, 'Received message: request(%s)' % (str(request)))

    wmr = WifiModuleRestart(request)
    wmr.wifi_module_restart_proc()
