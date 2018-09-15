import os
import subprocess
import shlex
from common.log import *
from common.env import *
from common.request import *
from uci_data import *


UCI_SHOW_CMD="uci show "
UCI_EXPORT_CMD="uci export "
UCI_GET_CMD="uci get "
UCI_SET_CMD="uci set "
UCI_DELETE_CMD="uci delete "
UCI_ADD__CMD="uci add "
UCI_ADD_LIST_CMD="uci add_list "
UCI_DELETE_LIST_CMD="uci delete_list "
UCI_COMMIT_CMD="uci commit "


LOG_MODULE_PUCI="puci"

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


def restart_uci_config_module(config_file, ifname):
    if config_file == 'network' and ifname:
        log_info(LOG_MODULE_PUCI, "ifdown/ifup for ifname: " + ifname)
        output, error = subprocess_open('ifdown ' + ifname)
        output, error = subprocess_open('ifup ' + ifname)
    else:
        log_info(LOG_MODULE_PUCI, "Service uci config restart : " + config_file)
        command = '/etc/init.d/' + config_file + ' restart'
        log_info(LOG_MODULE_PUCI, "===" , command + "===")
        output, error = subprocess_open(command)

    return output, error


def puci_send_message_to_apnotifier(command, noti_data):
    if os.path.exists(PROVISIONING_DONE_FILE):
        server_msg = ApServerLocalMassage(APNOTIFIER_CMD_PORT)
        server_msg.send_message_to_apnotifier("PUCI", command, noti_data)
        log_info(LOG_MODULE_PUCI, "** Send service module restart message to apClient **")
    else:
        log_info(LOG_MODULE_PUCI, "Cannot find provisioining file(%s)" %PROVISIONING_DONE_FILE)

#
# TODO: Detail error handling 
#
class ConfigUCI:
    def __init__(self, config_file, config_name, *args):
        self.config_file = config_file
        self.config_name = config_name
        self.section_map = uci_get_section_map(config_name, *args)
        log_info(LOG_MODULE_PUCI, "Section_map(" + config_name + "): " + str(self.section_map))
                               
    def commit_uci_config(self):
        #log_info(LOG_MODULE_PUCI, "=== " , UCI_COMMIT_CMD + self.config_file + " ===")
        return subprocess_open(UCI_COMMIT_CMD + self.config_file)

    '''
      Add uci section
      Command - uci add <config> <section-type>
    '''
    def add_uci_config(self, option):
        log_info(LOG_MODULE_PUCI, UCI_ADD_CMD + self.config_file + option)
        output, error = subprocess_open(UCI_ADD_CMD + self.config_file + option)
        if not error:
            self.commit_uci_config()
        else:
            log_error(LOG_MODULE_PUCI, "add_uci_config() error:" + error)

        return output, error

    '''
      Set uci value
      Command - uci set <config>.<section>[.<option>]=<value>
    '''
    def set_uci_config_scalar(self, option, value):
        log_info(LOG_MODULE_PUCI, UCI_SET_CMD + option + '=' + value)
        output, error = subprocess_open(UCI_SET_CMD + option + '=' + value)
        if not error:
            self.commit_uci_config()
        else:
            log_error(LOG_MODULE_PUCI, "set_uci_config_scalar() error:" + error)
        return output, error

    '''
      Set uci list value
      Command - uci add_list <config>.<section>.<option>=<string>
    '''
    def set_uci_config_list(self, option, values):
        output = None
        error = 0
        
        while len(values) > 0:
            value = values.pop()
            if not value: continue
        
            if isinstance(value, basestring):
                value = value.strip()
                if not value: continue

            log_info(LOG_MODULE_PUCI, UCI_ADD_LIST_CMD + option + '=' + str(value))
            output, error = subprocess_open(UCI_ADD_LIST_CMD + option + '=' + value)
            if not error:
                self.commit_uci_config()
            else:
                log_error(LOG_MODULE_PUCI, "set_uci_config_list() error:" + error)
        return output, error

    def set_uci_config(self, req):
        for req_key in req.keys():
            req_val = req[req_key]
            
            # Check dictionary value
            if isinstance(req_val, dict):
                continue

            req_val = req[req_key]

            # Update the requested SET Value to section_map
            if req_key in self.section_map:
                map_val = self.section_map[req_key]
                map_val[2] = self.convert_config_value(req_val)
                if req_key != "macAddr":
                    map_val.append('section_map_value_updated')

        log_info(LOG_MODULE_PUCI, "After SET Check:: Section_map(" + self.config_name + "): " + str(self.section_map))
        
        for map_val in self.section_map.values():
            if not 'section_map_value_updated' in map_val: continue

            self.delete_uci_config(map_val[1])

            if not map_val[2]: continue

            if isinstance(map_val[2], basestring):
                map_val[2] = map_val[2].strip()
                if not map_val[2]: continue

            log_info(LOG_MODULE_PUCI, "Set uci config for '" +
                     self.config_name + "', uci values[key,value]: " + str(map_val[1]) + ", " + str(map_val[2]))

            if map_val[0] == CONFIG_TYPE_SCALAR:
                self.set_uci_config_scalar(map_val[1], str(map_val[2]))
            else:
                self.set_uci_config_list(map_val[1], map_val[2])

    def delete_uci_list_config(self, option, value):
        log_info(LOG_MODULE_PUCI, UCI_DELETE_LIST_CMD + option + '=' + value)
        output, error = subprocess_open(UCI_DELETE_LIST_CMD + option + '=' + value)
        if not error:
            self.commit_uci_config()
        return output, error
        
    def delete_uci_config(self, option):
        log_info(LOG_MODULE_PUCI, UCI_DELETE_CMD + option)
        output, error = subprocess_open(UCI_DELETE_CMD + option)
        if not error:
            self.commit_uci_config()
        return output, error
        
    def show_uci_config(self):
        log_info(LOG_MODULE_PUCI, UCI_SHOW_CMD + self.config_file)
        output, error = subprocess_open(UCI_SHOW_CMD + self.config_file)
        
        if error: return None
        
        lines = output.splitlines()

        for line in lines:
            token = line.split('=')

            for map_val in self.section_map.values():
                if map_val[1] != token[0]: continue
                
                if map_val[0] == CONFIG_TYPE_SCALAR:
                    if token[1][0] == "'":
                        token[1] = token[1][1:-1]
                    map_val[2] = token[1]
                else:
                    # change uci format ['A' 'B' 'C'] string to ['A', 'B', 'C'] list.
                    list_value = token[1].split(' ')
                    map_val[2] = list()
                    while len(list_value):
                        value = list_value.pop()
                        
                        if value[0] == "'":
                            value = value[1:-1]

                        map_val[2].append(value)

        log_info(LOG_MODULE_PUCI, "self.section_map = ", self.section_map)

    def convert_config_value(self, val):
        if val == True: return 1
        elif val == False: return 2
        else: return val

