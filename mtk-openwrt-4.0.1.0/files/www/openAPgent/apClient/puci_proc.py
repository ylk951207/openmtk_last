#!/usr/bin/env python
import subprocess
import docker

from common.log import *
from common.env import *
from common.request import *
from apClient.device_info import device_info_get_serial_num


def subprocess_open(command):
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (stdoutdata, stderrdata) = popen.communicate()
    return stdoutdata, stderrdata

def puci_provisioning_done_file_create():
    f = open(PROVISIONING_DONE_FILE, "w")
    f.write("done")
    f.close()
    log_info(LOG_MODULE_APCLIENT, "** Create %s file **" %PROVISIONING_DONE_FILE)


def _docker_container_get_by_prefix(name_prefix):
    cmd_str = "docker ps -a --filter 'name=" + name_prefix + "' | grep " + name_prefix + " | awk '{print $NF}'"
    output, error = subprocess_open(cmd_str)
    output = output.split()
    log_info(LOG_MODULE_APCLIENT, "Execute command(%s) output(%s) error(%s)***" % (str(cmd_str), str(output), str(error)))
    if not error:
        return output
    return None

def _docker_container_restart(client, container_list):
    log_info(LOG_MODULE_APCLIENT, "container_list : " + str(container_list))
    for i in range(0, len(container_list)):
        try:
            container = client.containers.get(container_list[i])
        except docker.errors.DockerException as e:
            log_error(LOG_MODULE_APCLIENT, "*** docker  container get() error ***")
            log_error(LOG_MODULE_APCLIENT, "*** error: " + str(e))
            continue
        log_info(LOG_MODULE_APCLIENT, "container_status: " + str(container.status))
        if container.status == "running":
            container.restart()

def puci_module_restart(request):
    config_file = request['config_file']
    if 'ifname' in request.keys():
        ifname = request['ifname']
    else:
        ifname = None

    log_info(LOG_MODULE_APCLIENT, "Restart UCI config module: " + config_file)

    if config_file == "all":
        output, error = subprocess_open("/etc/init.d/system restart")
        output, error = subprocess_open("ifdown wan;ifup wan")
        output, error = subprocess_open("ifdown lan;ifup lan")
        log_info(LOG_MODULE_APCLIENT, "================= Service module restart for provisioning  ==============")

        # Notification
        noti_req = APgentSendNotification()
        noti_req.set_notification_value(200, "Successful")
        noti_req.response['serialNumber'] = device_info_get_serial_num()

        for i in range (0, 30):
            status_code = noti_req.send_notification(CAPC_NOTIFICATION_PROVISIONING_FINISH_URL)
            if status_code == 200:
                log_info (LOG_MODULE_APCLIENT, "** Send provisioning finish to Controller **")

                puci_provisioning_done_file_create()
                break
    elif config_file == 'network' and ifname:
        log_info(LOG_MODULE_APCLIENT, "ifdown/ifup for ifname: " + ifname)
        output, error = subprocess_open('ifdown ' + ifname)
        output, error = subprocess_open('ifup ' + ifname)
    elif config_file == 'snmpd':
        log_info(LOG_MODULE_APCLIENT, "<snmpd container restart>")
        client = docker.from_env()
        container_list = _docker_container_get_by_prefix("net-snmp")
        if container_list:
            _docker_container_restart(client, container_list)
    else:
        command = '/etc/init.d/' + config_file + ' restart'
        log_info(LOG_MODULE_APCLIENT, "===" , command + "===")
        output, error = subprocess_open(command)

    return output, error

def puci_cmd_proc(command, request):
    log_info(LOG_MODULE_APCLIENT, 'Received message: command(%s), request(%s)' % (command, str(request)))

    if command == SAL_PUCI_MODULE_RESTART:
        puci_module_restart(request)
    else:
        log_info(LOG_MODULE_APCLIENT, 'Invalid Argument')
