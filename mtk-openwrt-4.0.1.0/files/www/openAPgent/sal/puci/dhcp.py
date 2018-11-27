import socket
import struct
import time

from puci import *
from common.env import *
from common.misc import *
from common.network import *
from common.message import *

MAX_RETRY_COUNT = 3


def dhcp_puci_module_restart():
    noti_data = dict()
    noti_data['config_file'] = UCI_DHCP_CONFIG_FILE
    noti_data['container_name'] = "dnsmasq"
    puci_send_message_to_apnotifier(SAL_PUCI_MODULE_RESTART, noti_data)

'''
DHCP Common Config
'''
def puci_dhcp_common_config_list():
    dhcp_common_data = dict()
    dhcp_common_data = dhcp_config_common_uci_get(UCI_DHCP_COMMON_CONFIG, dhcp_common_data)
    data = {
        "dhcp-dns": dhcp_common_data,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def puci_dhcp_common_config_create(request):
    return dhcp_common_config_set(request)

def puci_dhcp_common_config_update(request):
    return dhcp_common_config_set(request)

def dhcp_common_config_set(request):
    dhcp_common_config_uci_set(request, UCI_DHCP_COMMON_CONFIG)

    dhcp_puci_module_restart()

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def dhcp_config_common_uci_get(uci_file, dhcp_data):
    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, uci_file)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.show_uci_config()

    for map_key, map_val in uci_config.section_map.items():
        dhcp_data[map_key] = map_val[2]

    return dhcp_data

def dhcp_common_config_uci_set(req_data, uci_file):
    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, uci_file)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.set_uci_config(req_data)


'''
DHCP Pool
'''
def puci_dhcp_pool_config_list():
    iflist = ['lan', 'wan']

    for i in range(0, len(iflist)):
        log_info(UCI_DHCP_CONFIG_FILE, "[ifname] : " + iflist[i])
        rc = puci_dhcp_pool_config_retrieve(iflist[i], 0)
        if i == 0:
            iflist_body = [rc]
        else:
            iflist_body.append(rc)

    data = {
        "dhcp-pool": iflist_body,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data


def puci_dhcp_pool_config_retrieve(ifname, add_header):
    if not ifname:
        return response_make_simple_error_body(500, "Not found interface name", None)

    log_info(UCI_DHCP_CONFIG_FILE, "[ifname] : " + ifname)

    dhcp_data = dict()

    dhcp_data = dhcp_pool_config_uci_get(ifname, dhcp_data)
    dhcp_data = dhcp_pool_v6pool_config_uci_get(ifname, dhcp_data)

    addr_data = device_get_lan_ipaddr_netmask()
    start = dhcp_data['addrStartAddr']
    limit = dhcp_data['addrEndAddr']
    ip_addr = addr_data['ipv4_addr']

    if dhcp_data['v4Netmask'] != ' ':
        netmask = dhcp_data['v4Netmask']
    else:
        netmask = addr_data['ipv4_netmask']

    pool_config = GetDhcpPoolData()
    if start !=" "  and limit !=" ":
        start_addr, end_addr = pool_config.get_start_end_address_by_start_limit(start, limit, ip_addr, netmask)

        if start_addr == None or end_addr == None:
            return response_make_simple_error_body(500, "Not found UCI config start limit", None)

        dhcp_data['addrStartAddr'] = start_addr
        dhcp_data['addrEndAddr'] = end_addr

    if add_header == 1:
        data = {
            'dhcp-pool': dhcp_data,
            'header': {
                'resultCode': 200,
                'resultMessage': 'Success.',
                'isSuccessful': 'true'
            }
        }
    else:
        data = dhcp_data
    return data

def puci_dhcp_pool_config_create(request):
    return dhcp_pool_config_set(request)

def puci_dhcp_pool_config_update(request):
    return dhcp_pool_config_set(request)

def puci_dhcp_pool_config_detail_create(request, ifname):
    return dhcp_pool_config_detail_set(request, ifname)

def puci_dhcp_pool_config_detail_update(request, ifname):
    return dhcp_pool_config_detail_set(request, ifname)

def dhcp_pool_config_set(request):
    dhcp_list = request['dhcp-pool']

    while len(dhcp_list) > 0:
        ifdata = dhcp_list.pop(0)

        ifname = ifdata['ifname']

        error_data = dhcp_pool_config_uci_set(ifdata, ifname)
        if UCI_DHCP_V6POOL_STR in ifdata:
            dhcp_pool_v6pool_config_uci_set(ifdata[UCI_DHCP_V6POOL_STR], ifname)

    if error_data:
        return error_data

    dhcp_puci_module_restart()

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def dhcp_pool_config_detail_set(request, ifname):
    if not ifname:
        return response_make_simple_error_body(500, "Not found interface name", None)

    error_data = dhcp_pool_config_uci_set(request, ifname)
    if UCI_DHCP_V6POOL_STR in request:
        dhcp_pool_v6pool_config_uci_set(request[UCI_DHCP_V6POOL_STR], ifname)

    if error_data:
        return error_data
    
    dhcp_puci_module_restart()

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def dhcp_pool_config_uci_get(ifname, dhcp_data):
    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_INTERFACE_POOL_CONFIG, ifname)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.show_uci_config()

    dhcp_data['ifname'] = ifname
    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]
        dhcp_data[map_key] = map_val[2]

    return dhcp_data

