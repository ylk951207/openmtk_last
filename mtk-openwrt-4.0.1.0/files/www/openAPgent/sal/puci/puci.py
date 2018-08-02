import subprocess
import shlex

from common.log import *
from common.env import *
from uci_data import *


UCI_SHOW_CMD="uci show "
UCI_EXPORT_CMD="uci export "
UCI_GET_CMD="uci get "
UCI_SET_CMD="uci set "
UCI_DELETE_CMD="uci delete "
UCI_ADD_LIST_CMD="uci add_list "
UCI_DELETE_LIST_CMD="uci delete_list "
UCI_COMMIT_CMD="uci commit "



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


# TODO: Detail error handling 
#
class ConfigUCI:
    def __init__(self, config_name, *args):
        self.config_name = config_name
        self.section_map = uci_get_section_map(config_name, *args)
        log_info(LOG_MODULE_SAL, "Section_map(" + config_name + "): " + str(self.section_map))

    def restart_module(self):
        command = '/www/openAPgent/utils/apply_config '+ self.config_name + ' &'
        log_info(LOG_MODULE_SAL, "===" , command + "===")  
        return subprocess_open(command)
                               
    def commit_uci_config(self):
        log_info(LOG_MODULE_SAL, "===" , UCI_COMMIT_CMD + self.config_name + "===")  
        return subprocess_open(UCI_COMMIT_CMD + self.config_name)

    def set_uci_list_config(self, option, value):
        log_info(LOG_MODULE_SAL, UCI_ADD_LIST_CMD + option + '=' + value)  
        output, error = subprocess_open(UCI_ADD_LIST_CMD + option + '=' + value)
        if not error:
            self.commit_uci_config()
        return output, error
        
    def set_uci_config(self, option, value):
        log_info(LOG_MODULE_SAL, UCI_SET_CMD + option + '=' + value)
#        output, error = subprocess_open(UCI_SET_CMD + ".".join([config, section, option]) + "=" + value)
        output, error = subprocess_open(UCI_SET_CMD + option + '=' + value)
        if not error:
            self.commit_uci_config()
        return output, error

    def delete_uci_list_config(self, option, value):
        log_info(LOG_MODULE_SAL, UCI_DELETE_LIST_CMD + option + '=' + value)  
        output, error = subprocess_open(UCI_DELETE_LIST_CMD + option + '=' + value)
        if not error:
            self.commit_uci_config()
        return output, error
        
    def delete_uci_config(self, option):
        log_info(LOG_MODULE_SAL, UCI_DELETE_CMD + option)  
        output, error = subprocess_open(UCI_DELETE_CMD + option)
        if not error:
            self.commit_uci_config()
        return output, error
        
    def show_uci_config(self, option):
        if option:
            log_info(LOG_MODULE_SAL, UCI_SHOW_CMD + self.config_name + "." + option)
            output, error = subprocess_open(UCI_SHOW_CMD + self.config_name + '.' + option)
        else:
            log_info(LOG_MODULE_SAL, UCI_SHOW_CMD + self.config_name)
            output, error = subprocess_open(UCI_SHOW_CMD + self.config_name)
        
        if not error:
            line = output.splitlines()

            for i in range (0, len(line)):
                token = line[i].split('=')

                for map_key in self.section_map.keys():
                    map_val = self.section_map[map_key]
                    if map_val[1] == token[0]:
                        map_val[2] = token[1]
                        break;
                i += 1

            log_info(LOG_MODULE_SAL, "self.section_map = ", self.section_map)

    def set_uci_config_list_value(self, keyword, option, list_value):
        for i in range (0, len(list_value)):
            self.set_uci_list_config(option, list_value[i])
        
    def convert_config_value(self, val):
        if val == True:
            return 1
        elif val == False:
            return 2
        else:
            return val


#TEST
#result = get_config_object("system", "@system[0]", "log_file")
#result = set_config_object("system", "@system[0]", "log_file", "/tmp/messages")

