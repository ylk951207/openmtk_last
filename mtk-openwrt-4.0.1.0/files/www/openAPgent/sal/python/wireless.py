import os
from common.env import *
from common.misc import *
from common.file import*
from common.message import *
from common.sysinfo import *


WIRELESS_COMMON_CONFIG = "wireless_common_config"
WIRELESS_SEARCH_CONFIG = "wireless_search_config"


'''
Wireless LAN setting type information list
2G is actually 2.4G, but URL cannot interpret '.' character. TODO.. 
'''
ap_type_list = {
    "2G_default" : "ra0",
    "2G_guest1"  : "ra1",
    "2G_guest2"  : "ra2",
    "5G_default" : "rai0",
    "5G_guest1"  : "rai1",
    "5G_guest2"  : "rai2",
}

'''
WPS enable is 7, disable is 0 (UCI configuration)
'''
WPS_ENABLE_SIGNAL = "7"
WPS_DISABLE_SIGNAL = "0"

'''
Wireless 802.11 protocol supported mode with UCI config value 
key is UCI value, value is protocol 
'''
wireless_mode_data = {
    0  : '802.11 b/g mixed',
    1  : '802.11 b only',
    2  : '802.11 a only',
    4  : '802.11 g only',
    8  : '802.11 a/n in 5 band',
    9  : '802.11 b/g/gn mode',
    14 : '802.11 a/ac/an mixed',
    15 :  '802.11 ac/an mixed'
}

'''
Classify wireless authentication and Encryption to the specific types.
TODO: Type 3 for 'WPA2, WPA1WPA2, IEEE802.1x' needs RADIUS server configuration. 
'''
auth_priv_model = {
    "Type1" : {
        'DISABLE' : ['NONE'],
        'OPEN' : ['WEP'],
        'SHARED' : ['WEP'],
        'WEPAUTO' : ['WEP']},
    "Type2" : {
        'WPA2PSK' : ['AES', 'TKIP', 'TKIPAES'],
        'WPAPSKWPA2PSK' : ['AES', 'TKIP', 'TKIPAES']
    }
}

FILE_HEADER_TEXT = "# Generated by mtkwifi.lua\nDefault\n"

def wireless_get_config_file(ap_type):
    if "5G_" in ap_type:
        data_file_name = MT7615_1_DAT_CONFIG_FILE
    elif "2G_" in ap_type:
        data_file_name = MT7622_1_DAT_CONFIG_FILE
    else:
        return None

    return data_file_name


def wireless_get_device_info(ap_type, if_name):
    if "2G_" in ap_type:
        device_name = TWO_GIGA_DEVICE_NAME
        if_index = if_name.strip('ra')
    elif "5G_" in ap_type:
        device_name = FIVE_GIGA_DEVICE_NAME
        if_index = if_name.strip('rai')
    else:
        return None, None

    return device_name, int(if_index)

def wireless_module_restart(enable, ifname, devname):
    if os.path.exists(PROVISIONING_DONE_FILE):
        noti_data = dict()
        noti_data['enable'] = enable
        noti_data['ifname'] = ifname
        noti_data['devname'] = devname
        server_msg = ApServerLocalMassage(APNOTIFIER_CMD_PORT)
        server_msg.send_message_to_apnotifier(SAL_WIFI_MODULE_RESTART, noti_data)
        log_info(WIRELESS_COMMON_CONFIG, "** Send wifi module restart message to apClient **")
    else:
        log_info(WIRELESS_COMMON_CONFIG, "Cannot find provisioining file(%s)" % PROVISIONING_DONE_FILE)

'''
Wireless configuration GET, SET
'''
def py_wireless_config_list():
    wireless_body = list()

    for ap_type, if_name in ap_type_list.items():
        log_info(WIRELESS_COMMON_CONFIG, "[ap type] : " + ap_type)

        if device_info_get_hwaddr(if_name) != '':
            wireless_data = py_wireless_config_retrieve(ap_type, 0)
            if wireless_data:
                wireless_body.append(wireless_data)

    data = {
        "wireless-list": wireless_body
    }
    return response_make_simple_success_body(data)

