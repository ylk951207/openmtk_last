import fileinput
import subprocess
import shlex

from puci import *
from common.log import *
from common.env import *

UCI_DHCP_CONFIG_FILE = "dhcp"
UCI_DHCP_COMMON_CONFIG = "dhcp_common"
UCI_DHCP_INTERFACE_POOL_CONFIG = "dhcp_interface_pool"
UCI_DHCP_INTERFACE_V6POOL_CONFIG = "dhcp_interface_v6pool"
UCI_DHCP_STATIC_LEASE_CONFIG = "dhcp_static_leases"
UCI_DHCP_V6POOL_STR = "v6Settings"


'''
DHCP Common Config
'''
def puci_dhcp_common_config_list():
    dhcp_common_data = dict()
    dhcp_common_data = dhcp_config_common_uci_get(UCI_DHCP_COMMON_CONFIG, dhcp_common_data)
    data = {
        "dhcp-dns": dhcp_common_data,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def puci_dhcp_common_config_create(request):
    return dhcp_common_config_set(request)

def puci_dhcp_common_config_update(request):
    return dhcp_common_config_set(request)

def dhcp_common_config_set(request):
    log_info(LOG_MODULE_SAL, "request data = ", request)

    dhcp_common_config_uci_set(request, UCI_DHCP_COMMON_CONFIG)

    noti_data = dict()
    noti_data['config_file'] = UCI_SYSTEM_CONFIG_FILE
    puci_send_message_to_apnotifier(SAL_PUCI_MODULE_RESTART, noti_data)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def dhcp_config_common_uci_get(uci_file, dhcp_data):
    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, uci_file)
    if uci_config == None:
        raise RespNotFound("UCI Config")

    uci_config.show_uci_config()

    for map_key, map_val in uci_config.section_map.items():
        dhcp_data[map_key] = map_val[2]

    return dhcp_data

def dhcp_common_config_uci_set(req_data, uci_file):
    log_info(LOG_MODULE_SAL, "request data = ", req_data)

    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, uci_file)
    if uci_config == None:
        raise RespNotFound("UCI Config")

    uci_config.set_uci_config(req_data)


'''
DHCP Pool
'''
def puci_dhcp_pool_config_list():
    iflist = ['lan', 'wan']

    for i in range(0, len(iflist)):
        log_info(LOG_MODULE_SAL, "[ifname] : " + iflist[i])
        rc = puci_dhcp_pool_config_retrieve(iflist[i], 0)
        if i == 0:
            iflist_body = [rc]
        else:
            iflist_body.append(rc)

    data = {
        "dhcp-pool": iflist_body,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data


def puci_dhcp_pool_config_retrieve(ifname, add_header):
    if not ifname:
        raise RespNotFound("dhcp")

    log_info(LOG_MODULE_SAL, "[ifname] : " + ifname)

    dhcp_data = dict()

    dhcp_data = dhcp_pool_config_uci_get(ifname, dhcp_data)
    dhcp_data = dhcp_pool_v6pool_config_uci_get(ifname, dhcp_data)

    if add_header == 1:
        data = {
            'dhcp-pool': dhcp_data,
            'header': {
                'resultCode': 200,
                'resultMessage': 'Success.',
                'isSuccessful': 'true'
            }
        }
    else:
        data = dhcp_data
    return data

def puci_dhcp_pool_config_create(request):
    return dhcp_pool_config_set(request)

def puci_dhcp_pool_config_update(request):
    return dhcp_pool_config_set(request)

def puci_dhcp_pool_config_detail_create(request, ifname):
    return dhcp_pool_config_detail_set(request, ifname)

def puci_dhcp_pool_config_detail_update(request, ifname):
    return dhcp_pool_config_detail_set(request, ifname)

def dhcp_pool_config_set(request):
    dhcp_list = request['dhcp-pool']

    while len(dhcp_list) > 0:
        ifdata = dhcp_list.pop(0)

        ifname = ifdata['ifname']

        dhcp_pool_uci_set(ifdata, ifname)
        if UCI_DHCP_V6POOL_STR in ifdata:
            dhcp_pool_v6pool_config_uci_set(ifdata[UCI_DHCP_V6POOL_STR], ifname)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def dhcp_pool_config_detail_set(request, ifname):
    if not ifname:
        raise RespNotFound("dhcp")

    dhcp_pool_config_uci_set(request, ifname)
    if UCI_DHCP_V6POOL_STR in request:
        dhcp_pool_v6pool_config_uci_set(request[UCI_DHCP_V6POOL_STR], ifname)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def dhcp_pool_config_uci_get(ifname, dhcp_data):
    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_INTERFACE_POOL_CONFIG, ifname)
    if uci_config == None:
        raise RespNotFound("UCI Config")

    uci_config.show_uci_config()

    dhcp_data['ifname'] = ifname
    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]
        dhcp_data[map_key] = map_val[2]

    return dhcp_data

def dhcp_pool_config_uci_set(req_data, ifname):
    if not ifname:
        raise RespNotFound("dhcp")

    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_INTERFACE_POOL_CONFIG, ifname)
    if uci_config == None:
        raise RespNotFound("UCI Config")

    uci_config.set_uci_config(req_data)

