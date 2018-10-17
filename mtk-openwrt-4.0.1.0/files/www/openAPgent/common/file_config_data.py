from common.log import*

CONFIG_TYPE_STRING = 1
CONFIG_TYPE_INTEGER = 2
CONFIG_TYPE_BOOLEAN = 3
CONFIG_TYPE_LIST_STRING = 4

VALUE_TYPE_EMPTY = ""
VALUE_TYPE_ZERO = "0"
VALUE_TYPE_ONE = "1"
VALUE_TYPE_TWO = "2"
VALUE_TYPE_DISABLE = "DISABLE"

def file_config_data_get_section_map(field_name, *args):
	log_info(LOG_MODULE_SAL, "ARGS: " + str(args[0]))

	if field_name == 'wireless_common_config':
		if args and args[0]:
			section_map = {
				'mode'              : [CONFIG_TYPE_INTEGER, "WirelessMode",                  " "],
				'channel'           : [CONFIG_TYPE_INTEGER, "Channel",                       " "],
				'authMode'          : [CONFIG_TYPE_STRING,  "AuthMode",                      " "],
				'privacyMode'       : [CONFIG_TYPE_STRING,  "EncrypType",                    " "],
				'wps'               : [CONFIG_TYPE_STRING,  "WscConfMode",                   " "],
				'password'          : [CONFIG_TYPE_STRING,  ''.join(["WPAPSK", args[0]]),    " "],
				# 'password'          : [CONFIG_TYPE_STRING,  ''.join(["Key1Str", args[0]]),   " "],
				'ssid'              : [CONFIG_TYPE_STRING,  ''.join(["SSID", args[0]]),      " "],
				'bssid'             : [CONFIG_TYPE_STRING,  " ",                             " "],
				'devName'           : [CONFIG_TYPE_STRING,  " ",                             " "],
				'type'              : [CONFIG_TYPE_STRING,  " ",                             " "],
				'enable'            : [CONFIG_TYPE_BOOLEAN, " ",                             " "],
				'status'            : [CONFIG_TYPE_STRING,  " ",                             " "],
			}
		return section_map


	if field_name == 'wireless_generate_config':
		if args and args[0]:
			section_map = {
				'BssidNum'          :['',                       ''],
				'DefaultKeyID'      :[VALUE_TYPE_ONE,           ''],
				'HideSSID'          :[VALUE_TYPE_ZERO,          ''],
				'IEEE8021X'         :[VALUE_TYPE_ZERO,          ''],
				'Key1Type'          :[VALUE_TYPE_ZERO,          ''],
				'Key2Type'          :[VALUE_TYPE_ZERO,          ''],
				'Key3Type'          :[VALUE_TYPE_ZERO,          ''],
				'Key4Type'          :[VALUE_TYPE_ZERO,          ''],
				'NoForwarding'      :[VALUE_TYPE_ZERO,          ''],
				'PreAuth'           :[VALUE_TYPE_ZERO,          ''],
				'RADIUS_Server'     :[VALUE_TYPE_ZERO,          ''],
				'WmmCapable'        :[VALUE_TYPE_ONE,           ''],
				'WscConfStatus'     :[VALUE_TYPE_TWO,           ''],
				'RekeyInterval'     :[VALUE_TYPE_EMPTY,         ''],
				'RekeyMethod'       :[VALUE_TYPE_DISABLE,       ''],

			}

		return section_map


	if field_name == 'wireless_search_config':
		if args and args[0]:
			section_map = {
				'ssid'              : [CONFIG_TYPE_STRING, " "],
				'channel'           : [CONFIG_TYPE_STRING, " "],
				'bssid'             : [CONFIG_TYPE_STRING, " "],
				'authMode'          : [CONFIG_TYPE_STRING, " "],
				'privacyMode'       : [CONFIG_TYPE_STRING, " "],
				'rssi'              : [CONFIG_TYPE_STRING, " "],
			}
			return section_map