def dhcp_pool_config_uci_set(req_data, ifname):
    if not ifname:
        return response_make_simple_error_body(500, "Not found interface name", None)

    log_info(UCI_DHCP_CONFIG_FILE, 'dhcp_pool_req = ' + str(req_data))

    addr_data = device_get_lan_ipaddr_netmask()
    log_info(UCI_DHCP_CONFIG_FILE, 'addr_data = ' + str(addr_data))
    '''
    When addr_data is None, it tries to fetch addr_data again.
    '''
    for i in range(MAX_RETRY_COUNT):
        if addr_data['ipv4_addr'] == None or addr_data['ipv4_netmask'] == None:
            addr_data = device_get_lan_ipaddr_netmask()
            log_info(UCI_DHCP_CONFIG_FILE, 'addr_data = ' + str(addr_data) + ' ' + str(i) + 'rd Retry')

    br_addr = addr_data['ipv4_addr']

    start_addr = req_data['addrStartAddr']
    end_addr = req_data['addrEndAddr']
    if req_data['v4Netmask'] != " " and req_data['v4Netmask']:
        netmask = req_data['v4Netmask']
    else:
        netmask = addr_data['ipv4_netmask']

    pool_config = GetDhcpPoolData()
    if start_addr != " " and end_addr != " ":
        req_data['addrStartAddr'], req_data['addrEndAddr'] = \
            pool_config.get_start_limit_by_start_end_addr(start_addr, end_addr, br_addr, netmask)

    if req_data['addrStartAddr'] == None or req_data['addrEndAddr'] == None:
        return response_make_simple_error_body(500, "Invalid Start End Addr Value", None)

    log_info(UCI_DHCP_CONFIG_FILE, 'dhcp_pool_set_req = ' + str(req_data))
    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_INTERFACE_POOL_CONFIG, ifname)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    if not req_data['dhcpOptions']:
        del req_data['dhcpOptions']

    uci_config.set_uci_config(req_data)

def dhcp_pool_v6pool_config_uci_get(ifname, dhcp_data):
    pool_data = dict()

    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_INTERFACE_V6POOL_CONFIG, ifname)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.show_uci_config()

    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]
        pool_data[map_key] = map_val[2]

    dhcp_data[UCI_DHCP_V6POOL_STR] = pool_data

    log_info(UCI_DHCP_CONFIG_FILE, dhcp_data)

    return dhcp_data

def dhcp_pool_v6pool_config_uci_set(req_data, ifname):
    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_INTERFACE_V6POOL_CONFIG, ifname)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.set_uci_config(req_data)


