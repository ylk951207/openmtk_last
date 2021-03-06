import datetime
import time
import os
import netifaces as ni
import socket, json
from random import *

import libs._network as ln

from common.env import *
from common.misc import *
from common.module_restart import *
from config.ap_device_config import *



LOG_MODULE_SYSINFO="common.network"

'''
From left to right near wan port
'''
PORT_WAN_IDX = 0
PORT_LAN_1_IDX = 1
PORT_LAN_2_IDX = 2
PORT_LAN_3_IDX = 3
PORT_LAN_4_IDX = 4

lan_port_idx_list = [PORT_LAN_1_IDX, PORT_LAN_2_IDX, PORT_LAN_3_IDX, PORT_LAN_4_IDX]

port_map = {
	PORT_LAN_1_IDX: "LAN 1",
	PORT_LAN_2_IDX: "LAN 2",
	PORT_LAN_3_IDX: "LAN 3",
	PORT_LAN_4_IDX: "LAN 4",
	PORT_WAN_IDX: "WAN",
}

'''
Netifaces class
'''
class DeviceNetifacesInfo(object):
	def __init__(self, def_iflist):
		if not def_iflist:
			self.iflist = ni.interfaces()
		else:
			self.iflist = def_iflist

		self.addresses = dict()

		for interface in self.iflist:
			self.addresses[interface] = dict()
			try:
				self.addresses[interface]['addrs'] = ni.ifaddresses(interface)
			except Exception as e:
				log_error(LOG_MODULE_REQUEST, "*** ni.ifaddresses() error: %s for %s" %(str(e), interface))
				continue

		ni_gateways = ni.gateways()
		self.ipv4_gateways = []
		if 'default' in ni_gateways.keys():
			for family in ni_gateways['default'].keys():
				if family == ni.AF_INET:
					self.ipv4_gateways.append(ni_gateways['default'][ni.AF_INET])

	def get_interface_addresses(self, ifname):
		if not ifname in self.addresses.keys():
			return {}
		if 'addrs' in self.addresses[ifname].keys():
			return self.addresses[ifname]['addrs']
		else:
			return {}

	def get_hwaddr(self, ifname):
		ni_addrs = self.get_interface_addresses(ifname)
		if ni.AF_PACKET in ni_addrs.keys():
			if 'addr' in ni_addrs[ni.AF_PACKET][0].keys():
				return ni_addrs[ni.AF_PACKET][0]['addr']
			else:
				return ""
	def get_ipv4_addr(self, ifname):
		ni_addrs = self.get_interface_addresses(ifname)
		if ni.AF_INET in ni_addrs.keys():
			if 'addr' in ni_addrs[ni.AF_INET][0].keys():
				return ni_addrs[ni.AF_INET][0]['addr']
			else:
				return ""

	def get_ipv4_netmask(self, ifname):
		ni_addrs = self.get_interface_addresses(ifname)
		if ni.AF_INET in ni_addrs.keys():
			if 'netmask' in ni_addrs[ni.AF_INET][0].keys():
				return ni_addrs[ni.AF_INET][0]['netmask']
			else:
				return ""

	def get_ipv4_broadcast(self, ifname):
		ni_addrs = self.get_interface_addresses(ifname)
		if ni.AF_INET in ni_addrs.keys():
			if 'broadcast' in ni_addrs[ni.AF_INET][0].keys():
				return ni_addrs[ni.AF_INET][0]['broadcast']
			else:
				return ""

	@property
	def wan_hwaddr(self):
		return self.get_hwaddr(WAN_ETHDEV)

	@property
	def wan_ipv4_addr(self):
		return self.get_ipv4_addr(WAN_ETHDEV)

	@property
	def wan_ipv4_netmask(self):
		return self.get_ipv4_netmask(WAN_ETHDEV)

	@property
	def wan_ipv4_broadcast(self):
		return self.get_ipv4_broadcast(WAN_ETHDEV)

	def get_ipv4_gateway_addr(self, ifname):
		for gw in self.ipv4_gateways:
			if len(gw) < 2:
				continue

			if gw[1] == ifname:
				return gw[0]
		return ""


