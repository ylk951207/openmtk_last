import libsrc._sys_usage as ls

from common.env import *
from common.misc import *
from common.message import *

SYSTEM_USAGE_CPU = "cpu_usage"
SYSTEM_USAGE_MEMORY = "memory_usage"


"""
SystemUsage
"""
def swigc_system_usage_list():

    system_cpu_usage = system_usage_get(SYSTEM_USAGE_CPU)
    system_memory_usage = system_usage_get(SYSTEM_USAGE_MEMORY)

    data = {
        "usages": {
            "cpu": system_cpu_usage,
            "memory": system_memory_usage,
        },
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def swigc_system_usage_retrieve(command, add_header):

    log_info(LOG_MODULE_SAL, "command = ", command)

    if command == 'cpu':
        system_usage = system_usage_get(SYSTEM_USAGE_CPU)
    elif command == 'memory':
        system_usage = system_usage_get(SYSTEM_USAGE_MEMORY)
    else:
        raise RespNotFound("Command")

    data = {
        command: system_usage,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    log_info(LOG_MODULE_SAL, "Response = ", str(data))

    return data

def system_usage_get(command):

    if command == 'cpu_usage':
        cpu_field = {
            'cpuCurrent' : ls.sys_usage_get_cpu_usage(),
        }
        return cpu_field

    if command == 'memory_usage':
        memory_field = {
            'memoryTotal'  : ls.sys_usage_get_memory_total(),
            'memoryUsed'   : ls.sys_usage_get_memory_used(),
            'memoryFree'   : ls.sys_usage_get_memory_free(),
        }
        return memory_field
