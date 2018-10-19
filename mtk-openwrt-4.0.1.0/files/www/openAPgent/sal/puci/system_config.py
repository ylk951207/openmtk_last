from puci import *
from common.log import *
from common.env import *
from common.request import *
from common.response import *

UCI_SYSTEM_CONFIG_FILE = "system"
UCI_SYSTEM_CONFIG_COMMON_CONFIG = "system_config_common"
UCI_SYSTEM_CONFIG_LOGGING_CONFIG = "system_config_logging"
UCI_SYSTEM_CONFIG_NTP_CONFIG = "system_config_ntp"


def system_puci_module_restart():
    noti_data = dict()
    noti_data['config_file'] = UCI_SYSTEM_CONFIG_FILE
    puci_send_message_to_apnotifier(SAL_PUCI_MODULE_RESTART, noti_data)

'''
SystemConfig
'''
def puci_system_config_list():
    system_common_data = dict()
    system_log_data = dict()
    system_ntp_data = dict()

    system_common_data = system_config_uci_get(UCI_SYSTEM_CONFIG_COMMON_CONFIG, system_common_data)
    system_log_data = system_config_uci_get(UCI_SYSTEM_CONFIG_LOGGING_CONFIG, system_log_data)
    system_ntp_data = system_config_uci_get(UCI_SYSTEM_CONFIG_NTP_CONFIG, system_ntp_data)

    data = {
        "system" : {
            "common" : system_common_data,
            "logging": system_log_data,
            "ntp": system_ntp_data
        },
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data


def puci_system_config_retrieve(command, add_header):
    system_data = dict()

    log_info(UCI_SYSTEM_CONFIG_FILE, "command = ", command)

    if command == 'common':
        system_data = system_config_uci_get(UCI_SYSTEM_CONFIG_COMMON_CONFIG, system_data)
    elif command == 'logging':
        system_data = system_config_uci_get(UCI_SYSTEM_CONFIG_LOGGING_CONFIG, system_data)
    elif command == 'ntp':
        system_data = system_config_uci_get(UCI_SYSTEM_CONFIG_NTP_CONFIG, system_data)
    else:
        raise RespNotFound("Command")

    data = {
        command: system_data,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    log_info(UCI_SYSTEM_CONFIG_FILE, "Response = ", str(data))

    return data


def puci_system_config_create(request):
    return system_config_set(request)


def puci_system_config_update(request):
    return system_config_set(request)


def puci_system_config_detail_create(request, command):
    return system_config_detail_set(request, command)


def puci_system_config_detail_update(request, command):
    return system_config_detail_set(request, command)

def system_config_set(request):

    log_info(UCI_SYSTEM_CONFIG_FILE, "request data = ", request)
    request = request["system"]
    if 'common' in request.keys():
        system_config_uci_set(UCI_SYSTEM_CONFIG_COMMON_CONFIG, request['common'])

    if 'logging' in request.keys():
        log_leq = convert_system_logging_output_data(request['logging'])
        system_config_uci_set(UCI_SYSTEM_CONFIG_LOGGING_CONFIG, log_leq)

    if 'ntp' in request.keys():
        system_config_uci_set(UCI_SYSTEM_CONFIG_NTP_CONFIG, request['ntp'])

    system_puci_module_restart()

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def system_config_detail_set(request, command):
    log_info(UCI_SYSTEM_CONFIG_FILE, "command = ", command)
    log_info(UCI_SYSTEM_CONFIG_FILE, "request data = ", request)

    if command == 'common':
        system_config_uci_set(UCI_SYSTEM_CONFIG_COMMON_CONFIG, request)
    elif command == 'logging':
        request = convert_system_logging_output_data(request)
        system_config_uci_set(UCI_SYSTEM_CONFIG_LOGGING_CONFIG, request)
    elif command == 'ntp':
        system_config_uci_set(UCI_SYSTEM_CONFIG_NTP_CONFIG, request)
    else:
        raise RespNotFound("Command")

    system_puci_module_restart()

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data


def system_config_uci_get(uci_file, system_data):
    uci_config = ConfigUCI(UCI_SYSTEM_CONFIG_FILE, uci_file)
    if uci_config == None:
        raise RespNotFound("UCI Config")

    uci_config.show_uci_config()

    for map_key, map_val in uci_config.section_map.items():
        system_data[map_key] = map_val[2]

    return system_data


def system_config_uci_set(uci_file, req_data):
    system_data = dict()
    log_info(UCI_SYSTEM_CONFIG_FILE, "request data = ", req_data)
    uci_config = ConfigUCI(UCI_SYSTEM_CONFIG_FILE, uci_file)
    if uci_config == None:
        raise RespNotFound("UCI Config")

    uci_config.set_uci_config(req_data)

    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]
        if system_data:
            system_data[map_key] = map_val[2]

    return system_data



def convert_system_logging_output_data(log_req):

    if log_req['loggingOutputLevel'] == 'emergency':
        log_req['loggingOutputLevel'] = '1'
    elif log_req['loggingOutputLevel'] == 'alert':
        log_req['loggingOutputLevel'] = '2'
    elif log_req['loggingOutputLevel'] == 'critical':
        log_req['loggingOutputLevel'] = '3'
    elif log_req['loggingOutputLevel'] == 'error':
        log_req['loggingOutputLevel'] = '4'
    elif log_req['loggingOutputLevel'] == 'warning':
        log_req['loggingOutputLevel'] = '5'
    elif log_req['loggingOutputLevel'] == 'notice':
        log_req['loggingOutputLevel'] = '6'
    elif log_req['loggingOutputLevel'] == 'info':
        log_req['loggingOutputLevel'] = '7'
    elif log_req['loggingOutputLevel'] == 'debug':
        log_req['loggingOutputLevel'] = '8'

    return log_req