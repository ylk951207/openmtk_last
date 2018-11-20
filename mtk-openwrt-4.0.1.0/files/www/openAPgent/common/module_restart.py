#!/usr/bin/env python
import docker
from common.env import *
from common.misc import *
from common.message import *
from common.sysinfo import *


def wifi_device_get_interface_operstate(ifname):
    filename = '/sys/class/net/' + ifname + '/flags'
    try:
        with open(filename, 'r') as f:
            flags = int(f.read()[2:-1])
            if (flags % 2) == 1:
                return True
            else:
                return False
    except:
        log_error(LOG_MODULE_SYSINFO, "file '%s' open() error" % filename)
        return False

class WifiModuleRestart(object):
    def __init__(self, request):
        self.req_ifname = request['ifname']
        self.req_enable = request['enable']
        self.req_devname = request['devname']

    def _wifi_device_enable_proc(self, enable):
        log_info(LOG_MODULE_SERVICE, "** wifi up/down devname(%s), up(%d) **" %(self.req_devname, enable))
        if enable == True:
            subprocess_open_nonblock('/sbin/wifi up %s' % self.req_devname)
        else:
            subprocess_open_nonblock('/sbin/wifi down %s' % self.req_devname)
        log_info(LOG_MODULE_SERVICE, "** wifi up/down done **")

    '''
    def _wifi_interface_enable_proc(self, enable):
        if enable == True:
            log_info(LOG_MODULE_SERVICE, "ifup for ifname: " + self.req_ifname)
            subprocess_open_nonblock('ifconfig %s up '%self.req_ifname)
        else:
            log_info(LOG_MODULE_SERVICE, "** ifconfig %s down **" + self.req_ifname)
            subprocess_open_nonblock('ifconfig %s down '%self.req_ifname)
        log_info(LOG_MODULE_SERVICE, "** Execute ifconfig **")
    '''

    def _wifi_module_reload(self):
        log_info(LOG_MODULE_SERVICE, "** /sbin/wifi reload for %s**" %self.req_devname)
        command = "/sbin/wifi reload %s" %self.req_devname
        subprocess_open_nonblock(command)
        log_info(LOG_MODULE_SERVICE, "** Execute wifi reload (command: %s) **" %command)

    def wifi_module_restart_proc(self):
        current_state = wifi_device_get_interface_operstate(self.req_ifname)
        log_info(LOG_MODULE_SERVICE, "wifi current state: " + str(current_state) + ", req_enable: " + str(self.req_enable))
        if current_state == True:
            if self.req_enable == False:
                self._wifi_device_enable_proc(0)
            else:
                self._wifi_module_reload()
        else:
            if self.req_enable == True:
                self._wifi_device_enable_proc(1)


def wifi_module_reload_all_devices():
    log_info(LOG_MODULE_SERVICE, "** /sbin/wifi reload **" )
    command = "/sbin/wifi reload"
    subprocess_open_nonblock(command)
    log_info(LOG_MODULE_SERVICE, "** Execute wifi reload (command: %s) **" % command)


def wifi_module_restart_proc(request):
    log_info(LOG_MODULE_SERVICE, 'Received message: request(%s)' % (str(request)))

    wmr = WifiModuleRestart(request)
    wmr.wifi_module_restart_proc()


