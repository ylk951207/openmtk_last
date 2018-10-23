from random import *

from puci import *
from common.env import *
from common.misc import *


UCI_SNMP_CONFIG_FILE = "snmpd"
UCI_SNNP_COMMUNITY_CONFIG = "snmp_community_config"
UCI_SNNP_TRAPHOST_CONFIG = "snmp_traphost_config"


def snmp_puci_module_restart():
    noti_data = dict()
    noti_data['config_file'] = UCI_SNMP_CONFIG_FILE
    noti_data['container_name'] = "net-snmp"
    puci_send_message_to_apnotifier(SAL_PUCI_MODULE_RESTART, noti_data)

'''
SNMP Config
'''
def puci_snmp_config_list():
    community_data_list = list()
    traphost_data_list = list()

    community_list = snmp_config_get_uci_section_value("com2sec")
    for i in range(0, len(community_list)):
        community_data = snmp_config_uci_get(UCI_SNNP_COMMUNITY_CONFIG, community_list[i])
        community_data_list.append(community_data)

    traphost_list = snmp_config_get_uci_section_value("trap_HostName")
    for i in range(0, len(traphost_list)):
        traphost_data = snmp_config_uci_get(UCI_SNNP_TRAPHOST_CONFIG, traphost_list[i])
        traphost_data_list.append(traphost_data)

    data = {
        "snmp" : {
            "snmpVersion" : ["v1", "v2c"],
            "community": community_data_list,
            "traphost": traphost_data_list,
        },
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
    log_info(UCI_SNMP_CONFIG_FILE, "request data = ", request)

    community_list = request['community']
    version_list = request['snmpVersion']
    traphost_list = request['traphost']

    snmp_config_initialize()

    for i in range(0, len(community_list)):
        community = community_list[i]
        community = snmp_community_config_set_default_value(community, version_list)
        snmp_config_uci_set(community, UCI_SNNP_COMMUNITY_CONFIG, community['community'], version_list)

    for i in range(0, len(traphost_list)):
        traphost = traphost_list[i]
        traphost_name = "traphost_" + str(randint(1, 100000))
        traphost = snmp_traphost_config_set_default_value(traphost)
        snmp_config_uci_set(traphost, UCI_SNNP_TRAPHOST_CONFIG, traphost_name, None)

    snmp_puci_module_restart()

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data


def snmp_community_config_set_default_value (community, version_list):
    community_data = dict()

    community_str = community['community']
    community_type = community['communityType']

    #community_data['com2sec'] = "com2sec"
    community_data['community'] = community_str
    community_data['communityType'] = community_type
    community_data['source'] = "default"

    #community_data['v1Group'] = "group"
    if "v1" or "v2c" or "usm" in version_list:
        community_data['v1GroupName'] = community_str
        community_data['v1Version'] = "v1"
        community_data['v1Secname'] = community_type

    #community_data['v2Group'] = "group"
    if "v2c" or "usm" in version_list:
        community_data['v2GroupName'] = community_str
        community_data['v2Version'] = "v2c"
        community_data['v2Secname'] = community_type

    #community_data['usmGroup'] = "group"
    if "usm" in version_list:
        community_data['usmGroupName'] = community_str
        community_data['usmVersion'] = "usm"
        community_data['usmSecname'] = community_type

    #community_data['access'] = "access"
    community_data['accessGroup'] = community_str
    community_data['context'] = "none"
    community_data['version'] = "any"
    community_data['level'] = "noauth"
    community_data['prefix'] = "exact"
    community_data['read'] = "all"
    if community_type == "ro":
        community_data['write'] = "none"
        community_data['notify'] = "none"
    else:
        community_data['write'] = "all"
        community_data['notify'] = "all"

    return community_data


def snmp_traphost_config_set_default_value (traphost):
    traphost_data = dict()

    #traphost_data['trapHostName'] = "trap_HostName"
    traphost_data['trapHost'] = traphost['trapHost']

    if traphost['trapVersion'] == "v1":
        traphost_data['trapVersion'] = "trapsink"
    elif traphost['trapVersion'] == "v2":
        traphost_data['trapVersion'] = "trap2sink"

    traphost_data['trapCommunity'] = traphost['trapCommunity']

    return traphost_data


def snmp_config_uci_get(uci_config_name, value):
    snmp_data = dict()
    uci_config = ConfigUCI(UCI_SNMP_CONFIG_FILE, uci_config_name, value)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.show_uci_config()

    for map_key, map_val in uci_config.section_map.items():
        if uci_config_name == UCI_SNNP_COMMUNITY_CONFIG:
            if map_key == "community" or map_key == "communityType":
                snmp_data[map_key] = map_val[2]
        elif uci_config_name == UCI_SNNP_TRAPHOST_CONFIG:
            if map_key == "trapHost" or map_key == "trapCommunity":
                snmp_data[map_key] = map_val[2]
            if map_key == "trapVersion":
                if map_val[2] == "trapsink":
                    snmp_data[map_key] = "v1"
                elif map_val[2] == "trap2sink":
                    snmp_data[map_key] = "v2"

    return snmp_data

def snmp_config_initialize():
    community_list = snmp_config_get_uci_section_value("com2sec")
    traphost_list = snmp_config_get_uci_section_value("trap_HostName")

    uci_config = ConfigUCI(UCI_SNMP_CONFIG_FILE, UCI_SNNP_COMMUNITY_CONFIG, None)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    for i in range(0, len(community_list)):
        uci_config.delete_uci_config("snmpd." + community_list[i])
        uci_config.delete_uci_config("snmpd." + community_list[i] + "_v1")
        uci_config.delete_uci_config("snmpd." + community_list[i] + "_v2c")
        uci_config.delete_uci_config("snmpd." + community_list[i] + "_usm")
        uci_config.delete_uci_config("snmpd." + community_list[i] + "_access")

    for i in range(0, len(traphost_list)):
        uci_config.delete_uci_config("snmpd." + traphost_list[i])


def snmp_config_uci_set(req_data, config_name, value, version_list):
    uci_config = ConfigUCI(UCI_SNMP_CONFIG_FILE, config_name, value)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    if config_name == UCI_SNNP_COMMUNITY_CONFIG:
        uci_config.set_uci_config_scalar("snmpd."+value, "com2sec")
        if "v1" in version_list:
            uci_config.set_uci_config_scalar("snmpd." + value + "_v1", "group")
        if "v2c" in version_list:
            uci_config.set_uci_config_scalar("snmpd." + value + "_v2c", "group")
        if "usm" in version_list:
            uci_config.set_uci_config_scalar("snmpd." + value + "_usm", "group")
        uci_config.set_uci_config_scalar("snmpd." + value + "_access", "access")
    else:
        uci_config.set_uci_config_scalar("snmpd." + value, "trap_HostName")

    uci_config.set_uci_config(req_data)


'''
section is com2sec or trap_HostName
'''
def snmp_config_get_uci_section_value(section):
    section_list = list()
    awk_cmd = " | awk '{result=substr($1,7,1000); print result}'"
    filter_cmd = " | grep " + section + awk_cmd

    output, error = subprocess_open(UCI_SHOW_CMD + UCI_SNMP_CONFIG_FILE + filter_cmd)
    if error:
        return section_list

    if output :
        line = output.splitlines()
        for token in line:
            section_list.append(token.split('=')[0])
        return section_list
    else:
        return section_list