def py_wireless_config_create(request):
    return wireless_config_set(request)

def py_wireless_config_update(request):
    return wireless_config_set(request)

def py_wireless_config_retrieve(ap_type, add_header):
    if not ap_type in ap_type_list:
        return response_make_simple_error_body(500, "Unknown AP Type", None)

    wireless_config_file = wireless_get_config_file(ap_type)
    if wireless_config_file == None:
        return response_make_simple_error_body(500, "No such wireless configuration file.", None)

    wireless_data = wireless_config_get(wireless_config_file, ap_type)

    if add_header == 1:
        data = {
            "wireless": wireless_data,
            'header': {
                'resultCode': 200,
                'resultMessage': 'Success.',
                'isSuccessful': 'true'
            }
        }
    else:
        data = wireless_data
    return data

def py_wireless_config_detail_create(request, ap_type):
    return wireless_config_detail_set(request, ap_type)

def py_wireless_config_detail_update(request, ap_type):
    return wireless_config_detail_set(request, ap_type)


def wireless_config_get(wireless_config_file, ap_type):
    wireless_data = dict()

    if_name = ap_type_list[ap_type]

    dev_file = "/sys/class/net/" + if_name
    if not os.path.exists(dev_file):
        log_error(WIRELESS_COMMON_CONFIG, "No such interface(%s)" %if_name)
        return None

    device_name, if_index = wireless_get_device_info(ap_type, if_name)
    if device_name == None or if_index == None:
        log_error(WIRELESS_COMMON_CONFIG, "wireless_get_device_info() failed: device_name(%s), if_index(%d)" %(device_name, if_index))
        return None

    config_index = str(if_index + 1)

    file_config = ConfigFileProc(WIRELESS_COMMON_CONFIG, WIRELESS_MEDIATEK_CONFIG_PATH + wireless_config_file, config_index)
    if file_config.section_map == None:
        log_error(WIRELESS_COMMON_CONFIG, "file_config.section_map is null")
        return None

    file_config.get_file_data_section_map(DELIMITER_EQUEL)

    for map_key, map_val in file_config.section_map.items():
        if "internal_" in map_key:
            continue
        wireless_data[map_key] = map_val[2]

    auth_mode = wireless_data['authMode']
    priv_mode = wireless_data['privacyMode']

    type = wireless_get_auth_priv_type(auth_mode, priv_mode)

    log_info(WIRELESS_COMMON_CONFIG, "-< Current wireless data, %s > : %s" %(type, str(wireless_data)))

    '''
    Change password as auth/priv type
    '''
    if auth_mode == "OPEN" and priv_mode == "NONE":
        wireless_data['authMode'] = "DISABLE"

    if type == "Type1":
        wireless_data['password'] = file_config.section_map['internal_Key1Str1'][2]
    else:
        wireless_data['password'] = file_config.section_map['internal_WPAPSK1'][2]

    wireless_data['bssid'] = device_info_get_hwaddr(if_name)
    wireless_data['devName'] = device_name
    wireless_data['type'] = ap_type

    if wireless_data['wps'] == WPS_ENABLE_SIGNAL:
        wireless_data['wps'] = True
    else:
        wireless_data['wps'] = False

    wireless_data['mode'] = wireless_convert_integer_to_mode_type(wireless_data['mode'])

    status = device_get_wireless_state(if_name)
    wireless_data['enable'] = status

    if status == True:
        wireless_data['status'] = 'connected'
    else:
        wireless_data['status'] = 'disconnected'

    '''
    TODO: Guest Value Handling 
    '''

    return wireless_data