def device_get_lan_ipaddr_netmask():
	iflist = ['eth0', 'br-lan']
	ni_addrs = DeviceNetifacesInfo(iflist)
	isBridge, bridgeList = device_get_if_bridge_mode()
	if isBridge == True:
		ifname = 'br-lan'
	else:
		ifname = 'eth0'

	addr_data = dict()
	addr_data['ifname'] = ifname
	addr_data['ipv4_addr'] = ni_addrs.get_ipv4_addr(ifname)
	addr_data['ipv4_netmask'] = ni_addrs.get_ipv4_netmask(ifname)
	return addr_data

'''
Device Information class
'''
class DeviceInformation(object):
	def __init__(self, device_id):
		'''
		TODO: Device ID
		'''
		self.device_id = device_id
		self.name = socket.gethostname()
		self.ip_addr = device_info_get_ip_address(WAN_ETHDEV)
		self.mac_addr = device_info_get_hwaddr(WAN_ETHDEV)
		self.serial_num = device_info_get_serial_num()
		self.counterfeit = 0

		self.vendor_id = AP_VENDOR_ID
		self.vendor_name = AP_VENDOR_NAME
		self.device_type = AP_DEVICE_TYPE
		self.model_num = AP_MODEL_NUMBER
		self.user_id = AP_USER_ID
		self.user_passwd = AP_USER_PASSWD
		self.status = AP_STATUS
		self.map_x = AP_MAP_X
		self.map_y = AP_MAP_Y
		self.capabilities = AP_CAPABILITIES

	def update_device_info(self):
		self.name = socket.gethostname()
		self.ip_addr = device_info_get_ip_address(WAN_ETHDEV)
		self.mac_addr = device_info_get_hwaddr(WAN_ETHDEV)
		self.serial_num = device_info_get_serial_num()

	def _make_device_info_data(self):
		self.data = {
	                "id": self.device_id,
	                "name": self.name,
	                "vendorId": self.vendor_id,
	                "vendorName": self.vendor_name,
	                "serialNumber": self.serial_num,
	                "type": self.device_type,
	                "model": self.model_num,
	                "ip": self.ip_addr,
	                "mac": self.mac_addr,
	                "userId": self.user_id,
	                "userPasswd": self.user_passwd,
	                "status": self.status,
	                "mapX": self.map_x,
	                "mapY": self.map_y,
	                "counterfeit": self.counterfeit,
	                "uptime" : device_info_get_uptime(),
	                "capabilities" : self.capabilities
                 }

		log_info(LOG_MODULE_SYSINFO,  "<Make Response Message>")
		log_info(LOG_MODULE_SYSINFO, json.dumps(self.data, indent=2))

		return self.data


def device_info_get_ip_address(ifname):
	ni_addrs = DeviceNetifacesInfo(None)
	return ni_addrs.get_ipv4_addr(ifname)

def device_info_get_hwaddr(ifname):
	ni_addrs = DeviceNetifacesInfo(None)
	return ni_addrs.get_hwaddr(ifname)

def device_info_get_serial_num():
	mac_addr = device_info_get_hwaddr(WAN_ETHDEV)
	if mac_addr:
		token = mac_addr.split(':')
		return "AP_SR_NO7777_"+ token[3] + token[4] + token[5]
	else:
		return "AF_SR_NO777_unknown"

def device_info_get_uptime():
	with open('/proc/uptime', 'r') as f:
		uptime_seconds = float(f.readline().split()[0].split('.')[0])
		uptime_seconds = str(datetime.timedelta(seconds=uptime_seconds))
		return uptime_seconds

def device_info_get_localtime():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def device_info_get_timezone():
	return time.tzname[time.daylight]