def dhcp_pool_v6pool_config_uci_get(ifname, dhcp_data):
    pool_data = dict()

    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_INTERFACE_V6POOL_CONFIG, ifname)
    if uci_config == None:
        raise RespNotFound("UCI Config")

    uci_config.show_uci_config()

    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]
        pool_data[map_key] = map_val[2]

    dhcp_data[UCI_DHCP_V6POOL_STR] = pool_data

    log_info(LOG_MODULE_SAL, dhcp_data)

    return dhcp_data

def dhcp_pool_v6pool_config_uci_set(req_data, ifname):
    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_INTERFACE_V6POOL_CONFIG, ifname)
    if uci_config == None:
        raise RespNotFound("UCI Config")

    uci_config.set_uci_config(req_data)


'''
DHCP_Static_leases
'''
def puci_dhcp_static_leases_config_list():
    leases_body = list()
    host_info_list = dhcp_static_leases_config_get_info(None)

    while host_info_list:
        host_info = host_info_list.pop(0)
        leases_data = dhcp_static_leases_config_uci_get(host_info)
        leases_body.append(leases_data)

    data = {
        "static-lease-list": leases_body,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data


def puci_dhcp_static_leases_config_retrieve(name, add_header):
    host_info_list = dhcp_static_leases_config_get_info(name)
    leases_data = dhcp_static_leases_config_uci_get(host_info_list[0])

    data = {
        'static-lease': leases_data,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def puci_dhcp_static_leases_config_create(request):
    return dhcp_static_leases_config_set(request)

def puci_dhcp_static_leases_config_update(request):
    return dhcp_static_leases_config_set(request)


def puci_dhcp_static_leases_config_detail_create(request, name):
    return dhcp_static_leases_config_detail_set(request, name)


def puci_dhcp_static_leases_config_detail_update(request, name):
    return dhcp_static_leases_config_detail_set(request, name)


def dhcp_static_leases_config_set(request):
    leases_list = request['static-lease-list']

    host_info_list = dhcp_static_leases_config_get_info(None)

    while len(leases_list) > 0:
        leases_data = leases_list.pop(0)
        found = False

        for host_key, host_name in host_info_list.items():
            if host_name == leases_data['name']:
                dhcp_static_leases_config_uci_set(leases_data, host_key, host_name)
                found = True

        if found == False:
            host_info_list = dhcp_static_leases_config_uci_add('host')

            for host_key, host_name in host_info_list.items():
                dhcp_static_leases_config_uci_set(request, host_key, host_name)

    noti_data = dict()
    noti_data['config_file'] = UCI_DHCP_CONFIG_FILE
    puci_send_message_to_apnotifier(SAL_PUCI_MODULE_RESTART, noti_data)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def dhcp_static_leases_config_detail_set(request, name):
    host_info_list = dhcp_static_leases_config_get_info(name)

    if len(host_info_list) <= 0:
        host_info_list = dhcp_static_leases_config_uci_add('host')

    for host_key, host_name in host_info_list.items():
        dhcp_static_leases_config_uci_set(request, host_key, host_name)

    noti_data = dict()
    noti_data['config_file'] = UCI_DHCP_CONFIG_FILE
    puci_send_message_to_apnotifier(SAL_PUCI_MODULE_RESTART, noti_data)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data


def dhcp_static_leases_config_uci_get(host_info, leases_data):
    leases_data = dict()
    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_STATIC_LEASE_CONFIG, host_info)
    if uci_config == None:
        raise RespNotFound("UCI Config")

    uci_config.show_uci_config()

    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]
        leases_data[map_key] = map_val[2]

    return leases_data

def dhcp_static_leases_config_uci_add(req_data, host_str):
    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_STATIC_LEASE_CONFIG, None)
    if uci_config == None:
        raise RespNotFound("UCI Config")

    uci_config.add_uci_config(host_str)

    output, error = subprocess_open(UCI_SHOW_CMD + UCI_DHCP_CONFIG_FILE + "| tail -1")

    host_info = dict()
    host_line = output.splitlines()
    host_key = host_line.split('.')[0]
    host_name = host_line.split('=')[1]
    host_info[host_key] = host_name
    return host_info


def dhcp_static_leases_config_uci_set(req_data, host_key, host_name):
    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_STATIC_LEASE_CONFIG, host_key)
    if uci_config == None:
        raise RespNotFound("UCI Config")

    uci_config.set_uci_config(req_data)


def dhcp_static_leases_config_get_info(name):
    '''
    Extract host number from 'host' section config
    '''
    host_info = dict()
    awk_cmd = " | awk '{result=substr($1,6,1000); print result}'"
    if name:
        name_str = "name='" + name + "'"
        filter_cmd = " | grep grep '@host'" + " | grep " + name_str + awk_cmd
    else:
        filter_cmd = " | grep grep '@host'" + " | grep name" + awk_cmd

    output, error = subprocess_open(UCI_SHOW_CMD + UCI_DHCP_CONFIG_FILE + filter_cmd)
    if error:
        return None

    if output :
        host_line = output.splitlines()
        host_key =  host_line.split('.')[0]
        host_name = host_line.split('=')[1]
        host_info[host_key] = host_name
    else:
        return None





