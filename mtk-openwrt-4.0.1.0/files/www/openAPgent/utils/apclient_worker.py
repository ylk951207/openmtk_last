import sys
from common.env import *
from common.misc import *
from common.module_restart import *

PARAMS_DELIMITER=","

init_log("apclient_worker")

command = int(sys.argv[1])
request = dict()
for i in range (2, len(sys.argv)):
    param = sys.argv[i].split(":")
    if param[1] == "True":
        param[1] = True
    elif param[1] == "False":
        param[1] = False
    elif "," in param[1]:
        param[1] = param[1].split(",")

    request[param[0]] = param[1]

log_info(LOG_MODULE_SERVICE, '------ apClient_worker:Input command(%s)------' % (str(command)))

'''
Example:
interface) cd /www/openAPgent; python -m utils/apclient_worker 2 dnsmasq_restart:True iflist:lan,wan config_file:network
system) cd /www/openAPgent; python -m utils/apclient_worker 2 modules:logging,ntp config_file:system
dhcp) cd /www/openAPgent; python -m utils/apclient_worker 2 config_file:dhcp container_name:dnsmasq
wifi) cd /www/openAPgent; python -m utils/apclient_worker 4 devname:MT7615.1 ifname:rai0 enable:True
'''
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