def wireless_config_set(request):

    wireless_list = request['wireless-list']
    while len(wireless_list) > 0:
        wireless_field = wireless_list.pop(0)
        for ap_type, value in ap_type_list.items():
            if wireless_field['type'] == ap_type:
                wireless_config_detail_set(wireless_field, ap_type)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def wireless_chagne_request_data_to_file_config(request):
    mod_request = request

    for req_key, req_val in request.items():
        if req_key == 'wps':
            if req_val == True:
                mod_request['wps'] = WPS_ENABLE_SIGNAL
            else:
                mod_request['wps'] = WPS_DISABLE_SIGNAL
        elif req_key == 'authMode':
            auth_mode = request['authMode']
            priv_mode = request['privacyMode']
            passwd = request['password']
            mod_request = wireless_chagne_auth_request_data_to_file_config(mod_request, auth_mode, priv_mode, passwd)
            if not mod_request:
                return None
        elif req_key == 'mode':
            mod_request['mode'] = wireless_convert_mode_type_to_integer(req_val)
            if not mod_request['mode']:
                return None
        else:
            continue
    if mod_request:
        log_info(WIRELESS_COMMON_CONFIG, "mod_request : " + str(mod_request))
    return mod_request

def wireless_chagne_auth_request_data_to_file_config(mod_request, auth_mode, priv_mode, passwd):
    type = wireless_get_auth_priv_type(auth_mode, priv_mode)
    if type == "Type1":
        if priv_mode == "WEP":
            mod_request['internal_DefaultKeyID'] = 1
            mod_request['internal_Key1Str1'] = passwd
            mod_request['internal_WscModeOption'] = 0
        else:
            mod_request['internal_RekeyMethod'] = 'DISABLE'
            mod_request['privacyMode'] = 'NONE'
            mod_request['authMode'] = 'OPEN'
    elif type == "Type2":
        mod_request['internal_DefaultKeyID'] = 2
        mod_request['internal_WPAPSK1'] = passwd
        mod_request['internal_RekeyMethod'] = 'TIME'
    else:
        return None
    return mod_request

def wireless_config_detail_set(request, ap_type):
    log_info(WIRELESS_COMMON_CONFIG, "request data = ", str(request))

    if not ap_type == request["type"]:
        return response_make_simple_error_body(500, "Invalid AP Type", None)

    if_name = ap_type_list[ap_type]
    device_name, if_index = wireless_get_device_info(ap_type, if_name)
    if device_name == None or if_index == None:
        return None

    wireless_config_file = wireless_get_config_file(ap_type)
    if wireless_config_file == None:
        return response_make_simple_error_body(500, "No such wireless configuration file.", None)

    config_index = str(if_index + 1)
    file_config = ConfigFileProc(WIRELESS_COMMON_CONFIG, WIRELESS_MEDIATEK_CONFIG_PATH + wireless_config_file, config_index)
    if file_config.section_map == None:
        return response_make_simple_error_body(500, "Not found file configuration", None)

    mod_request = wireless_chagne_request_data_to_file_config(request)
    if not mod_request:
        return response_make_simple_error_body(500, "Invalid set value", None)

    file_config.write_file_data(mod_request, DELIMITER_EQUEL, FILE_HEADER_TEXT)

    '''
    Wireless Enable/Disable Processing
    '''
    wireless_module_restart(request['enable'], if_name, device_name)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def wireless_get_auth_priv_type(auth_mode, priv_mode):
    for type_key, dict_values in auth_priv_model.items():
        for auth_key, priv_list in dict_values.items():
            if auth_mode != auth_key:
                continue
            if priv_mode in priv_list:
                log_info(WIRELESS_COMMON_CONFIG,
                         "Current auth_mode %s priv_mode %s -> type %s" % (auth_mode, priv_mode, type_key))
                return type_key
            else:
                log_error(WIRELESS_COMMON_CONFIG, "Not support auth-priv mode (%s-%s)" %(auth_mode, priv_mode))
                return None
    return None

'''
Change the mode type to a matching number(802.11 b only -> 1, 802.11 g only -> 4 ...)
'''
def wireless_convert_mode_type_to_integer(mode_id):
    for key,val in wireless_mode_data.items():
        if val == mode_id:
            return key
    return ""


'''
Change the number to a matching mode type(1 -> 802.11 b only , 4 -> 802.11 g only...)
'''
def wireless_convert_integer_to_mode_type(mode_id):
    if mode_id in wireless_mode_data.keys():
        return wireless_mode_data[mode_id]
    else:
        return None


'''
Wireless Station GET
'''
def py_wireless_station_list():
    pass