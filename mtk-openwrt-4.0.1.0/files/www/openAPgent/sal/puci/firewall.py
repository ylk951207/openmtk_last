from puci import *
from common.env import *
from common.misc import *
from common.message import *
from common.sysinfo import *

UCI_FIREWALL_CONFIG_FILE="firewall"
UCI_PORT_FORWARDING_CONFIG = "port_forwarding_config"


def firewall_puci_module_restart():
    noti_data = dict()
    noti_data['config_file'] = UCI_FIREWALL_CONFIG_FILE
    puci_send_message_to_apnotifier(SAL_PUCI_MODULE_RESTART, noti_data)

def puci_port_forwarding_list():
    body_data = list()
    name_list = port_forwarding_get_name_info(None)

    log_info(UCI_FIREWALL_CONFIG_FILE, "name_list = " + str(name_list))

    for name_key in name_list.keys():
        data = port_forwarding_config_uci_get(name_key)
        body_data.append(data)

    data = {
        "port-forwarding": body_data,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def puci_port_forwarding_retrieve(name, add_header):
    data = dict()
    name_list = port_forwarding_get_name_info(name)
    log_info(UCI_FIREWALL_CONFIG_FILE, "name_list = " +  str(name_list))

    for name_key, name_value in name_list.items():
        if name_value == name:
            data = port_forwarding_config_uci_get(name_key)

    data = {
        'port-forwarding': data,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def puci_port_forwarding_create(request):
    return port_forwarding_config_set(request)

def puci_port_forwarding_update(request):
    return port_forwarding_config_set(request)

def puci_port_forwarding_detail_create(request, name):
    return port_forwarding_config_detail_set(request, name)

def puci_port_forwarding_detail_update(request, name):
    return port_forwarding_config_detail_set(request, name)

def puci_port_forwarding_destroy(request):
    return port_forwarding_config_destroy(request)

def puci_port_forwarding_detail_destroy(request, name):
    return port_forwarding_config_detail_destroy( name)

def port_forwarding_config_set(request):
    config_data_list = request['port-forwarding']

    name_list = port_forwarding_get_name_info(None)

    while len(config_data_list) > 0:
        config_data = config_data_list.pop(0)
        found = False

        for name_key, name_str in name_list.items():
            if name_str == config_data['name']:
                port_forwarding_config_uci_set(config_data, name_key)
                found = True

        if found == False:
            name_list = port_forwarding_config_uci_add(' redirect', config_data['name'])

            for name_key, name_str in name_list.items():
                port_forwarding_config_uci_set(config_data, name_key)

    firewall_puci_module_restart()

    return response_make_simple_success_body(None)


def port_forwarding_config_detail_set(request, name):
    if name != request['name']:
       return response_make_simple_error_body(400, "Mismatch between URI and request name value", None)

    name_list = port_forwarding_get_name_info(name)

    if len(name_list) <= 0:
        name_list = port_forwarding_config_uci_add(' redirect', name)

    for name_key, name_value in name_list.items():
        if name_value == name:
            port_forwarding_config_uci_set(request, name_key)

    firewall_puci_module_restart()

    return response_make_simple_success_body(None)

def port_forwarding_config_uci_get(name_key):
    data = dict()
    uci_config = ConfigUCI(UCI_FIREWALL_CONFIG_FILE, UCI_PORT_FORWARDING_CONFIG, name_key)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.show_uci_config()

    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]

        if map_key == 'externalAddr':
            data[map_key] = device_info_get_ip_address(WAN_ETHDEV)
        elif map_key == 'protocol':
            data[map_key] = map_val[2].split(' ')
        else:
            data[map_key] = map_val[2]

    return data

def port_forwarding_config_destroy(request):
    config_data_list = request['port-forwarding']

    while len(config_data_list) > 0:
        config_data = config_data_list.pop(0)
        port_forwarding_config_detail_destroy(config_data['name'])

    return response_make_simple_success_body(None)

def port_forwarding_config_detail_destroy(name):
    uci_config = ConfigUCI(UCI_FIREWALL_CONFIG_FILE, UCI_PORT_FORWARDING_CONFIG, None)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    name_list = port_forwarding_get_name_info(name)

    for name_key, name_value in name_list.items():
        if name_value == name:
            cmd_str = "%s.%s" %(UCI_FIREWALL_CONFIG_FILE, name_key)
            uci_config.delete_uci_config(cmd_str)

    return response_make_simple_success_body(None)

def port_forwarding_config_uci_add(host_str, name):
    name_info = dict()
    uci_config = ConfigUCI(UCI_FIREWALL_CONFIG_FILE, UCI_PORT_FORWARDING_CONFIG, None)
    uci_config.add_uci_config(host_str)

    output, error = subprocess_open(UCI_SHOW_CMD + UCI_FIREWALL_CONFIG_FILE + "| tail -1")
    if error:
        return name_info

    line = output.splitlines()[0]
    name_key = line.split('.')[1].split('=')[0]
    name_value = name
    name_info[name_key] = name_value

    cmd_str = "uci set firewall.%s.target='DNAT'" % name_key
    output, error = subprocess_open(cmd_str)

    return name_info

def port_forwarding_config_uci_set(req_data, name_key):
    uci_config = ConfigUCI(UCI_FIREWALL_CONFIG_FILE, UCI_PORT_FORWARDING_CONFIG, name_key)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    str_value = ""
    for value in req_data['protocol']:
        str_value = str_value + " " + value

    req_data['protocol'] = "'%s'" % str_value.strip()
    req_data['externalAddr'] = ""
    if not req_data['internalAddr']:
        isBridge, bridgeList = device_get_if_bridge_mode()
        if isBridge == True:
            req_data['internalAddr'] = device_info_get_ip_address('br-lan')
        else:
            req_data['internalAddr'] = device_info_get_ip_address(LAN_ETHDEV)

    uci_config.set_uci_config(req_data)

def port_forwarding_get_name_info(name):
    '''
    Extract host number from 'host' section config
    '''
    name_info = dict()
    if name:
        name_str = "\"name='" + name + "'\""
        filter_cmd = " | grep '@redirect'" + " | grep " + name_str
    else:
        filter_cmd = " | grep '@redirect'" + " | grep name"

    output, error = subprocess_open(UCI_SHOW_CMD + UCI_FIREWALL_CONFIG_FILE + filter_cmd)
    if error:
        return name_info

    if output :
        lines = output.splitlines()
        for line in lines:
            token = line.split('.')
            name_key = token[1]
            name_value = token[2].split('=')[1].strip("'")
            name_info[name_key] = name_value
        return name_info
    else:
        return name_info
