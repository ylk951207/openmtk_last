from puci import *
from common.env import *
from common.misc import *
from common.message import *


UCI_SYSTEM_CONFIG_FILE = "system"
UCI_SYSTEM_CONFIG_COMMON_CONFIG = "system_config_common"
UCI_SYSTEM_CONFIG_LOGGING_CONFIG = "system_config_logging"

#If ntp is enable, but server doesn't exist, use the default hostname.
NTP_SERVER_DEFAULT_HOSTNAME="2.openwrt.pool.ntp.org"

def system_puci_module_restart(module_restart):
    noti_data = dict()
    noti_data['config_file'] = UCI_SYSTEM_CONFIG_FILE
    noti_data['modules'] = module_restart
    puci_send_message_to_apnotifier(SAL_PUCI_MODULE_RESTART, noti_data)

'''
SystemConfig
'''
def puci_system_config_list():
    system_common_data = dict()
    system_log_data = dict()
    system_ntp_data = dict()

    system_common_data = system_config_uci_get(UCI_SYSTEM_CONFIG_COMMON_CONFIG, system_common_data)
    system_log_data = system_config_uci_get(UCI_SYSTEM_CONFIG_LOGGING_CONFIG, system_log_data)
    system_log_data = convert_get_system_logging_output_cron_data(system_log_data)
    system_ntp_data = system_config_ntp_uci_get(system_ntp_data)

    data = {
        "system" : {
            "common" : system_common_data,
            "logging": system_log_data,
            "ntp": system_ntp_data
        },
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data


def puci_system_config_retrieve(command, add_header):
    system_data = dict()

    log_info(UCI_SYSTEM_CONFIG_FILE, "command = ", command)

    if command == 'common':
        system_data = system_config_uci_get(UCI_SYSTEM_CONFIG_COMMON_CONFIG, system_data)
    elif command == 'logging':
        system_data = system_config_uci_get(UCI_SYSTEM_CONFIG_LOGGING_CONFIG, system_data)
        system_data = convert_get_system_logging_output_cron_data(system_data)
    elif command == 'ntp':
        system_data = system_config_ntp_uci_get(system_data)
    else:
        return response_make_simple_error_body(500, "Not found command", None)

    data = {
        command: system_data,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    log_info(UCI_SYSTEM_CONFIG_FILE, "Response = ", str(data))

    return data


def puci_system_config_create(request):
    return system_config_set(request)


def puci_system_config_update(request):
    return system_config_set(request)


def puci_system_config_detail_create(request, command):
    return system_config_detail_set(request, command)


def puci_system_config_detail_update(request, command):
    return system_config_detail_set(request, command)


def system_config_set(request):
    module_restart = []
    if 'common' in request.keys():
        system_config_uci_set(UCI_SYSTEM_CONFIG_COMMON_CONFIG, request['common'])

    if 'logging' in request.keys():
        log_req = convert_set_system_logging_output_cron_data(request['logging'])
        if 'loggingServerIpAddr' in request['logging'] and request['logging']['loggingServerIpAddr'] :
            request['logging']['internal_logRemote'] = True
        else:
            request['logging']['internal_logRemote'] = False
        system_config_uci_set(UCI_SYSTEM_CONFIG_LOGGING_CONFIG, log_req)
        module_restart.append("logging")
    if 'ntp' in request.keys():
        system_config_ntp_set(request['ntp'])
        module_restart.append("ntp")

    system_puci_module_restart(module_restart)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def system_config_detail_set(request, command):
    module_restart = []
    log_info(UCI_SYSTEM_CONFIG_FILE, "command = ", command)

    if command == 'common':
        system_config_uci_set(UCI_SYSTEM_CONFIG_COMMON_CONFIG, request)
    elif command == 'logging':
        request = convert_set_system_logging_output_cron_data(request)
        if 'loggingServerIpAddr' in request and request['loggingServerIpAddr'] :
            request['internal_logRemote'] = True
        else:
            request['internal_logRemote'] = False
        system_config_uci_set(UCI_SYSTEM_CONFIG_LOGGING_CONFIG, request)
        module_restart.append("logging")
    elif command == 'ntp':
        system_config_ntp_set(request)
        module_restart.append("ntp")
    else:
        return response_make_simple_error_body(500, "Not found command", None)

    system_puci_module_restart(module_restart)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def system_config_uci_get(uci_file, system_data):
    uci_config = ConfigUCI(UCI_SYSTEM_CONFIG_FILE, uci_file)

    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.show_uci_config()

    for map_key, map_val in uci_config.section_map.items():
        if "internal_" in map_key:
            continue
        system_data[map_key] = map_val[2]

    return system_data

def system_config_uci_set(uci_file, req_data):
    system_data = dict()
    uci_config = ConfigUCI(UCI_SYSTEM_CONFIG_FILE, uci_file)

    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.set_uci_config(req_data)

    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]
        if system_data:
            system_data[map_key] = map_val[2]

    return system_data

def system_config_ntp_uci_get (system_data):
    system_data['ntpServerCandidates'] = list()

    for index in range (0, 4):
        cmd_str = "uci show chrony.@server[%d].hostname"  %index
        output, error = subprocess_open(cmd_str)
        if ".hostname=" in output:
            server = output.split("=")[1]
            server = server.strip().strip("'")
            system_data['ntpServerCandidates'].append(server)

    system_data['provideNtpServer'] = False
    if len(system_data['ntpServerCandidates']) > 0:
        system_data['enableNtpClient'] = True
        if NTP_SERVER_DEFAULT_HOSTNAME in system_data['ntpServerCandidates']:
            system_data['ntpServerCandidates'] = []
        else:
            system_data['enableNtpClient'] = False

    return system_data

def system_config_ntp_set(request):
    if request['enableNtpClient'] == True:
        ntp_server_exist = False
        if request['ntpServerCandidates']:
            for server in request['ntpServerCandidates']:
                if  server.strip():
                    ntp_server_exist = True
        if not ntp_server_exist:
           request['ntpServerCandidates'] = [NTP_SERVER_DEFAULT_HOSTNAME]
    else:
        request['ntpServerCandidates'] = []

    for index in range(0, len(request['ntpServerCandidates'])):
        option_str = "chrony.@server[%d].hostname" %index
        server = request['ntpServerCandidates'][index]
        cmd_str = "uci set %s=%s" %(option_str, server)
        output, error = subprocess_open(cmd_str)
        log_info(UCI_SYSTEM_CONFIG_FILE, "cmd_str: %s, output:%s, error:%s" % (cmd_str, output, error))

        if error:
            subprocess_open ("uci add chrony server")

            cmd_str = "uci set %s=%s" % (option_str, server)
            subprocess_open(cmd_str)
            log_info(UCI_SYSTEM_CONFIG_FILE, "cmd_str: %s" %(cmd_str))

            option_str = "chrony.@server[%d].iburst" % index
            cmd_str = "uci set %s=%s" % (option_str, "yes")
            subprocess_open(cmd_str)
            log_info(UCI_SYSTEM_CONFIG_FILE, "cmd_str: %s" %(cmd_str))

    for index in range (len(request['ntpServerCandidates']), 4):
        option_str = "chrony.@server[%d].hostname" % index
        cmd_str = "uci delete %s" % (option_str)
        subprocess_open(cmd_str)
        log_info(UCI_SYSTEM_CONFIG_FILE, "cmd_str: %s" %(cmd_str))

    subprocess_open("uci commit chrony")

def convert_set_system_logging_output_cron_data(log_req):

    if log_req['loggingOutputLevel'] == 'emergency':
        log_req['loggingOutputLevel'] = '1'
    elif log_req['loggingOutputLevel'] == 'alert':
        log_req['loggingOutputLevel'] = '2'
    elif log_req['loggingOutputLevel'] == 'critical':
        log_req['loggingOutputLevel'] = '3'
    elif log_req['loggingOutputLevel'] == 'error':
        log_req['loggingOutputLevel'] = '4'
    elif log_req['loggingOutputLevel'] == 'warning':
        log_req['loggingOutputLevel'] = '5'
    elif log_req['loggingOutputLevel'] == 'notice':
        log_req['loggingOutputLevel'] = '6'
    elif log_req['loggingOutputLevel'] == 'info':
        log_req['loggingOutputLevel'] = '7'
    elif log_req['loggingOutputLevel'] == 'debug':
        log_req['loggingOutputLevel'] = '8'

    if log_req['loggingCronLogLevel'] == 'debug':
        log_req['loggingCronLogLevel'] = '5'
    elif log_req['loggingCronLogLevel'] == 'normal':
        log_req['loggingCronLogLevel'] = '8'
    elif log_req['loggingCronLogLevel'] == 'critical':
        log_req['loggingCronLogLevel'] = '9'

    return log_req

def convert_get_system_logging_output_cron_data(log_req):

    if log_req['loggingOutputLevel'] == '1':
        log_req['loggingOutputLevel'] = 'emergency'
    elif log_req['loggingOutputLevel'] == '2':
        log_req['loggingOutputLevel'] = 'alert'
    elif log_req['loggingOutputLevel'] == '3':
        log_req['loggingOutputLevel'] = 'critical'
    elif log_req['loggingOutputLevel'] == '4':
        log_req['loggingOutputLevel'] = 'error'
    elif log_req['loggingOutputLevel'] == '5':
        log_req['loggingOutputLevel'] = 'warning'
    elif log_req['loggingOutputLevel'] == '6':
        log_req['loggingOutputLevel'] = 'notice'
    elif log_req['loggingOutputLevel'] == '7':
        log_req['loggingOutputLevel'] = 'info'
    elif log_req['loggingOutputLevel'] == '8':
        log_req['loggingOutputLevel'] = 'debug'

    if log_req['loggingCronLogLevel'] == '5':
        log_req['loggingCronLogLevel'] = 'debug'
    elif log_req['loggingCronLogLevel'] == '8':
        log_req['loggingCronLogLevel'] = 'normal'
    elif log_req['loggingCronLogLevel'] == '9':
        log_req['loggingCronLogLevel'] = 'critical'

    return log_req
