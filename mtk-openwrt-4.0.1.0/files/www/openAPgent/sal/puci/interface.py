import fileinput
import os
from puci import *
from common.env import *
from common.misc import *
from common.message import *
from common.sysinfo import device_info_get_dns_server

UCI_NETWORK_FILE="network"
UCI_INTERFACE_COMMON_CONFIG = "interface_config"
UCI_INTERFACE_V4ADDR_CONFIG = "interface_v4addr_config"

UCI_INTERFACE_LIST_STR='interfaces-list'
UCI_INTERFACE_STR='interface'
UCI_INTERFACE_V4ADDR_STR='v4Addr'
UCI_INTERFACE_V6ADDR_STR='v6Addr'



def interface_puci_module_restart(iflist):
    noti_data = dict()
    noti_data['config_file'] = UCI_NETWORK_FILE
    noti_data['iflist'] = iflist
    puci_send_message_to_apnotifier(SAL_PUCI_MODULE_RESTART, noti_data)

'''
InterfaceConfig
'''
def puci_interface_config_list():
    iflist=['lan', 'wan', 'wan6']

    for i in range (0, len(iflist)):
        rc = puci_interface_config_retrieve(iflist[i], 0)
        if i == 0:
            iflist_body = [rc]
        else:
            iflist_body.append(rc)

    data = {
            UCI_INTERFACE_LIST_STR : iflist_body,
            'header' : {
                        'resultCode':200,
                        'resultMessage':'Success.',
                        'isSuccessful':'true'
            }
    }
    return data

def puci_interface_config_retrieve(ifname, add_header):
    if not ifname:
        return response_make_simple_error_body(500, "Not found interface name", None)

    log_info(UCI_NETWORK_FILE, "[ifname] : " + ifname)

    interface_data = dict()

    interface_data = interface_config_common_uci_get(ifname, interface_data)
    interface_data = interface_config_v4addr_uci_get(ifname, interface_data)

    if add_header == 1:
        data = {
            UCI_INTERFACE_STR : interface_data,
            'header' : {
                            'resultCode':200,
                            'resultMessage':'Success.',
                            'isSuccessful':'true'
            }
        }
    else:
        data = interface_data

    return data

def puci_interface_config_create(request):
    return interface_config_common_set(request)

def puci_interface_config_update(request):
    return interface_config_common_set(request)

def puci_interface_config_detail_create(request, ifname):
    return interface_config_common_detail_set(request, ifname)

def puci_interface_config_detail_update(request, ifname):
    return interface_config_common_detail_set(request, ifname)