'''
DHCP_Static_leases
'''
def puci_dhcp_static_leases_config_list():
    sl_body = list()
    host_info_list = dhcp_static_leases_config_get_info(None)

    for host_key, host_name in host_info_list.items():
        sl_data = dhcp_static_leases_config_uci_get(host_key)
        sl_body.append(sl_data)

    data = {
        "static-lease-list": sl_body,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data


def puci_dhcp_static_leases_config_retrieve(name, add_header):
    host_info_list = dhcp_static_leases_config_get_info(name)
    log_info(UCI_DHCP_CONFIG_FILE, "host_info data = " + str(host_info_list))

    for host_key, host_name in host_info_list.items():
        if host_name == name:
            sl_data = dhcp_static_leases_config_uci_get(host_key)

    data = {
        'static-lease': sl_data,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def puci_dhcp_static_leases_config_create(request):
    return dhcp_static_leases_config_set(request)

def puci_dhcp_static_leases_config_update(request):
    return dhcp_static_leases_config_set(request)


def puci_dhcp_static_leases_config_detail_create(request, name):
    return dhcp_static_leases_config_detail_set(request, name)


def puci_dhcp_static_leases_config_detail_update(request, name):
    return dhcp_static_leases_config_detail_set(request, name)


def puci_dhcp_static_leases_config_destroy(request):

    static_leases_list = request['static-lease-list']
    for sl_data in static_leases_list:
        host_info_list = dhcp_static_leases_config_get_info(sl_data['name'])
        log_info(UCI_DHCP_CONFIG_FILE, 'host info list = ' + str(host_info_list))

        for host_key, host_name in host_info_list.items():
            dhcp_static_leases_config_uci_destroy(host_key)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def puci_dhcp_static_leases_config_detail_destroy(request, name):
    host_info_list = dhcp_static_leases_config_get_info(name)

    for host_key, host_name in host_info_list.items():
        if host_name == name:
            dhcp_static_leases_config_uci_destroy(host_key)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def dhcp_static_leases_config_set(request):
    sl_list = request['static-lease-list']

    host_info_list = dhcp_static_leases_config_get_info(None)

    while len(sl_list) > 0:
        sl_data = sl_list.pop(0)
        found = False

        for host_key, host_name in host_info_list.items():
            if host_name == sl_data['name']:
                dhcp_static_leases_config_uci_set(sl_data, host_key)
                found = True

        if found == False:
            host_info_list = dhcp_static_leases_config_uci_add(' host', sl_data['name'])

            for host_key, host_name in host_info_list.items():
                dhcp_static_leases_config_uci_set(sl_data, host_key)

    dhcp_puci_module_restart()

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def dhcp_static_leases_config_detail_set(request, name):
    host_info_list = dhcp_static_leases_config_get_info(name)

    if len(host_info_list) <= 0:
        host_info_list = dhcp_static_leases_config_uci_add(' host', name)

    for host_key, host_name in host_info_list.items():
        if host_name == name:
            dhcp_static_leases_config_uci_set(request, host_key)

    dhcp_puci_module_restart()

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data


def dhcp_static_leases_config_uci_get(host_info):
    sl_data = dict()
    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_STATIC_LEASE_CONFIG, host_info)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.show_uci_config()

    for map_key in uci_config.section_map.keys():
        map_val = uci_config.section_map[map_key]
        sl_data[map_key] = map_val[2]

    return sl_data

def dhcp_static_leases_config_uci_add(host_str, name):
    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_STATIC_LEASE_CONFIG, None)

    uci_config.add_uci_config(host_str)

    output, error = subprocess_open(UCI_SHOW_CMD + UCI_DHCP_CONFIG_FILE + "| tail -1")

    host_info = dict()
    host_line = output.splitlines()[0]
    host_key = host_line.split('.')[1].split('=')[0]
    host_name = name
    host_info[host_key] = host_name
    return host_info


