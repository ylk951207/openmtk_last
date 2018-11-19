import os, sys
import shlex
import subprocess
import logging
from logging.handlers import RotatingFileHandler

from common.env import *


LOG_MODULE_MISC="misc"

'''
Command Execution Functions
'''

def subprocess_open_nonblock(command):
	try:
		subprocess.Popen(shlex.split(command), shell=True)
	except Exception as e:
		log_info ("MISC", "command error: %s" %str(e))

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
Logging 
'''
class GetLogger():
	def __init__(self, name):
		self.logger = logging.getLogger(name)
		self.logger.setLevel(logging.INFO)

		formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
		if name == "apServerLog":
			log_file = APSERVER_LOG_PATH
		else:
			log_file = APCLIENT_LOG_PATH

		#self.handler = logging.FileHandler(log_file)
		self.handler = RotatingFileHandler(log_file, mode='a', maxBytes=(5 * 1024 * 1024), backupCount=2, encoding=None, delay=0)
		self.handler.setFormatter(formatter)
		self.logger.addHandler(self.handler)


def init_log(name):
	global gLogger
	gLogger = GetLogger(name)

def get_logger_handler():
	return gLogger.handler

def log_debug(module, *values):
	if not values:
		gLogger.logger.debug('%s: Invaild log' % module)
	else:
		val_list = ' '.join(str(x) for x in values)
		gLogger.logger.debug('%s[%d]: %s' % (module, os.getpid(),  val_list))

def log_info(module, *values):
	if not values:
		gLogger.logger.info ('%s: Invaild log' % module)
	else:
		val_list = ' '.join(str(x) for x in values)
		gLogger.logger.info('%s[%d]: %s' % (module, os.getpid(), val_list))

def log_error(module, *values):
	if not values:
		gLogger.logger.error('%s: Invaild log' % module)
	else:
		val_list = ' '.join(str(x) for x in values)
		gLogger.logger.error('%s[%d]: %s' % (module, os.getpid(), val_list))

def log_warn(module, *values):
	if not values:
		gLogger.logger.warn('%s: Invaild log' % module)
	else:
		val_list = ' '.join(str(x) for x in values)
		gLogger.logger.warn('%s[%d]: %s' % (module, os.getpid(), val_list))
