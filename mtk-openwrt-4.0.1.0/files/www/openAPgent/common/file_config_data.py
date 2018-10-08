
from common.log import*

CONFIG_TYPE_SCALAR=1

def file_config_data_get_section_map(field_name, *args):

	log_info(LOG_MODULE_SAL, "ARGS: " + str(args[0]))
	if field_name == 'wireless_common_config':
		if args and args[0]:
			section_map = {
				'mode'              : [CONFIG_TYPE_SCALAR, "WirelessMode",                  " "],
				'channel'           : [CONFIG_TYPE_SCALAR, "Channel",                       " "],
				'authMode'          : [CONFIG_TYPE_SCALAR, "AuthMode",                      " "],
				'privacyMode'       : [CONFIG_TYPE_SCALAR, "EncrypType",                    " "],
				'wps'               : [CONFIG_TYPE_SCALAR, "WscConfMode",                   " "],
				'password'          : [CONFIG_TYPE_SCALAR, ''.join(["WPAPSK", args[0]]),    " "],
				'ssid'              : [CONFIG_TYPE_SCALAR, ''.join(["SSID", args[0]]),      " "],
				'bssid'             : [CONFIG_TYPE_SCALAR, " ",                             " "],
				'devName'           : [CONFIG_TYPE_SCALAR, " ",                             " "],
				'type'              : [CONFIG_TYPE_SCALAR, " ",                             " "],
				'enable'            : [CONFIG_TYPE_SCALAR, "add_plan",                      " "],
				'status'            : [CONFIG_TYPE_SCALAR, "add_plan",                      " "],
			}
			return section_map


	if field_name == 'wireless_search_config':
		if args and args[0]:
			section_map = {
				'ssid'              : [CONFIG_TYPE_SCALAR, " "],
				'channel'           : [CONFIG_TYPE_SCALAR, " "],
				'bssid'             : [CONFIG_TYPE_SCALAR, " "],
				'authMode'          : [CONFIG_TYPE_SCALAR, " "],
				'privacyMode'       : [CONFIG_TYPE_SCALAR, " "],
				'rssi'              : [CONFIG_TYPE_SCALAR, " "],
			}
			return section_map

