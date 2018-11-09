#!/usr/bin/env python
import socket

from common.env import *
from common.misc import *
from common.sysinfo import *

from apClient.docker_proc import *
from apClient.puci_proc import *
from apClient.wifi_proc import *



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
class ClientCmdApp():
    def __init__(self):
        pass

    def run(self):
        cmd_sock=CommandSocket('', APNOTIFIER_CMD_PORT)

        log_info (LOG_MODULE_APCLIENT, '----- Start Command Application  ----')

        while True:
            sock, addr = cmd_sock.sock.accept()
            log_info(LOG_MODULE_APCLIENT, '[Got connection from', addr)

            data = sock.recv(MAX_SOCK_MSG_LENGTH)

            if data:
                log_info(LOG_MODULE_APCLIENT, 'data:', data, 'len:', len(data))
                data = eval(data)
                command = data['command']

                if command == SAL_PROVISIONING_DONE:
                    system_provisioning_done_proc()
                elif command == SAL_PYTHON_DOCKER_IMAGE_CREATE:
                    docker_image_create_proc(data['body'])
                elif command == SAL_PUCI_MODULE_RESTART:
                    puci_module_restart_proc(data['body'])
                elif command == SAL_WIFI_MODULE_RESTART:
                    wifi_module_restart_proc(data['body'])
                elif command == SAL_SYSTEM_REBOOT:
                    system_reboot_proc(data['body'])

            log_info(LOG_MODULE_APCLIENT, '---- Socket close ----')
            sock.close()


def system_provisioning_done_proc():
    log_info(LOG_MODULE_APCLIENT, "================= Service module restart for provisioning  ==============")

    pmr = PuciModuleRestart(None)

    cmd_str = "ifdown lan; ifup lan; ifdown wan; ifup wan"
    output, error = subprocess_open(cmd_str)

    pmr._puci_default_module_restart("system")
    pmr._puci_default_module_restart("firewall")

    '''
    pmr._puci_container_module_restart("snmpd")
    pmr._puci_container_module_restart("dnsmasq")
    '''

    wifi_module_reload_all_devices()

    # [2018.11.09] Remove docker container clean up
    #initialize_docker_containers()

    # Notification
    noti_req = APgentSendNotification()
    noti_req.set_notification_value(200, "Successful")
    noti_req.response['serialNumber'] = device_info_get_serial_num()

    for i in range(0, 30):
        status_code = noti_req.send_notification(CAPC_NOTIFICATION_PROVISIONING_FINISH_URL)
        if status_code == 200:
            log_info(LOG_MODULE_APCLIENT, "** Send provisioning finish to Controller Success **")
            puci_provisioning_done_file_create()
            break

def puci_provisioning_done_file_create():
    f = open(PROVISIONING_DONE_FILE, "w")
    f.write("done")
    f.close()
    log_info(LOG_MODULE_APCLIENT, "** Create %s file **" %PROVISIONING_DONE_FILE)


def system_reboot_proc(request):
    if not 'delay' in request: return

    delay = request['delay']

    cmd_str = "reboot -d %d" % delay
    subprocess_open(cmd_str)

    log_info(LOG_MODULE_APCLIENT, "** System Reboot Done **")
