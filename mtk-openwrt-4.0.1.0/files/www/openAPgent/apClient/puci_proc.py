#!/usr/bin/env python
import docker

from common.log import *
from common.env import *
from common.request import *
from common.misc import *
from apClient.device_info import device_info_get_serial_num


class PuciModuleRestart(object):
    def __init__(self, request):
        self.request = request

        self.config_file = request['config_file']

        if 'container_name' in request.keys():
            self.container_name = request['container_name']
        else:
            self.container_name = None

        if 'ifname' in request.keys():
            self.ifname = request['ifname']
        else:
            self.ifname = None

    def puci_provisioning_done_file_create(self):
        f = open(PROVISIONING_DONE_FILE, "w")
        f.write("done")
        f.close()
        log_info(LOG_MODULE_APCLIENT, "** Create %s file **" %PROVISIONING_DONE_FILE)

    def _docker_container_get_by_prefix(self, name_prefix):
        cmd_str = "docker ps -a --filter 'name=" + name_prefix + "' | grep " + name_prefix + " | awk '{print $NF}'"
        output, error = subprocess_open(cmd_str)
        output = output.split()
        log_info(LOG_MODULE_APCLIENT, "Execute command(%s) output(%s) error(%s)***" % (str(cmd_str), str(output), str(error)))
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

    def _puci_network_module_restart(self, ifname):
        log_info(LOG_MODULE_APCLIENT, "ifdown/ifup for ifname: " + ifname)
        output, error = subprocess_open('ifdown ' + ifname)
        output, error = subprocess_open('ifup ' + ifname)

    def _puci_default_module_restart(self, config_file):
        command = '/etc/init.d/' + config_file + ' restart'
        output, error = subprocess_open(command)
        log_info(LOG_MODULE_APCLIENT, "== command '%s', output:%s, error:%s ==" % (command, output, error))

    def _puci_provisioning_module_restart(self):

        log_info(LOG_MODULE_APCLIENT, "================= Service module restart for provisioning  ==============")
        self._puci_default_module_restart("system")

        self._puci_network_module_restart('lan')
        self._puci_network_module_restart('wan')

        self._puci_container_module_restart("snmpd")
        self._puci_container_module_restart("dnsmasq")

        # Notification
        noti_req = APgentSendNotification()
        noti_req.set_notification_value(200, "Successful")
        noti_req.response['serialNumber'] = device_info_get_serial_num()

        for i in range(0, 30):
            status_code = noti_req.send_notification(CAPC_NOTIFICATION_PROVISIONING_FINISH_URL)
            if status_code == 200:
                log_info(LOG_MODULE_APCLIENT, "** Send provisioning finish to Controller Success **")
                self.puci_provisioning_done_file_create()
                break

    def puci_module_restart(self):
        log_info(LOG_MODULE_APCLIENT, "Restart UCI config module: " + self.config_file)

        if self.config_file == "all":
            self._puci_provisioning_module_restart ()
        elif self.container_name:
            self._puci_container_module_restart(self.container_name)
        elif self.config_file == 'network' and self.ifname:
            self._puci_network_module_restart(self.ifname)
        else:
            self._puci_default_module_restart(self.config_file)

        '''
        TODO : Send result message to cACP
        '''

def puci_cmd_proc(command, request):
    log_info(LOG_MODULE_APCLIENT, 'Received message: command(%s), request(%s)' % (command, str(request)))

    pmr = PuciModuleRestart(request)

    if command == SAL_PUCI_MODULE_RESTART:
        pmr.puci_module_restart()
    else:
        log_info(LOG_MODULE_APCLIENT, 'Invalid Argument')
