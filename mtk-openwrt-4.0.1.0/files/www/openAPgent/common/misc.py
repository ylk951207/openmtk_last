import os
import shlex
import subprocess
#import netifaces as ni
import fcntl, socket, struct, json

from common.log import *
from common.env import *
from conf.ap_device_config import *
import libs._network as ln


LOG_MODULE_MISC="misc"

'''
Command Execution Functions
'''
def subprocess_open(command):
	popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	(stdoutdata, stderrdata) = popen.communicate()
	return stdoutdata, stderrdata

def subprocess_open_when_shell_false(command):
	popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdoutdata, stderrdata) = popen.communicate()
	return stdoutdata, stderrdata

def subprocess_open_when_shell_false_with_shelx(command):
	popen = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdoutdata, stderrdata) = popen.communicate()
	return stdoutdata, stderrdata

def subprocess_pipe(cmd_list):
	prev_stdin = None
	last_p = None

	for str_cmd in cmd_list:
		cmd = str_cmd.split()
		last_p = subprocess.Popen(cmd, stdin=prev_stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		prev_stdin = last_p.stdout

	(stdoutdata, stderrdata) = last_p.communicate()
	return stdoutdata, stderrdata


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

		log_info(LOG_MODULE_MISC,  "<Make Response Message>")
		log_info(LOG_MODULE_MISC, json.dumps(self.data, indent=2))

		return self.data


def device_info_get_ip_address(ifname):
	'''
	return ni.ifaddresses(ifname)[ni.AF_INET][0]['addr']
	'''
	f = os.popen('ifconfig '+ ifname +' | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
	return f.read()[:-1]

def device_info_get_serial_num():
	mac_addr = device_info_get_hwaddr(WAN_ETHDEV)
	token = mac_addr.split(':')
	return "AP_SR_NO7777_"+ token[3] + token[4] + token[5]

def device_info_get_hwaddr(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
	return ':'.join(['%02x' % ord(char) for char in info[18:24]])

def device_info_get_uptime():
	with open('/proc/uptime', 'r') as f:
		uptime_seconds = float(f.readline().split()[0])
		return uptime_seconds


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

		log_info(LOG_MODULE_MISC, "=" * 80)
		log_info(LOG_MODULE_MISC, "<Make Request Message>")
		log_info(LOG_MODULE_MISC, json.dumps(self.data, indent=2))

		return self.data


def device_get_if_bridge_mode():
	ifBridge = True
	ifBridgeList = ["eth0"]
	'''
	TODO
	'''
	return ifBridge, ifBridgeList

def device_get_if_oper_status(ifname):
	return False

def device_get_port_link_status(port_idx):
	'''
	call SWIG function for ioctl
	'''
	link_status = ln.network_link_status_get(port_idx)
	if link_status == 1:
		return True
	else:
		return False

'''
From left to right near wan port
'''
PORT_LAN_1_IDX = 0
PORT_LAN_2_IDX = 1
PORT_LAN_3_IDX = 2
PORT_LAN_4_IDX = 3
PORT_WAN_IDX = 4

lan_port_idx_list = [PORT_LAN_1_IDX, PORT_LAN_2_IDX, PORT_LAN_3_IDX, PORT_LAN_4_IDX]

port_map = {
	PORT_LAN_1_IDX: "LAN 1",
	PORT_LAN_2_IDX: "LAN 2",
	PORT_LAN_3_IDX: "LAN 3",
	PORT_LAN_4_IDX: "LAN 4",
	PORT_WAN_IDX: "WAN",
}

def device_get_port_name_by_idx(port_idx):
	for key in port_map:
		if key == port_idx:
			return port_map[key]

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
		"ifOperStatus": device_get_if_oper_status("eth1"),
		"ifUptime": ""
	}
	iface_list.append (data);

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
		"ifOperStatus" : device_get_if_oper_status(ifname),
		"ifUptime" : ""
	}
	iface_list.append(data);

	return iface_list;

def device_get_wan_interface_info():
	data = {
		"ifName" : "eth1",
		"ifBridge": False,
		"ifBridgeList": [],
		"portList" : device_get_port_info("wan"),
		"ifPhyAddress" : device_info_get_hwaddr("eth1"),
		"ifOperStatus" : device_get_if_oper_status("eth1"),
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
		"ifOperStatus" : device_get_if_oper_status(ifname),
		"ifUptime" : ""
	}
	return data