def dhcp_static_leases_config_uci_set(req_data, host_key):
    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_STATIC_LEASE_CONFIG, host_key)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.set_uci_config(req_data)

def dhcp_static_leases_config_uci_destroy(host_key):

    uci_config = ConfigUCI(UCI_DHCP_CONFIG_FILE, UCI_DHCP_STATIC_LEASE_CONFIG, host_key)
    if uci_config.section_map == None:
        return response_make_simple_error_body(500, "Not found UCI config", None)

    uci_config.delete_uci_config('dhcp.' + host_key)


def dhcp_static_leases_config_get_info(name):
    '''
    Extract host number from 'host' section config
    '''
    host_info = dict()
    awk_cmd = " | awk '{result=substr($1,6,1000); print result}'"
    if name:
        name_str = "\"name='" + name + "'\""
        filter_cmd = " | grep '@host'" + " | grep " + name_str + awk_cmd
    else:
        filter_cmd = " | grep '@host'" + " | grep name" + awk_cmd

    output, error = subprocess_open(UCI_SHOW_CMD + UCI_DHCP_CONFIG_FILE + filter_cmd)
    if error:
        return host_info

    if output :
        host_line = output.splitlines()
        for token in host_line:
            host_key = token.split('.')[0]
            host_name = token.split('=')[1].strip("'")
            host_info[host_key] = host_name

        return host_info

    else:
        return host_info

class GetDhcpPoolData:
    '''
    Process data needed for DHCP Pool
    '''
    def get_start_limit_by_start_end_addr(self, start_addr, end_addr, addr, netmask):
        '''
        GET the start number and the number of the IP to lease by the start address and the end address.
        ex) start_addr = xxx.xxx.xxx.100, end_addr = xxx.xxx.xxx.249 --> start = 100, limit = 150
        '''
        min_addr, max_addr = self.get_max_min_address(addr, netmask)
        if min_addr == None or max_addr == None:
            log_error(UCI_DHCP_CONFIG_FILE, "get_max_min_addr_error")
            return None, None

        int_min_addr = self.ip2int(min_addr)
        int_max_addr = self.ip2int(max_addr)
        if self.check_valid_ipv4_address(start_addr) and self.check_valid_ipv4_address(end_addr):
            int_start_addr = self.ip2int(start_addr)
            int_end_addr = self.ip2int(end_addr)
        else:
            int_start_addr = None
            int_end_addr = None

        if int_start_addr == None or int_end_addr == None:
            log_error(UCI_DHCP_CONFIG_FILE, "Invalid_addr_type")
            return None, None

        if int_min_addr < int_start_addr and int_end_addr < int_max_addr and int_start_addr <= int_end_addr:
            limit = self.ip2int(end_addr) - self.ip2int(start_addr) + 1
            start = self.ip2int(start_addr) - self.ip2int(min_addr)
            log_info(UCI_DHCP_CONFIG_FILE,"start_data = " + str(start) + ", " + "limit_data = " + str(limit))
            return start, limit
        else:
            return None, None

    def get_start_end_address_by_start_limit(self, start, limit, addr, netmask):
        '''
        GET start address and end address to lease through DHCP with starting number and IP number to lease.
        ex) start = 100, limit = 150 --> start_addr = xxx.xxx.xxx.100, end_addr = xxx.xxx.xxx.249
        '''
        min_addr, max_addr = self.get_max_min_address(addr, netmask)
        if min_addr == None or max_addr == None:
            log_error(UCI_DHCP_CONFIG_FILE, "get_max_min_addr_error")
            return None, None

        start = int(start)
        limit = int(limit)
        int_addr = self.ip2int(min_addr)
        int_start_addr = int_addr + start
        start_addr = self.int2ip(int_start_addr)

        int_end_addr = int_start_addr + limit - 1
        limit_addr = self.int2ip(int_end_addr)

        return start_addr, limit_addr


    def get_max_min_address(self, ip_addr, netmask):
        '''
        Gets the largest, smallest IP address given a given IP and subnet mask.
        '''
        if ip_addr != None and netmask != None and ip_addr != ' ' and netmask != ' ':
            if self.check_valid_ipv4_address(ip_addr) and self.check_valid_ipv4_address(netmask):
                int_min = self.ip2int(netmask) & self.ip2int(ip_addr)
                min_addr = self.int2ip(int_min)

                wild_addr = self.get_wildcard_address(netmask)
                int_max = int_min | self.ip2int(wild_addr)
                max_addr = self.int2ip(int_max)

                return min_addr, max_addr
            else:
                log_error(UCI_DHCP_CONFIG_FILE,
                         "Invalid_ip_type = " + str(ip_addr) + ", " +
                         "Invalid_netmask_type = " + str(netmask))
                return None, None

        else:
            log_error(UCI_DHCP_CONFIG_FILE,
                      "None_addr = " + str(ip_addr) + ", " +
                      "None_netmask = "+ str(netmask))
            return None, None

    def get_wildcard_address(self, netmask):
        '''
        Get wildcard address
        ex) 255.255.0.0   --> 0.0.255.255
        	255.255.192.0 --> 0.0.63.255
        '''
        sub_int = self.ip2int(netmask)
        sub = bin(sub_int).replace('0b', '')
        wild_addr = self.int2ip(int(self.reverse_binary_data(sub), 2))

        return wild_addr

    def reverse_binary_data(self, bin_data):
        '''
        Reverse binary data ex)1100101 --> 0011010
        '''
        token = []
        for i in range(0, len(bin_data)):
            token.append(str(1 - int(bin_data[i])))
        token = ''.join(token)

        return token

    def ip2int(self, addr):
        '''
        Compute IP to integer
        '''
        return struct.unpack("!I", socket.inet_aton(addr))[0]

    def int2ip(self, addr):
        '''
        Compute integer to IP
        '''
        return socket.inet_ntoa(struct.pack("!I", addr))

    def check_valid_ipv4_address(self, addr):
        '''
        Check that the ip address is valid.
        '''
        log_info(UCI_DHCP_CONFIG_FILE,"addr = " + str(addr) + " vaild check")
        try:
            socket.inet_pton(socket.AF_INET, addr)
        except AttributeError:
            try:
                socket.inet_aton(addr)
            except socket.error:
                return False
            return addr.count('.') == 3
        except socket.error:
            return False

        return True