def device_info_get_all_time_info():
	data = {
		"uptime" : device_info_get_uptime(),
		"localtime" : str(device_info_get_localtime()).replace('T',' '),
		"timezone" : device_info_get_timezone()
	}
	return data

def device_info_get_ifname_by_port_name(port_name):
	iflist = ['lo', 'lan', 'wan', 'wan6']

	for ifname in iflist:
		compare_str = 'network.%s.ifname' % ifname
		cmd_str = "uci show network.%s.ifname" % ifname

		output, error = subprocess_open(cmd_str)
		if compare_str in output:
			output = output.split("=")[1]
			output = output.strip("\n")
			output = output.strip("'")
			if output == port_name:
				log_debug(LOG_MODULE_SYSINFO, "port name %s output %s" % (port_name, output))
				return ifname

	return None


def device_info_get_dns_server(ifname):
	dhcp_resolv_config_list = [DHCP_RESOLV_AUTO_CONFIG_FILE]
	dns_data = dict()
	append_dns = False

	iftype_list = ['lan', 'wan']

	for iftype in iftype_list:
		dns_list = list()

		compare_str = "# Interface %s" %iftype

		for config_file in dhcp_resolv_config_list:
			if not os.path.exists(config_file): continue

			with open(config_file, 'r') as rfile:
				lines = rfile.readlines()
				for line in lines:
					if append_dns == True and line[0] == '#':
						append_dns = False
						continue

					if compare_str in line:
						append_dns = True
						continue

					if append_dns == True:
						line = line.split()
						if line in dns_list:
							continue
						dns_list.append(line[1])

					#dns_list = list(set(dns_list))
					if len(dns_list) >= 2:
						break

		# wanDnsServer, lanDnsServer
		key_str = iftype + "DnsServer"
		dns_data[key_str] = dns_list
		log_debug(LOG_MODULE_SYSINFO, "Interface %s dns server : %s" % (iftype, str(dns_list)))

	# To return specific interface's dns server
	if ifname:
		if ifname == 'eth0' or ifname == 'br-lan':
			dns_data[ifname] = dns_data['lanDnsServer']
		elif ifname == 'eth1':
			dns_data[ifname] = dns_data['wanDnsServer']
		else:
			dns_data[ifname] = []

	log_info(LOG_MODULE_SYSINFO, "DNS Servers : " + str(dns_data))
	return dns_data


def device_update_lan_dns_server():
	option_str = ""
	dns_data = device_info_get_dns_server(None)

	# Check LAN dhcp option
	output, error = subprocess_open("uci show dhcp.lan.dhcp_option")
	if 'dhcp.lan.dhcp_option' in output:
		# Already exist
		log_info(LOG_MODULE_APCLIENT, "dhcp option already exist")
		return

	dns_list = dns_data[WAN_DNS_SERVER_KEY]
	if len(dns_list) > 0:
		option_str = "6"
		for dns_server in dns_list:
			if dns_server in option_str:
				continue
			option_str = option_str + "," + dns_server

	if len(option_str):
		cmd_str = "uci set dhcp.lan.dhcp_option='%s'" % str(option_str)
		output, error = subprocess_open(cmd_str)
		log_info(LOG_MODULE_APCLIENT, "dhcp option = %s, outout:%s, error:%s" % (cmd_str, output, error))

		cmd_str = "uci commit"
		subprocess_open(cmd_str)

		pmr = PuciModuleRestart(None)
		pmr._puci_container_module_restart("dnsmasq", True)

	log_info(LOG_MODULE_APCLIENT, "dhcp option string '%s'" % option_str)
	return

'''
Hardware Information Class
'''
def hardware_info_list():
	hardware_info = HardwareInformation()
	interface_data = hardware_info._make_hardware_interface_info_data("all")
	data = {
		"hardware-info": {
			"interface-info" : interface_data,
		},
		'header': {
			'resultCode': 200,
			'resultMessage': 'Success.',
			'isSuccessful': 'true'
		}
	}
	return data


