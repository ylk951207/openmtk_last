import fileinput

from puci import *

from common.log import *
from common.env import *

UCI_SYSTEM_CONFIG="systemConfigLogging"


# TODO: fill values 
def _system_config_make_response(uci_config):
    temp = dict()
    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]
        temp[map_key] = map_val[2]
#    for i in range (0, len(config.section_map)):  
#        temp[config.section_map[i][0]] = config.section_map[i][2]
#        i += 1

    data = {
            'system': temp,
            'header':{
            'resultCode':200,
            'resultMessage':'Success.',
            'isSuccessful':'true'
            }
        }
    log_info(LOG_MODULE_SAL, "Response = ", str(data))
    return data


'''
SystemConfig
'''
def system_config_list():
    uci_config = ConfigUCI(UCI_SYSTEM_CONFIG)

    uci_config.show_uci_config(None)
    
    data = _system_config_make_response(uci_config)
    return data

def system_config_create(req):
    uci_config = ConfigUCI(UCI_SYSTEM_CONFIG)
    
    log_info(LOG_MODULE_SAL, "request data = ", req)
    
    for map_key in req.keys():
        if map_key in uci_config.section_map:
            map_val = uci_config.section_map[map_key]
            map_val[2] = uci_config.convert_config_value(req[map_key])

    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]
        if map_val[2]:
            if map_val[0] == CONFIG_TYPE_SCALAR:
                uci_config.set_uci_config(map_val[1], str(map_val[2]))
            else:
                uci_config.delete_uci_config(map_val[1])
                uci_config.set_uci_config_list_value(req, map_val[1], map_val[2])
                
    uci_config.restart_module()
    
    data = _system_config_make_response(uci_config)
    return data

def system_config_update(req):
    uci_config = ConfigUCI(UCI_SYSTEM_CONFIG)
    
    for map_key in req.keys():
        map_val = uci_config.section_map[map_key]
        if map_key in uci_config.section_map:
            map_val[2] = uci_config.convert_config_value(req[map_key])
            uci_config.delete_uci_config(map_val[1])

        uci_config.delete_uci_config(map_val[1])
        if map_val[2]:
            #update
            uci_config.set_uci_config(map_val[1], str(map_val[2]))
    
    data = _system_config_make_response(uci_config)
    return data
    
