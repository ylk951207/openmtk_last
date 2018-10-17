import fileinput
import time
from common.env import *
from common.log import *
from common.misc import *
from common.request import *
from common.response import *


def py_provisioning_done_create(request):
    '''
    TODO: Celery Tasks
    '''

    noti_data = dict()
    noti_data['config_file'] = "all"
    server_msg = ApServerLocalMassage(APNOTIFIER_CMD_PORT)
    server_msg.send_message_to_apnotifier("PUCI", SAL_PUCI_MODULE_RESTART, noti_data)

    return response_make_simple_success_body(None)


def py_keepalive_check_list():
    return response_make_simple_success_body(None)


def py_system_info_list():
    device_info = DeviceInformation(0)
    device_data = device_info._make_device_info_data()
    time_data = device_info_get_all_time_info ()
    data = {
            "device-info" : device_data,
            "time-info" : time_data,
            'header' : {
                    'resultCode':200,
                    'resultMessage':'Success.',
                    'isSuccessful':'true'
            }
    }
    return data


def py_system_info_retrieve(command, add_header):
    log_info(LOG_MODULE_SAL, "command = ", command)

    time_data = dict()

    if command == 'times':
        time_data = device_info_get_all_time_info()
    else:
        raise RespNotFound("Command")

    data = {
        'time-info': time_data,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    log_info(LOG_MODULE_SAL, "Response = ", str(data))

    return data


def py_hardware_interface_info_list():
    interface_info = HardwareInformation()
    interface_data = interface_info._make_hardware_interface_info_data("all")
    data = {
        "interface-info" : interface_data,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data


def py_hardware_interface_info_retrieve(if_type, add_header):
    interface_info = HardwareInformation()
    interface_data = interface_info._make_hardware_interface_info_data(if_type)
    data = {
        if_type: interface_data,
        'header' : {
            'resultCode':200,
            'resultMessage':'Success.',
            'isSuccessful':'true'
        }
    }
    return data


def py_hardware_wireless_info_list():
    wireless_data = list()
    wireless_iflist = {
        "2G_default" : "ra0",
        "5G_default" : "rai0"
    }

    for key, value in wireless_iflist.items():
        dict_data = {
            "type" : key,
            "state" : device_get_wireless_state(value)
        }
        wireless_data.append(dict_data)

    data = {
        "wireless-info": wireless_data,
        'header': {
               'resultCode': 200,
               'resultMessage': 'Success.',
               'isSuccessful': 'true'
        }
    }
    return data


def py_system_reboot_create(request):
    delay = request['delay']

    # Default delay for response
    if delay <= 0: delay = 2

    cmd_str = "reboot -d %d" % delay

    subprocess_open(cmd_str)

    data = {
        'header': {
               'resultCode': 200,
               'resultMessage': 'Success.',
               'isSuccessful': 'true'
        }
    }
    return data



