import sys
from common.env import *
from common.misc import *
from common.module_restart import *

PARAMS_DELIMITER=","

command = int(sys.argv[1])
params = sys.argv[2]

init_log("apclient_worker")

log_info(LOG_MODULE_SERVICE, '------ apClient_worker:Input command(%s), params(%s) ------' % (str(command), params))


request = dict()
params = params.split(PARAMS_DELIMITER)

for value in params:
    value = value.split(":")
    if value[1] == "True":
        value[1] = True
    elif value[1] == "False":
        value[1] = False
    elif "/" in value[1]:
        value[1] = value[1].split("/")

    request[value[0]] = value[1]

log_info(LOG_MODULE_SERVICE, "Request ARGS: " + str(request))

if command == SAL_WIFI_MODULE_RESTART:
    wmr = WifiModuleRestart(request)
    wmr._wifi_module_restart_proc()
elif command == SAL_PUCI_MODULE_RESTART:
    if 'iflist' in request.keys():
        if request['iflist'] == "all":
            request['iflist'] = ['lan', 'wan']
        else:
            request['iflist'] = [request['iflist']]

    pmr = PuciModuleRestart(request)
    pmr.puci_module_restart()

log_info(LOG_MODULE_SERVICE, "------ apClient_worker: End ---------")
