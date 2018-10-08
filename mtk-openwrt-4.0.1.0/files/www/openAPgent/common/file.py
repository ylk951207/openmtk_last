import fcntl
import os

from common.log import *
from common.env import *
from common.misc import *
from common.file_config_data import *


DELIMITER_EQUEL = "="
DELIMITER_SPACE = " "
DELIMITER_DOT = "."
LOG_MODULE_FILE = "file"

'''
I/O files of a specific path
'''
class ConfigFileProc:
	def __init__(self, field_name, config_path, config_name, *args):
		self.config_path = config_path
		self.config_name = config_name
		self.section_map = file_config_data_get_section_map(field_name, *args)
		log_info(LOG_MODULE_FILE, "Section_map(" + config_name + "): " + str(self.section_map))

	'''
	Read the data and split it by delimiter
	'''
	def read_file_data(self, delimiter):
		file_data = dict()
		with open(self.config_path + self.config_name, 'r') as f:
			lines = f.readlines()
			for line in lines:
				line = line.replace("\r\n", "")
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
	def write_file_data(self, req_data, delimiter, header):
		log_info(LOG_MODULE_FILE, "request_data = " + str(req_data))

		file_data = self.read_file_data(delimiter)
		apply_req_data = self.apply_request_data(req_data)

		for key, val in file_data.items():
			for req_key, req_val in apply_req_data.items():
				if key == req_key:
					file_data[key] = apply_req_data[req_key]

		with open(self.config_path + self.config_name, 'w') as f:
			f.write(header)
			for file_data_key, file_data_val in file_data.items():
				write_data = delimiter.join([file_data_key, file_data_val]) + "\n"
				f.write(write_data)

	'''
	Get section map
	'''
	def get_file_data_section_map(self, delimiter):

		file_data = self.read_file_data(delimiter)

		for map_key, map_val in self.section_map.items():
			for key, val in file_data.items():
				if map_val[1] in key:
					map_val[2] = file_data[map_val[1]]
					self.section_map[map_key] = map_val

		return self.section_map

	'''
	Apply data using request value
	'''
	def apply_request_data(self, req_data):
		apply_req_data = dict()

		for map_key, map_val in self.section_map.items():
			for req_key, req_val in req_data.items():
				if map_key == req_key:
					apply_map_key = map_val[1]
					apply_req_data[apply_map_key] = req_val

		return apply_req_data


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
