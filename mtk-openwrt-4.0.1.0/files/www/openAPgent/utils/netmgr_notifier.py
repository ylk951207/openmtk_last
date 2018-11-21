import sys
from common.env import *
from common.misc import *
from common.message import *
from common.sysinfo import *

LOG_MODULE_NETMGR = "netmgr"

def send_ip_address_change_notification(ifname):
    noti_req = APgentSendNotification()

    if ifname == 'eth0' or ifname == 'br-lan':
        noti_req.response['ifname'] = 'lan'
    elif ifname == 'eth1':
        noti_req.response['ifname'] = 'wan'
    else:
        return

    iflist = [ifname]
    ni_addrs = DeviceNetifacesInfo(iflist)

    noti_req.response['ipv4Address'] = ni_addrs.get_ipv4_addr(ifname)
    noti_req.response['ipv4Netmask'] = ni_addrs.get_ipv4_netmask(ifname)

    device_identify = dict()
    device_identify['serialNumber'] = device_info_get_serial_num()
    noti_req.response['deviceIdentity'] = device_identify


    dns_data = device_info_get_dns_server(ifname)
    noti_req.response['dnsServer'] = dns_data[ifname]

    noti_req.send_notification(CAPC_NOTIFICATION_ADDRESS_CHANGE_URL)
    return


init_log("Netmgr_notifier")

ifname = sys.argv[1]

log_info (LOG_MODULE_NETMGR, '-------- netMgrd: Start netmgr python module (ifname %s) -------'%ifname)

send_ip_address_change_notification (ifname)

'''
Update dns server
'''
device_update_lan_dns_server()

log_info (LOG_MODULE_NETMGR, '--------- netMgrd: End  --------')

