from common.misc import*

CONFIG_TYPE_STRING = 1
CONFIG_TYPE_INTEGER = 2
CONFIG_TYPE_BOOLEAN = 3
CONFIG_TYPE_LIST_STRING = 4

def file_config_data_get_section_map(field_name, *args):
	log_info(LOG_MODULE_SAL, "ARGS: " + str(args[0]))

	if field_name == 'wireless_common_config':
		if args and args[0]:
			section_map = {
				'mode'             : [CONFIG_TYPE_INTEGER, "WirelessMode",                  " "],
				'channel'          : [CONFIG_TYPE_INTEGER, "Channel",                       " "],
				'authMode'         : [CONFIG_TYPE_STRING,  "AuthMode",                      " "],
				'privacyMode'      : [CONFIG_TYPE_STRING,  "EncrypType",                    " "],
				'wps'              : [CONFIG_TYPE_STRING,   "WscConfMode",                   " "],
				'password'         : [CONFIG_TYPE_STRING,  " ",           " "],
				'ssid'             : [CONFIG_TYPE_STRING,  "".join(["SSID", args[0]]), " "],
				'bssid'            : [CONFIG_TYPE_STRING,  " ", " "],
				'devName'          : [CONFIG_TYPE_STRING,  " ", " "],
				'type'             : [CONFIG_TYPE_STRING,  " ", " "],
				'enable'           : [CONFIG_TYPE_BOOLEAN, " ", " "],
				'status'           : [CONFIG_TYPE_STRING,  " ", " "],

				'internal_DefaultKeyID':       [CONFIG_TYPE_INTEGER, "DefaultKeyID",     " "],
				'internal_Key1Str1' :          [CONFIG_TYPE_STRING,  "Key1Str1",         " "],
				'internal_WPAPSK1':            [CONFIG_TYPE_STRING,  "WPAPSK1",          " "],
				'internal_WscModeOption':      [CONFIG_TYPE_INTEGER, "WscModeOption",    " "],
				'internal_RekeyMethod':        [CONFIG_TYPE_STRING, "RekeyMethod", " "],
				'internal_AutoChannelSelect':  [CONFIG_TYPE_INTEGER, "AutoChannelSelect",    " "],
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