def interface_config_common_set(request):
    interface_list = request[UCI_INTERFACE_LIST_STR]
    req_dns_data = dict()
    iflist = list()
    wan_static = False

    while len(interface_list) > 0:
        ifdata = interface_list.pop(0)
        ifname = ifdata['ifname']

        req_dns_data = interface_config_get_request_dns_data(ifname, ifdata['v4Addr'], ifdata['protocol'])
        if req_dns_data:
            ifdata['v4Addr']['dnsServer'].reverse()

        if ifname == 'wan' and ifdata['protocol'] == 'static':
            wan_static = True

        interface_config_common_uci_set(ifdata, ifname)
        if UCI_INTERFACE_V4ADDR_STR in ifdata:
            interface_config_v4addr_uci_set(ifdata[UCI_INTERFACE_V4ADDR_STR], ifname)
        iflist.append(ifname)

    # To return current dns server
    interface_config_update_dhcp_config(req_dns_data, wan_static)

    interface_puci_module_restart(iflist)


    data = {
        'header' : {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def interface_config_common_detail_set(request, ifname):
    if not ifname:
        return response_make_simple_error_body(500, "Not found interface name", None)

    log_info(UCI_NETWORK_FILE, "ifname[%s]" %ifname)

    req_dns_data = interface_config_get_request_dns_data(ifname, request['v4Addr'], request['protocol'])
    if req_dns_data:
        request['v4Addr']['dnsServer'].reverse()

    interface_config_common_uci_set(request, ifname)
    if UCI_INTERFACE_V4ADDR_STR in request:
        interface_config_v4addr_uci_set(request[UCI_INTERFACE_V4ADDR_STR], ifname)

    wan_static = False
    if ifname == 'wan' and request['protocol'] == 'static':
        wan_static = True

    # To return current dns server
    interface_config_update_dhcp_config(req_dns_data, wan_static)

    interface_puci_module_restart([ifname])

    data = {
        'header' : {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def interface_config_common_uci_get(ifname, interface_data):
    uci_config = ConfigUCI(UCI_NETWORK_FILE, UCI_INTERFACE_COMMON_CONFIG, ifname)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.show_uci_config()

    interface_data['ifname'] = ifname
    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]
        interface_data[map_key] = map_val[2]

    return interface_data

def interface_config_common_uci_set(req_data, ifname):
    if not ifname:
        return response_make_simple_error_body(500, "Not found interface name", None)

    uci_config = ConfigUCI(UCI_NETWORK_FILE, UCI_INTERFACE_COMMON_CONFIG, ifname)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.set_uci_config(req_data)

def puci_interface_v4addr_config_list(ifname):
    if not ifname:
        return response_make_simple_error_body(500, "Not found interface name", None)

    interface_data = dict()
    interface_data = interface_config_v4addr_uci_get(ifname, interface_data)

    data = interface_data
    data['header'] = {
        'resultCode':200,
        'resultMessage':'Success.',
        'isSuccessful':'true'
    }
    return data

def puci_interface_v4addr_config_create(request, ifname):
    return interface_config_v4addr_set(request, ifname)

def puci_interface_v4addr_config_update(request, ifname):
    return interface_config_v4addr_set(request, ifname)

def interface_config_v4addr_set(request, ifname):
    if not ifname:
        return response_make_simple_error_body(500, "Not found interface name", None)

    # TODO: If 'proto' config isn't 'static', return with error
    req_dns_data = interface_config_get_request_dns_data(ifname, request, 'static')
    if req_dns_data:
        request['dnsServer'].reverse()

    error_msg = interface_config_v4addr_uci_set(request, ifname)
    if error_msg:
        return error_msg

    # To return current dns server
    interface_config_update_dhcp_config(req_dns_data, True)
    interface_puci_module_restart([ifname])

    data = {
        'header' : {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def interface_config_v4addr_uci_get(ifname, interface_data):
    addr_data = dict()

    uci_config = ConfigUCI(UCI_NETWORK_FILE, UCI_INTERFACE_V4ADDR_CONFIG, ifname)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.show_uci_config()

    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]
        addr_data[map_key] = map_val[2]

    interface_data[UCI_INTERFACE_V4ADDR_STR] = addr_data

    log_info(UCI_NETWORK_FILE, interface_data)

    return interface_data

def interface_config_v4addr_uci_set(req_data, ifname):

    uci_config = ConfigUCI(UCI_NETWORK_FILE, UCI_INTERFACE_V4ADDR_CONFIG, ifname)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.set_uci_config(req_data)

'''
If dnsServer is changed, Update /etc/config/dhcp
'''
def interface_config_update_dhcp_config(req_dns_data, wan_static):
    dns_list = list()
    # Get dns server
    dns_data = device_info_get_dns_server(None)

    if req_dns_data and LAN_DNS_SERVER_KEY in req_dns_data:
        if len(req_dns_data[LAN_DNS_SERVER_KEY]) > 0:
            dns_list = req_dns_data[LAN_DNS_SERVER_KEY]

    '''
    If LAN config doesn't include dns server, apply WAN dns servers.
    '''
    if len(dns_list) <= 0:
        if wan_static == True:
            if req_dns_data and WAN_DNS_SERVER_KEY in req_dns_data:
                dns_list = req_dns_data[WAN_DNS_SERVER_KEY]
        else:
            dns_list = dns_data[WAN_DNS_SERVER_KEY]

    option_list = []
    if len(dns_list) > 0:
        option_str = "6"
        for dns_server in dns_list:
            if dns_server in option_str:
                continue
            option_str = option_str + "," + dns_server
        if "," in option_str:
            option_list.append(option_str)

    dhcp_option = {'dhcpOptions' : option_list}

    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_INTERFACE_POOL_CONFIG, 'lan')
    if uci_config.section_map != None:
        uci_config.set_uci_config(dhcp_option)


def interface_config_get_request_dns_data(ifname, req_v4addr, protocol):
    req_dns_data = dict()

    '''
    LAN interface only can support manual DNS configuration. 
    '''
    if ifname == 'wan' and protocol == 'static':
        if req_v4addr['dnsServer'] and len(req_v4addr['dnsServer']) > 0 :
            req_dns_data[WAN_DNS_SERVER_KEY] = req_v4addr['dnsServer']
            return req_dns_data
    elif ifname == 'lan':
        if not req_v4addr['dnsServer']:
            return None

        # copy original data, because req_data will be modified..
        if len(req_v4addr['dnsServer']) > 0:
            req_dns_data[LAN_DNS_SERVER_KEY] = list(req_v4addr['dnsServer'])
            return req_dns_data

    return None

'''
GenericIfStats
stats = [[ifname, inBytes, inPkts, inErr, inDrop, outBytes, outPkts, outErr, outDrop]] 
'''
def generic_ifstats_get(ifname):
    #Get port traffic from /proc/net/dev file
    stats=None
    port_count = 0
    for line in fileinput.input([PROC_NET_DEV_PATH]):
        if not line:
            break
        if not ':' in line:
            continue
        line = line.replace("\n", "")
        token = line.split()

        if ifname:
            if line.find(ifname) == -1:
                continue
            stats = [[ifname, token[1], token[2], token[3], token[4], token[9], token[10], token[11], token[12]]]
            break
        else:
            if port_count == 0:
                stats = [[token[0], token[1], token[2], token[3], token[4], token[9], token[10], token[11], token[12]]]
            else:
                stats.append([token[0], token[1], token[2], token[3], token[4], token[9], token[10], token[11], token[12]])
        port_count = port_count + 1

    fileinput.close()
    return stats, port_count


def puci_if_statistics_list():
    stats, port_count = generic_ifstats_get('')

    for index in range(0, port_count):
        temp = {
                'ifName':stats[index][0].strip(':'),
                'ifIndex':0,
                'rxBytes':stats[index][1],
                'rxPkts':stats[index][2],
                'rxError':stats[index][3],
                'rxDrop': stats[index][4],
                'txBytes':stats[index][5],
                'txPkts':stats[index][6],
                'txError' : stats[index][7],
                'txDrop': stats[index][8],
        }
        if index == 0:
            ifstats_body = [temp]
        else:
            ifstats_body.append(temp)
        index = index + 1

    data = {
            'generic-ifstats': ifstats_body,
            'header':{
            'resultCode':200,
            'resultMessage':'Success.',
            'isSuccessful':'true'
            }
    }
    return data


def puci_if_statistics_retrieve(ifname, add_header):
    if not ifname:
        return response_make_simple_error_body(500, "Not found interface name", None)

    log_info(UCI_NETWORK_FILE, "[ifName] : " + ifname)

    stats, port_count = generic_ifstats_get(ifname)
    if not stats: return None

    ifstats_body = {
            'ifName':stats[0][0].strip(':'),
            'ifIndex':0,
            'rxBytes':stats[0][1],
            'rxPkts':stats[0][2],
            'rxError': stats[0][3],
            'rxDrop': stats[0][4],
            'txBytes':stats[0][5],
            'txPkts':stats[0][6],
            'txError': stats[0][7],
            'txDrop': stats[0][8],
    }

    data = {
            'generic-ifstats': ifstats_body,
            'header':{
            'resultCode':200,
            'resultMessage':'Success.',
            'isSuccessful':'true'
        }
    }
    return data
