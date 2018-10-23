from puci import *
from common.env import *
from common.misc import *


UCI_NETWORK_FILE="network"
UCI_VLAN_COMMON_CONFIG_CONFIG = "vlan_common_config"
UCI_VLAN_CONFIG_CONFIG = "vlan_config"


'''
Switch VLAN
'''

def puci_vlan_config_list():
	vlan_list_body = dict()
	vlan_body = list()
	vlan_info_list = vlan_config_get_info(None)

	for vlan_key, vlan_value in vlan_info_list.items():
		vlan_data = vlan_config_uci_get(vlan_key, UCI_VLAN_CONFIG_CONFIG)
		vlan_body.append(vlan_data)

	common_data = vlan_config_uci_get(None, UCI_VLAN_COMMON_CONFIG_CONFIG)
	vlan_list_body[common_data.keys()[0]] = common_data.values()[0]
	vlan_list_body['vlan-list'] = vlan_body





	data = {
		"vlan": vlan_list_body,
		'header': {
			'resultCode': 200,
			'resultMessage': 'Success.',
			'isSuccessful': 'true'
		}
	}
	return data

def puci_vlan_config_retrieve(vlan_id, add_header):
	vlan_info_list = vlan_config_get_info(vlan_id)

	for vlan_key, vlan_value in vlan_info_list.items():
		if vlan_value == vlan_id:
			vlan_data = vlan_config_uci_get(vlan_key, UCI_VLAN_CONFIG_CONFIG)

	data = {
		'vlan': vlan_data,
		'header': {
			'resultCode': 200,
			'resultMessage': 'Success.',
			'isSuccessful': 'true'
		}
	}
	return data


def puci_vlan_config_create(request):
	return vlan_config_set(request)

def puci_vlan_config_update(request):
	return vlan_config_set(request)


def puci_vlan_config_detail_create(request, vlan_id):
	return vlan_config_detail_set(request, vlan_id)

def puci_vlan_config_detail_update(request, vlan_id):
	return vlan_config_detail_set(request, vlan_id)


def vlan_config_set(request):

	enable_data = {'enableVlan' : request['enableVlan']}
	vlan_config_uci_set(enable_data, None, UCI_VLAN_COMMON_CONFIG_CONFIG)

	vlan_list = request['vlan-list']
	vlan_info_list = vlan_config_get_info(None)

	while len(vlan_list) > 0:
		vlan_data = vlan_list.pop(0)
		found = False

		for vlan_key, vlan_value in vlan_info_list.items():
			if vlan_value == vlan_data['vlanId']:
				port_data = ""
				for i in vlan_data['ports']:

					if port_data == "":
						port_data = port_data + i
					else:
						port_data = port_data + " " + i
				port_data = "'" + port_data + "'"
				vlan_data['ports'] = port_data

				vlan_config_uci_set(vlan_data, vlan_key, UCI_VLAN_CONFIG_CONFIG)
				found = True

		if found == False:
			vlan_info_list = vlan_config_uci_add(' switch_vlan', vlan_data['vlanId'])

			for vlan_key, vlan_value in vlan_info_list.items():
				port_data = ""
				for i in vlan_data['ports']:
					if port_data == "":
						port_data = port_data + i
					else:
						port_data = port_data + " " + i
				port_data = "'" + port_data + "'"
				vlan_data['ports'] = port_data



				vlan_config_uci_set(vlan_data, vlan_key, UCI_VLAN_CONFIG_CONFIG)

	noti_data = dict()
	noti_data['config_file'] = UCI_NETWORK_FILE
	puci_send_message_to_apnotifier(SAL_PUCI_MODULE_RESTART, noti_data)

	data = {
		'header': {
			'resultCode': 200,
			'resultMessage': 'Success.',
			'isSuccessful': 'true'
		}
	}
	return data

def vlan_config_detail_set(request, vlan_id):
	vlan_info_list = vlan_config_get_info(vlan_id)
	port_data = ""
	if len(vlan_info_list) <= 0:
		vlan_info_list = vlan_config_uci_add(' switch_vlan', vlan_id)

	for vlan_key, vlan_value in vlan_info_list.items():
		if vlan_value == vlan_id:

			for i in request['ports']:
				if port_data == "":
					port_data = port_data + i
				else:
					port_data = port_data + " " + i
			port_data = "'" + port_data + "'"
			request['ports'] = port_data

			vlan_config_uci_set(request, vlan_key, UCI_VLAN_CONFIG_CONFIG)

	noti_data = dict()
	noti_data['config_file'] = UCI_NETWORK_FILE
	puci_send_message_to_apnotifier(SAL_PUCI_MODULE_RESTART, noti_data)

	data = {
		'header': {
			'resultCode': 200,
			'resultMessage': 'Success.',
			'isSuccessful': 'true'
		}
	}
	return data

def vlan_config_uci_get(vlan_info, uci_config_file):
	vlan_data = dict()
	uci_config = ConfigUCI(UCI_NETWORK_FILE, uci_config_file, vlan_info)
	if uci_config == None:
		raise RespNotFound("UCI Config")

	uci_config.show_uci_config()

	for map_key in uci_config.section_map.keys():
		map_val = uci_config.section_map[map_key]
		vlan_data[map_key] = map_val[2]

	if 'ports' in vlan_data.keys():
		vlan_data['ports'] = vlan_data['ports'].split()

	return vlan_data


def vlan_config_uci_add(vlan_str, vlan_id):
	vlan_info = dict()
	uci_config = ConfigUCI(UCI_NETWORK_FILE, UCI_VLAN_CONFIG_CONFIG, None)
	if uci_config == None:
		raise RespNotFound("UCI Config")

	uci_config.add_uci_config(vlan_str)

	output, error = subprocess_open(UCI_SHOW_CMD + UCI_NETWORK_FILE + "| tail -1")
	if error:
		return vlan_info

	vlan_line = output.splitlines()[0]
	vlan_key = vlan_line.split('.')[1].split('=')[0]
	vlan_value = vlan_id
	vlan_info[vlan_key] = vlan_value

	output, error = subprocess_open(UCI_SHOW_CMD + UCI_NETWORK_FILE + "| tail -1")
	if error:
		return vlan_info
	vlan_device = output.split('[')
	device_num = vlan_device[1][0]
	subprocess_open(UCI_SET_CMD + UCI_NETWORK_FILE + ".@switch_vlan[" + device_num +"].device='switch0'")

	return vlan_info

def vlan_config_uci_set(req_data, vlan_key, uci_config_file):
	uci_config = ConfigUCI(UCI_NETWORK_FILE, uci_config_file, vlan_key)
	if uci_config == None:
		raise RespNotFound("UCI Config")

	uci_config.set_uci_config(req_data)

def vlan_config_get_info(vlan_id):

	vlan_info = dict()
	awk_cmd = " | awk '{result=substr($1,9,1000); print result}'"
	if vlan_id:
		id_str = "\"vlan='" + vlan_id + "'\""
		filter_cmd = " | grep '@switch_vlan'" + "| grep " + id_str + awk_cmd
	else:
		filter_cmd = " | grep '@switch_vlan'" + "| grep vlan=" + awk_cmd

	output, error = subprocess_open(UCI_SHOW_CMD + UCI_NETWORK_FILE + filter_cmd)
	if error:
		return vlan_info

	if output:
		vlan_line = output.splitlines()
		for token in vlan_line:
			vlan_key = token.split('.')[0]
			vlan_value = token.split('=')[1].strip("'")
			vlan_info[vlan_key] = vlan_value

		return vlan_info

	else:
		return vlan_info

