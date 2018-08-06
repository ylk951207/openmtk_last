import fileinput

from puci import *

from common.log import *
from common.env import *

UCI_NETWORK_CONFIG="interfaceConfig"




def _interface_config_make_response(uci_config):
    interface = dict()

    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]

        if '.' in map_key:
            token = map_key.split('.')
            token_len = len(token)
            if token_len > 1:
                if not token[0] in interface.keys():
                    interface[token[0]] = dict()

                sub = interface[token[0]]
                sub[token[1]] = map_val[2]
                    
            elif token_len > 2:
                if not token[0] in interface.keys():
                    interface[token[0]] = dict()

                sub = interface[token[0]]
                if not token[1] in sub.keys():
                    sub[token[1]] = dict()

                sub_sub = sub[token[1]]
                sub_sub[token[2]] = map_val[2]
        else:     
            interface[map_key] = map_val[2]

    data = {
            'interface': interface,
    }
    log_info(LOG_MODULE_SAL, "Response =", data)
    return data


'''
InterfaceConfig
'''
def interface_config_list():
    iflist=['lan', 'wan', 'wan6']

    for i in range (0, len(iflist)):
        log_info(LOG_MODULE_SAL, "[ifname] : " + iflist[i])
        rc = interface_config_retrieve(iflist[i], 0)
        if i == 0:
            iflist_body = [rc]
        else:
            iflist_body.append(rc)

    data = {
            'interface_list': iflist_body,
            'header' : {
                        'resultCode':200,
                        'resultMessage':'Success.',
                        'isSuccessful':'true'
                       }
            }
    return data


def interface_config_retrieve(ifname, add_header):
    if not ifname: return None
    log_info(LOG_MODULE_SAL, "[ifname] : " + ifname)
    
    uci_config = ConfigUCI(UCI_NETWORK_CONFIG, ifname)
    uci_config.show_uci_config(ifname)
    
    data = _interface_config_make_response(uci_config)

    if add_header == 1:
        data['header'] =  {
                            'resultCode':200,
                            'resultMessage':'Success.',
                            'isSuccessful':'true'
                           }

    return data

def interface_config_create(req, ifname):
    # Get ifname from URI
    if not ifname: return None
    log_info(LOG_MODULE_SAL, "[ifname] : " + ifname)

    uci_config = ConfigUCI(UCI_NETWORK_CONFIG, ifname)

    for req_key in req.keys():
        req_val = req[req_key]
        # Check dictionary value
        if isinstance(req_val, dict):
            for sub_k, sub_v in req_val.items():
                mval_k = req_key + '.' + sub_k
                mval_v = sub_v
        else:
            mval_k = req_key
            mval_v = req[req_key]
            
        if mval_k in uci_config.section_map:
            map_val = uci_config.section_map[mval_k]
            map_val[2] = uci_config.convert_config_value(mval_v)

    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]
        if map_val[2]:
            if map_val[0] == CONFIG_TYPE_SCALAR:
                uci_config.set_uci_config(map_val[1], str(map_val[2]))
            else:
                uci_config.delete_uci_config(map_val[1])
                uci_config.set_uci_config_list_value(req, map_val[1], map_val[2])

        # TODO: elif, value is not set, call DELETE handler 

    uci_config.restart_module()

    iflist_body = _interface_config_make_response(uci_config)

    data = {
            'interface_list': iflist_body,
            'header' : {
                        'resultCode':200,
                        'resultMessage':'Success.',
                        'isSuccessful':'true'
                       }
            }
    
    return data

def interface_config_update(req, ifname):
    # Get ifname from URI
    if not ifname: return None
    log_info(LOG_MODULE_SAL, "[ifname] : " + ifname)

    uci_config = ConfigUCI(UCI_NETWORK_CONFIG, ifname)

    for key in req.keys():
        ele = req[key]
        if isinstance(ele, dict):
            for sub_k, sub_v in ele.items():
                mval_k = key + '.' + sub_k
                mval_v = sub_v
        else:
            mval_k = key
            mval_v = req[key]
            
        if mval_k in uci_config.section_map:
            map_val = uci_config.section_map[mval_k]
            map_val[2] = uci_config.convert_config_value(mval_v)
            uci_config.delete_uci_config(map_val[1])

        uci_config.delete_uci_config(map_val[1])
        if map_val[2]:
            #update
            uci_config.set_uci_config(map_val[1], str(map_val[2]))

    uci_config.restart_module()

    iflist_body = _interface_config_make_response(uci_config)
    data = {
            'interface_list': iflist_body,
            'header' : {
                        'resultCode':200,
                        'resultMessage':'Success.',
                        'isSuccessful':'true'
                       }
           }
    return data

'''
GenericIfStats
'''
def get_generic_port_traffic(ifname):
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
            stats = [[ifname, token[1], token[2], token[9], token[10]]]
            break
        else:
            if port_count == 0:
                stats = [[token[0], token[1], token[2], token[9], token[10]]]
            else:
                stats.append([token[0], token[1], token[2], token[9], token[10]])
        port_count = port_count + 1

    fileinput.close()
    return stats, port_count


def generic_ifstats_list():
    stats, port_count = get_generic_port_traffic('')

    for index in range(0, port_count):
        temp = {
                'ifName':stats[index][0],
                'ifIndex':0,
                'rxBytes':stats[index][1],
                'rxPkts':stats[index][2],
                'txBytes':stats[index][3],
                'txPkts':stats[index][4]
        }
        if index == 0:
            ifstats_body = [temp]
        else:
            ifstats_body.append(temp)
        index = index + 1

    data = {
            'traffic-list': ifstats_body,
            'header':{
            'resultCode':200,
            'resultMessage':'Success.',
            'isSuccessful':'true'
            }
    }
    return data


def generic_ifstats_retrieve(ifname):

    if not ifname: return None

    log_info(LOG_MODULE_SAL, "[ifname] : " + ifname)

    stats, port_count = get_generic_port_traffic(ifname)
    if not stats: return None

    ifstats_body = {
            'ifName':stats[0][0],
            'ifIndex':0,
            'rxBytes':stats[0][1],
            'rxPkts':stats[0][2],
            'txBytes':stats[0][3],
            'txPkts':stats[0][4]
    }

    data = {
            'traffic': ifstats_body,
            'header':{
            'resultCode':200,
            'resultMessage':'Success.',
            'isSuccessful':'true'
        }
    }
    return data

