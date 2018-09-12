import fileinput

from puci import *
from common.log import *
from common.env import *

UCI_SNMP_CONFIG_FILE = "snmp"


'''
SNMP Config
'''
def puci_snmp_config_list():
    snmp_data = dict()
    snmp_data = snmp_config_uci_get(UCI_SNMP_CONFIG_FILE, snmp_data)
    data = {
        "snmp": snmp_data,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def puci_snmp_config_create(request):
    return snmp_config_set(request)

def puci_snmp_config_update(request):
    return snmp_config_set(request)

def snmp_config_set(request):
    log_info(LOG_MODULE_SAL, "request data = ", request)

    snmp_config_uci_set(request, UCI_SNMP_CONFIG_FILE)

    noti_data = dict()
    noti_data['config_file'] = UCI_SNMP_CONFIG_FILE
    puci_send_message_to_apnotifier(SAL_PUCI_MODULE_RESTART, noti_data)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def snmp_config_uci_get(uci_file, dhcp_data):
    uci_config = ConfigUCI(UCI_SNMP_CONFIG_FILE, uci_file)
    if uci_config == None:
        raise RespNotFound("UCI Config")

    uci_config.show_uci_config()

    for map_key, map_val in uci_config.section_map.items():
        dhcp_data[map_key] = map_val[2]

    return dhcp_data

def snmp_config_uci_set(req_data, uci_file):
    log_info(LOG_MODULE_SAL, "request data = ", req_data)

    uci_config = ConfigUCI(UCI_SNMP_CONFIG_FILE, uci_file)
    if uci_config == None:
        raise RespNotFound("UCI Config")

    uci_config.set_uci_config(req_data)