class HardwareInformation():
	def __init__(self):
		pass

	def _make_hardware_interface_info_data(self, if_type):
		if if_type == "all":
			self.data = {
				"maxLanPort": MAX_LAN_PORTS,
				"maxWanPort": MAX_WAN_PORTS,
				"interfaces" : device_get_interface_info(),
			}
		elif if_type == "wan":
			self.data = device_get_wan_interface_info()
		elif if_type == "lan":
			self.data = device_get_lan_interface_info()
		else:
			self.data = "Not support interface"

		#log_info(LOG_MODULE_SYSINFO, "=" * 80)
		#log_info(LOG_MODULE_SYSINFO, "<Make Request Message>")
		#log_info(LOG_MODULE_SYSINFO, json.dumps(self.data, indent=2))

		return self.data


def device_get_port_name_by_idx(port_idx):
	for key in port_map:
		if key == port_idx:
			return port_map[key]

def device_get_if_bridge_mode():
	ifBridge = False
	ifBridgeList = []

	cmd_str = "brctl show"
	output, error = subprocess_open(cmd_str)
	if 'br-lan' in output:
		output = output.split('\n')
		for line in output:
			token = line.split()

			if ifBridge == True:
				if len(token) == 1:
					ifBridgeList.append(token[0])
					continue
				else:
					break

			if not 'br-lan' in line:
				continue
			ifBridge = True
			if len(token) > 3 and token[3]:
				ifBridgeList.append(token[3])

	log_debug(LOG_MODULE_SYSINFO, "ifBridge :" + str(ifBridge))
	log_debug(LOG_MODULE_SYSINFO, "ifBridgeList :" + str(ifBridgeList))
	return ifBridge, ifBridgeList

def device_get_interface_operstate(ifname):
	filename = '/sys/class/net/' + ifname + '/flags'
	try:
		with open(filename, 'r') as f:
			flags = int(f.read()[2:-1])
			if (flags % 2) == 1:
				return True
			else:
				return False
	except:
		log_error(LOG_MODULE_SYSINFO, "file '%s' open() error" % filename)
		return False

def device_get_wireless_state(ifname):
	return device_get_interface_operstate(ifname)

def device_get_port_link_status(port_idx):
	'''
	call SWIG function for ioctl
	'''
	link_status = ln.network_link_status_get(port_idx)
	if link_status == 1:
		return True
	else:
		return False

def device_get_port_info(type):
	data = list()

	if type == "wan":
		port_idx = PORT_WAN_IDX
		port_data = {
			"portName" : device_get_port_name_by_idx(port_idx),
			"portSpeed" : "1000M",
			"portDuplex" : "full duplex",
			"portLinkStatus" : device_get_port_link_status(port_idx)
		}
		data.append(port_data)
	else:
		for port_idx in lan_port_idx_list:
			port_data = {
				"portName": device_get_port_name_by_idx(port_idx),
				"portSpeed": "1000M",
				"portDuplex": "full duplex",
				"portLinkStatus": device_get_port_link_status(port_idx)
			}
			data.append(port_data)

	return data

def device_get_interface_info():
	iface_list = list()

	data = {
		"ifName": "eth1",
        "ifType" : "wan",
		"ifBridge": False,
		"ifBridgeList": [],
		"portList": device_get_port_info("wan"),
		"ifPhyAddress": device_info_get_hwaddr("eth1"),
		"ifOperStatus": device_get_interface_operstate("eth1"),
		"ifUptime": ""
	}
	iface_list.append (data)

	ifBridge, ifBridgeList = device_get_if_bridge_mode()
	if ifBridge == True:
		ifname = "br-lan"
	else:
		ifname = "eth0"

	data = {
		"ifName" : ifname,
        "ifType": "lan",
		"ifBridge" : ifBridge,
		"ifBridgeList" : ifBridgeList,
		"portList" : device_get_port_info("lan"),
		"ifPhyAddress" : device_info_get_hwaddr(ifname),
		"ifOperStatus" : device_get_interface_operstate(ifname),
		"ifUptime" : ""
	}
	iface_list.append(data)

	return iface_list