'''
Python UCI module restart 
'''
class PuciModuleRestart(object):
    def __init__(self, request):
        if not request : return

        self.config_file = request['config_file']

        if 'container_name' in request.keys():
            self.container_name = request['container_name']
        else:
            self.container_name = None

        if 'iflist' in request.keys():
            self.iflist = request['iflist']
        else:
            self.iflist = None

        if 'dnsmasq_restart' in request.keys():
            self.dnsmasq_restart =  request['dnsmasq_restart']
        else:
            # Default = True
            self.dnsmasq_restart = True

    def _docker_container_get_by_prefix(self, name_prefix):
        cmd_str = "docker ps -a --filter 'name=" + name_prefix + "' | grep " + name_prefix + " | awk '{print $NF}'"
        output, error = subprocess_open(cmd_str)
        output = output.split()
        log_info(LOG_MODULE_SERVICE, "Execute command(%s) output:%s, error:%s ***" % (str(cmd_str), str(output), str(error)))
        if not error:
            return output
        return None

    def _docker_container_restart(self, client, container_list):
        log_info(LOG_MODULE_SERVICE, "container_list : " + str(container_list))
        for i in range(0, len(container_list)):
            try:
                container = client.containers.get(container_list[i])
            except docker.errors.DockerException as e:
                log_error(LOG_MODULE_SERVICE, "*** docker  container get() error ***")
                log_error(LOG_MODULE_SERVICE, "*** error: " + str(e))
                continue
            except Exception as e:
                log_info(LOG_MODULE_SERVICEMISC, "container.get: %s" % str(e))

            log_info(LOG_MODULE_SERVICE, "container_status: " + str(container.status))
            if container.status != "running":
                continue

        log_info(LOG_MODULE_SERVICE, "Restart container %s" %container.name)
        try:
            container.restart()
        except docker.errors.DockerException as e:
            log_error(LOG_MODULE_SERVICE, "*** docker  container restart() error ***")
            log_error(LOG_MODULE_SERVICE, "*** error: " + str(e))
        except Exception as e:
            log_info(LOG_MODULE_SERVICE, "container.restart error: %s" % str(e))

    def _puci_container_module_restart(self, container_name, wifi_restart):
        log_info(LOG_MODULE_SERVICE, "<'%s' container restart>" %container_name)
        client = docker.from_env()
        container_list = self._docker_container_get_by_prefix(container_name)
        if container_list:
            self._docker_container_restart(client, container_list)

        if wifi_restart == True:
            wifi_module_reload_all_devices()
        log_info(LOG_MODULE_SERVICE, "container restart done")

    def _puci_network_module_restart(self, iflist):
        log_info(LOG_MODULE_SERVICE, "ifdown/ifup for iflist: " + str(iflist))
        for ifname in iflist:
            if ifname == 'wan':
                continue
            command = "ifdown %s; ifup %s" %(ifname, ifname)
            output, error = subprocess_open(command)
            log_info(LOG_MODULE_SERVICE, "** Execute ifdown/ifup (command:%s) **" % command)
        if 'wan' in iflist:
            command = "sleep 2; ifdown wan;ifup wan"
            output, error = subprocess_open(command)
            log_info(LOG_MODULE_SERVICE, "** Execute ifdown/ifup (command:%s) **" %command)

    def _puci_default_module_restart(self, config_file):
        command = '/etc/init.d/%s restart' %config_file
        subprocess_open_nonblock(command)
        log_info(LOG_MODULE_SERVICE, "** Execute command '%s'" %command)

    def puci_module_restart(self):
        log_info(LOG_MODULE_SERVICE, "Restart UCI config module: " + self.config_file)

        if self.container_name:
            if self.container_name == 'dnsmasq':
                self._puci_container_module_restart(self.container_name, True)
            else:
                self._puci_container_module_restart(self.container_name, False)
        elif self.config_file == 'network' and self.iflist:
            self._puci_network_module_restart(self.iflist)

            '''
            When interface config is changed, the related container must be restarted
            to apply interface config.
            '''
            log_info(LOG_MODULE_SERVICE, 'dnsmasq_restart: ' + str(self.dnsmasq_restart))

            if self.dnsmasq_restart == True:
                self._puci_container_module_restart("dnsmasq", True)
        else:
            self._puci_default_module_restart(self.config_file)

            if self.config_file == "system":
                self.container_name = 'chrony'
                self._puci_container_module_restart(self.container_name, False)


def puci_module_restart_proc(request):
    log_info(LOG_MODULE_SERVICE, 'Received message: request(%s)' % (str(request)))

    pmr = PuciModuleRestart(request)
    pmr.puci_module_restart()
