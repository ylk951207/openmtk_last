from common.env import *
from common.misc import *
from common.message import *
from common.network import *

LOG_MODULE_PYSYSTEM="python.system"

def provisioning_receive_file_create():
    f = open(PROVISIONING_RECEIVE_FILE, "w")
    f.write("Receive Success")
    f.close()
    log_info(LOG_MODULE_APCLIENT, "** Create %s file **" %PROVISIONING_RECEIVE_FILE)


def py_provisioning_done_create(request):
    provisioning_receive_file_create()

    if not os.path.exists(PROVISIONING_DONE_FILE):
        noti_data = dict()
        server_msg = ApServerLocalMassage(APNOTIFIER_CMD_PORT)
        server_msg.send_message_to_apnotifier(SAL_PROVISIONING_DONE, noti_data)
        log_info(LOG_MODULE_PYSYSTEM, "** Send provisioning done message to apClient **")
    return response_make_simple_success_body(None)

def py_keepalive_check_list():
    if not os.path.exists(PROVISIONING_DONE_FILE):
        return response_make_simple_error_body(500, "Device Not Ready", None)

    return response_make_simple_success_body(None)


def py_system_info_list():
    device_info = DeviceInformation(0)
    device_data = device_info._make_device_info_data()
    time_data = device_info_get_all_time_info()
    data = {
            "device-info" : device_data,
            "time-info" : time_data,
            'header' : {
                    'resultCode':200,
                    'resultMessage':'Success.',
                    'isSuccessful':'true'
            }
    }
    return data

def py_system_time_info_list():
    time_data = device_info_get_all_time_info()

    data = {
        'time-info': time_data,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    log_info(LOG_MODULE_PYSYSTEM, "Response = ", str(data))

    return data


def py_interface_info_list():
    interface_info = HardwareInformation()
    interface_data = interface_info._make_hardware_interface_info_data("all")
    data = {
        "interface-info" : interface_data,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data


def py_interface_info_retrieve(if_type, add_header):
    interface_info = HardwareInformation()
    interface_data = interface_info._make_hardware_interface_info_data(if_type)
    data = {
        if_type: interface_data,
        'header' : {
            'resultCode':200,
            'resultMessage':'Success.',
            'isSuccessful':'true'
        }
    }
    return data

def py_interface_address_info_list():
    iflist_body = []

    ni_addrs = DeviceNetifacesInfo(None)

    for ifname in ni_addrs.iflist:
        dns_data = device_info_get_dns_server(ifname)
        interface_data = {
            "ifname": ifname,
            "ipv4Address": ni_addrs.get_ipv4_addr(ifname),
            "ipv4Netmask": ni_addrs.get_ipv4_netmask(ifname),
            "ipv4Gateway": ni_addrs.get_ipv4_gateway_addr(ifname),
            "ipv4Broadcast": ni_addrs.get_ipv4_broadcast(ifname),
            "dnsServer" : dns_data[ifname],
        }
        iflist_body.append(interface_data)

    data = {
        "v4Addr": iflist_body,
        'header' : {
            'resultCode':200,
            'resultMessage':'Success.',
            'isSuccessful':'true'
        }
    }
    return data

def py_interface_address_info_retrieve(ifname, add_header):
    if not ifname:
        return response_make_simple_error_body(500, "Not found interface name", None)

    log_info(LOG_MODULE_PYSYSTEM, "[ifname] : " + ifname)

    ni_addrs = DeviceNetifacesInfo(None)
    dns_data = device_info_get_dns_server(ifname)

    interface_data = {
        "ifname": ifname,
        "ipv4Address": ni_addrs.get_ipv4_addr(ifname),
        "ipv4Netmask": ni_addrs.get_ipv4_netmask(ifname),
        "ipv4Gateway": ni_addrs.get_ipv4_gateway_addr(ifname),
        "ipv4Broadcast": ni_addrs.get_ipv4_broadcast(ifname),
        "dnsServer": dns_data[ifname],
    }

    data = {
        "v4Addr" : interface_data,
        'header' : {
            'resultCode':200,
            'resultMessage':'Success.',
            'isSuccessful':'true'
        }
    }
    return data


def py_wireless_info_list():
    wireless_data = list()
    wireless_iflist = {
        "2G_default" : "ra0",
        "5G_default" : "rai0"
    }

    for key, value in wireless_iflist.items():
        dict_data = {
            "type" : key,
            "state" : device_get_wireless_state(value)
        }
        wireless_data.append(dict_data)

    data = {
        "wireless-info": wireless_data,
        'header': {
               'resultCode': 200,
               'resultMessage': 'Success.',
               'isSuccessful': 'true'
        }
    }
    return data


def py_system_reboot_create(request):
    delay = int(request['delay'])

    # Default delay for response
    if delay <= 3: delay = 3

    cmd_str = "reboot -d %d" % delay
    subprocess_open_nonblock(cmd_str)
    log_info(LOG_MODULE_PYSYSTEM, "** System Reboot Done **")

    data = {
        'header': {
               'resultCode': 200,
               'resultMessage': 'Success.',
               'isSuccessful': 'true'
        }
    }
    return data