def py_dhcp_leases_list():
    dhcp_lease_list = list()

    if os.path.exists(DHCP_LEASE_FILE):
        with open(DHCP_LEASE_FILE, "r") as rfile:
            lines = rfile.readlines()
            for line in lines:
                if line.strip() == '':
                    continue
                line = line.split()
                expiry_time = int(line[0])
                '''
                Calculate the time the device was created and the current local time
                '''
                expiry_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(expiry_time))
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')
                total_time = (datetime.datetime.strptime(expiry_time,'%Y-%m-%d %H:%M:%S')
                              - datetime.datetime.strptime(current_time,'%Y-%m-%d %H:%M:%S'))
                '''
                ex) total_time = '1 day, 12:50:03'
                '''
                token = str(total_time).split(',')
                if len(token) == 2:
                    d_data = token[0].split(' ')[0]
                    hms_data = token[1].strip().split(':')
                    expiry_time = d_data + "d " + hms_data[0] + "h " + hms_data[1] + "m " + hms_data[2] + "s"

                elif len(token) == 1:
                    hms_data = token[0].strip().split(':')
                    expiry_time = hms_data[0] + "h " + hms_data[1] + "m " + hms_data[2] + "s"

                dhcp_lease_data = {
                    'hostname' : line[3],
                    'v4Addr' : line[2],
                    'macAddr' : line[1],
                    'leaseExpiryTime' : expiry_time
                }
                dhcp_lease_list.append(dhcp_lease_data)

    data = {
        'dhcp-leases' : dhcp_lease_list,
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

