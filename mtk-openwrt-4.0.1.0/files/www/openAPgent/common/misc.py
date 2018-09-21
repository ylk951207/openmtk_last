import os
import subprocess
import shlex
from common.log import *
from common.env import *
from conf.ap_device_config import *


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
Device Information Functions
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
		#gDeviceInfo.ip_addr = ni.ifaddresses(WAN_ETHDEV)[ni.AF_INET][0]['addr']
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

		log_info(LOG_MODULE_MISC, "=" * 80)
		log_info(LOG_MODULE_MISC,  "<Make Request Message>")
		log_info(LOG_MODULE_MISC, json.dumps(self.data, indent=2))

		return self.data


def device_info_get_ip_address(ifname):
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