import os
import sys
from apNotifier.notifier import *
from common.log import *


'''
Main Routine
'''
init_log("apNotifierLog")

pid = str(os.getpid())
pidfile = "/var/run/apnotifier.pid"
file(pidfile, 'w').write(pid)

notifier = NotifierCmdApp()
notifier.run()
