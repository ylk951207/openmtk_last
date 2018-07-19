import os, sys
import logging
from common.env import *

class GetLogger():
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        if name == "apServerLog":
            log_file = APSERVER_LOG_PATH
        else:
            log_file = APCLIENT_LOG_PATH

        self.handler = logging.FileHandler(log_file)
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
        gLogger.logger.debug('%s: %s' % (module, val_list))

def log_info(module, *values):
    if not values:
        gLogger.logger.info ('%s: Invaild log' % module)
    else:
        val_list = ' '.join(str(x) for x in values)
        gLogger.logger.info('%s: %s' % (module, val_list))

def log_err(module, *values):
    if not values:
        gLogger.logger.error('%s: Invaild log' % module)
    else:
        val_list = ' '.join(str(x) for x in values)
        gLogger.logger.error('%s: %s' % (module, val_list))

def log_warn(module, *values):
    if not values:
        gLogger.logger.warn('%s: Invaild log' % module)
    else:
        val_list = ' '.join(str(x) for x in values)
        gLogger.logger.warn('%s: %s' % (module, val_list))