def device_get_wan_interface_info():
	data = {
		"ifName" : "eth1",
		"ifBridge": False,
		"ifBridgeList": [],
		"portList" : device_get_port_info("wan"),
		"ifPhyAddress" : device_info_get_hwaddr("eth1"),
		"ifOperStatus" : device_get_interface_operstate("eth1"),
		"ifUptime" : ""
	}
	return data

def device_get_lan_interface_info():
	ifBridge, ifBridgeList = device_get_if_bridge_mode()
	if ifBridge == True:
		ifname = "br-lan"
	else:
		ifname = "eth0"

	data = {
		"ifName" : ifname,
		"ifBridge" : ifBridge,
		"ifBridgeList" : ifBridgeList,
		"portList" : device_get_port_info("lan"),
		"ifPhyAddress" : device_info_get_hwaddr(ifname),
		"ifOperStatus" : device_get_interface_operstate(ifname),
		"ifUptime" : ""
	}
	return data


'''
Wireless Stations
'''
class WirelessStation(object):
	def __init__(self):
		self.wireless_2g_station_file = "/tmp/wireless_station_2g_"
		self.wireless_5g_station_file = "/tmp/wireless_station_5g_"

		self.wirless_config_map = {
			"macAddr"         : "macAddr",
			"TxRate_MCS"      : "TxRateMCS",
			"TxRate_BW"       : "TxRateBW",
			"TxRate_GI"       : "TxRateGI",
			"TxRate_PhyMode" : "TxRateMode",
			"AvgRssi0"        : "rssi",
			"connectTime"     : "connectTime"
		}

	def make_wireless_station_data_file(self, ifname, file_name):
		if os.path.exists(file_name):
			os.remove(file_name)
		ln.wireless_station_get(ifname, file_name)

	def get_rssi_dbm_value(self, value):
		'''
		Temporary....;;
		'''
		if value > 180 and value < 190:
			ret_val =  randint(50, 60)
		elif value > 190 and value < 200:
			ret_val = randint(60, 70)
		elif value > 160 and value < 170:
			ret_val = randint(50, 60)
		elif value > 200 and value < 220:
			ret_val = randint(70, 80)
		else:
			ret_val = randint(80, 90)

		return -(ret_val)

	def get_wireless_station_data(self, ap_type, ifname, list_data):
		dict_data = dict()
		if "5g_" in ap_type:
			file_name = self.wireless_2g_station_file + ifname
		else:
			file_name = self.wireless_5g_station_file + ifname

		self.make_wireless_station_data_file(ifname, file_name)

		if not os.path.exists(file_name):
			log_debug(LOG_MODULE_SYSINFO, "Not exist file name(%s)" %file_name)
			return list_data

		with open(file_name, 'r') as rfile:
			lines = rfile.readlines()

			for line in lines:
				if line.strip() == '':
					# End of a instance
					list_data.append(dict_data)
					dict_data = dict()
					continue

				line = line.split(':', 1)
				if len(line) < 2: continue

				line_key = line[0].strip()
				line_value = line[1].strip()

				dict_data['type'] = ap_type

				for key, value in self.wirless_config_map.items():
					if key.strip() != line_key:
						continue

					if value == 'connectTime':
						temp_time = int(line_value)
						hr = temp_time / 3600
						min = (temp_time % 3600) / 60
						sec = (temp_time - (hr * 3600) - (min * 60))
						dict_data['connectTime'] = "%sh %sm %ss" % (hr, min, sec)
					elif value == 'rssi':
						dict_data[value] = str(self.get_rssi_dbm_value(int(line_value))) + " dBm"
					else:
						dict_data[value] = line_value

		log_info(LOG_MODULE_SYSINFO, "Get wireless stations : %s for ifname(%s)" %(str(list_data), ifname))
		return list_data
