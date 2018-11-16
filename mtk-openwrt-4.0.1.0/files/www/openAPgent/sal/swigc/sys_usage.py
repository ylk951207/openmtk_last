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

    system_cpu_usage = {'cpuCurrent': get_cpu_usage_from_top()}
    system_memory_usage = system_usage_get(SYSTEM_USAGE_MEMORY)
    if system_cpu_usage['cpuCurrent'] == None or system_memory_usage == None:
        return response_make_simple_error_body(500, "Failed to open /proc ", None)

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
        system_usage = {'cpuCurrent': get_cpu_usage_from_top()}
    elif command == 'memory':
        system_usage = system_usage_get(SYSTEM_USAGE_MEMORY)
    else:
        return response_make_simple_error_body(500, "Not found command", None)

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

def get_cpu_usage_from_top():
    top_data, error = subprocess_open('top -b -n 1 | grep CPU')
    if error:
        return None
    top_data = top_data.split('\n')
    cpu_line = None
    for i in range(len(top_data)):
        if 'CPU:' and 'usr' and 'sys' in top_data[i]:
            cpu_line = top_data[i]

    if not cpu_line:
        return None

    usr_data = int(cpu_line.split('usr')[0].split(':')[1].strip().replace('%', ''))
    sys_data = int(cpu_line.split('sys')[0].split('usr')[1].strip().replace('%', ''))

    cpu_data = usr_data + sys_data

    return cpu_data