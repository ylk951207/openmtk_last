from common.log import*

CONFIG_TYPE_STRING = 1
CONFIG_TYPE_INTEGER = 2
CONFIG_TYPE_BOOLEAN = 3
CONFIG_TYPE_LIST_STRING = 4

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
				'ssid'              : [CONFIG_TYPE_STRING,  ''.join(["SSID", args[0]]),      " "],
				'bssid'             : [CONFIG_TYPE_STRING,  " ",                             " "],
				'devName'           : [CONFIG_TYPE_STRING,  " ",                             " "],
				'type'              : [CONFIG_TYPE_STRING,  " ",                             " "],
				'enable'            : [CONFIG_TYPE_BOOLEAN, " ",                             " "],
				'status'            : [CONFIG_TYPE_STRING,  " ",                             " "],
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

