import fcntl
import os

from common.env import *
from common.misc import *
from conf.wireless_config_data import *


DELIMITER_EQUEL = "="
DELIMITER_SPACE = " "
DELIMITER_DOT = "."
LOG_MODULE_FILE = "file"

'''
I/O files of a specific path
'''
class ConfigFileProc:
	def __init__(self, field_name, config_file, *args):
		self.config_file = config_file
		self.section_map = file_config_data_get_section_map(field_name, *args)
		log_info(LOG_MODULE_FILE, "Section_map(" + config_file + "): " + str(self.section_map))

	'''
	Get section map
	'''
	def get_file_data_section_map(self, delimiter):

		file_data = self.read_file_data(delimiter)

		for map_key, map_val in self.section_map.items():
			for key, val in file_data.items():
				if map_val[1] == key:
					map_val[2] = self.convert_get_config_value(map_val[0], file_data[map_val[1]])
					self.section_map[map_key] = map_val

		return self.section_map

	'''
	Read the data and split it by delimiter
	'''
	def read_file_data(self, delimiter):
		file_data = dict()
		with open(self.config_file, 'r') as f:
			lines = f.readlines()
			for line in lines:
				line = line.strip()
				if delimiter in line:
					tokens = line.split(delimiter)

					if tokens and tokens[1]:
						file_data[tokens[0]] = tokens[1]
					else:
						file_data[tokens[0]] = ""
			return file_data

	'''
	Rewrite to a file of a specific path using the request value
	'''
	def write_file_data(self, req_data, delimiter, header, add_header = True):
		temp_file = ".".join([self.config_file, 'temp'])
		log_info(LOG_MODULE_FILE, "request_data = " + str(req_data))

		apply_req_data = self.apply_request_data(req_data, add_header)
		with open(self.config_file, 'r') as f:
			lines = f.readlines()

		with open(temp_file, 'w') as fw:
			fw.write(header)
			for line in lines:
				if '#' in line:	continue
				token = line.strip()
				tokens = token.split(delimiter)
				if len(tokens) == 2:
					for key, val in apply_req_data.items():
						if tokens[0] == key:
							tokens[1] = val
					if not tokens[1]:
						tokens[1] = '\n'
					else:
						tokens[1] = str(tokens[1]) + '\n'
					fw.write('='.join(tokens))

		os.rename(temp_file, self.config_file)

	'''
	Apply data using request value
	'''
	def apply_request_data(self, req_data, add_header):
		apply_req_data = req_data
		if add_header == True:
			for map_key, map_val in self.section_map.items():
				for req_key, req_val in req_data.items():
					if map_key == req_key:
						apply_map_key = map_val[1]
						apply_req_data[apply_map_key] = self.convert_set_config_value(map_val[0], req_val)

		return apply_req_data


	'''
	Changes the string to a different type
	'''
	def convert_get_config_value(self, type, val):
		if not val:
			return val
		if type == CONFIG_TYPE_INTEGER:
			if isinstance(val, str) and val != '\n':
				val = int(val)
				return val
		elif type == CONFIG_TYPE_BOOLEAN:
			if isinstance(val, bool):
				if val == "1":	return True
				elif val == "0": return False
		else:
			return val

	'''
	Change other types to strings.
	'''
	def convert_set_config_value(self, type, val):
		if type == CONFIG_TYPE_INTEGER:
			if isinstance(val, int):
				val = str(val)
				return val
		elif type == CONFIG_TYPE_BOOLEAN:
			if isinstance(val, bool):
				if val == True:	return "1"
				elif val == False: return "0"
		else:
			return val

'''
File Lock Class
'''
class FileLock:
	"""Implements a file-based lock using flock(2).
    The lock file is saved in directory dir with name lock_name.
    dir is the current directory by default.
    """

	def __init__(self, lock_name, dir="."):
		self.lock_file = open(os.path.join(dir, lock_name), "w")

	def acquire(self, blocking=True):
		"""Acquire the lock.
        If the lock is not already acquired, return None.  If the lock is
        acquired and blocking is True, block until the lock is released.  If
        the lock is acquired and blocking is False, raise an IOError.
        """
		ops = fcntl.LOCK_EX
		if not blocking:
			ops |= fcntl.LOCK_NB
		fcntl.flock(self.lock_file, ops)
		log_info(LOG_MODULE_FILE, "++ Acqure File Lock (%s) ++" % self.lock_file)

	def release(self):
		"""Release the lock. Return None even if lock not currently acquired"""
		fcntl.flock(self.lock_file, fcntl.LOCK_UN)
		log_info(LOG_MODULE_FILE, "++ Release File Lock (%s) ++" % self.lock_file)
