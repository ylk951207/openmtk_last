#!/usr/bin/env python
import docker

from common.env import *
from common.misc import *
from common.message import *
from apClient.wifi_proc import *

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

        if 'ifname' in request.keys():
            self.ifname = request['ifname']
        else:
            self.ifname = None

    def _docker_container_get_by_prefix(self, name_prefix):
        cmd_str = "docker ps -a --filter 'name=" + name_prefix + "' | grep " + name_prefix + " | awk '{print $NF}'"
        output, error = subprocess_open(cmd_str)
        output = output.split()
        log_info(LOG_MODULE_APCLIENT, "Execute command(%s) output:%s, error:%s ***" % (str(cmd_str), str(output), str(error)))
        if not error:
            return output
        return None

    def _docker_container_restart(self, client, container_list):
        log_info(LOG_MODULE_APCLIENT, "container_list : " + str(container_list))
        for i in range(0, len(container_list)):
            try:
                container = client.containers.get(container_list[i])
            except docker.errors.DockerException as e:
                log_error(LOG_MODULE_APCLIENT, "*** docker  container get() error ***")
                log_error(LOG_MODULE_APCLIENT, "*** error: " + str(e))
                continue

            log_info(LOG_MODULE_APCLIENT, "container_status: " + str(container.status))
            if container.status != "running":
                continue

        log_info(LOG_MODULE_APCLIENT, "Restart container %s" %container.name)
        try:
            container.restart()
        except docker.errors.DockerException as e:
            log_error(LOG_MODULE_APCLIENT, "*** docker  container restart() error ***")
            log_error(LOG_MODULE_APCLIENT, "*** error: " + str(e))

    def _puci_container_module_restart(self, container_name):
        log_info(LOG_MODULE_APCLIENT, "<'%s' container restart>" %container_name)
        client = docker.from_env()
        container_list = self._docker_container_get_by_prefix(container_name)
        if container_list:
            self._docker_container_restart(client, container_list)

        if container_name == 'dnsmasq':
            wifi_module_reload_all_devices()

    def _puci_network_module_restart(self, ifname):
        log_info(LOG_MODULE_APCLIENT, "ifdown/ifup for ifname: " + ifname)
        cmd_str = "ifdown %s; ifup %s" %(ifname, ifname)
        output, error = subprocess_open(cmd_str)

    def _puci_default_module_restart(self, config_file):
        command = '/etc/init.d/' + config_file + ' restart'
        output, error = subprocess_open(command)
        log_info(LOG_MODULE_APCLIENT, "== command '%s', output:%s, error:%s ==" % (command, output, error))

    def puci_module_restart(self):
        log_info(LOG_MODULE_APCLIENT, "Restart UCI config module: " + self.config_file)

        if self.container_name:
            self._puci_container_module_restart(self.container_name)
        elif self.config_file == 'network' and self.ifname:
            self._puci_network_module_restart(self.ifname)

            '''
            When interface config is changed, the related container must be restarted
            to apply interface config.
            '''
            self._puci_container_module_restart("dnsmasq")

            wifi_module_reload_all_devices()
        else:
            self._puci_default_module_restart(self.config_file)

        '''
        TODO : Send result message to cACP
        '''

def puci_module_restart_proc(request):
    log_info(LOG_MODULE_APCLIENT, 'Received message: request(%s)' % (str(request)))

    pmr = PuciModuleRestart(request)
    pmr.puci_module_restart()