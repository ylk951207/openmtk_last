import fileinput
from common.env import *
from common.log import *
from common.request import *
from common.response import *

def py_provisioning_done_create(request):
    '''
    TODO: Celery Tasks
    '''

    noti_data = dict()
    noti_data['config_file'] = "all"
    server_msg = ApServerLocalMassage(APNOTIFIER_CMD_PORT)
    server_msg.send_message_to_apnotifier("PUCI", SAL_PUCI_MODULE_RESTART, noti_data)

    return response_make_simple_success_body()

