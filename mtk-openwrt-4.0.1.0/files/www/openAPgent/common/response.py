from rest_framework.exceptions import *
from common.log import *
from common.env import *

class RespNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
#    default_detail = _('Not found.')


class APgentResponseMessgae(object):
    def __init__(self):
        self.response = dict()

    def set_response_value(self, status_code, response_msg, is_successful):
        if status_code != 200:
            response = response_msg.response
            try:
                explanation = response.json()['message']
            except ValueError:
                explanation = (response.content or '').strip()
        else:
            explanation = response_msg

        self.response['status_code'] = status_code
        self.response['error_msg'] = explanation
        self.response['isSuccessful'] = is_successful
        log_debug(LOG_MODULE_RESPONSE, "Set Response = ", str(self.response))

        return self.response

    @property
    def status_code(self):
        return self.response['status_code']

    @property
    def error_msg(self):
        return self.response['error_msg']

    @property
    def is_successful(self):
        return self.response['isSuccessful']

    def make_response_body(self, body_data):
        if not body_data:
            body_data = dict()

        body_data['header'] =  {
            'resultCode': self.status_code,
            'resultMessage': self.error_msg,
            'isSuccessful': self.is_successful
        }
        log_debug(LOG_MODULE_RESPONSE, "Response Body = ", str(body_data))
        return body_data

def response_make_simple_success_body(body_data):
    resp_msg = APgentResponseMessgae()
    resp_msg.set_response_value(200, "Successful", True)
    data = resp_msg.make_response_body(body_data)
    return data

def response_make_simple_error_body(status_code, msg, body_data):
    resp_msg = APgentResponseMessgae()

    resp_msg.response['status_code'] = status_code
    resp_msg.response['error_msg'] = msg
    resp_msg.response['isSuccessful'] = False

    data = resp_msg.make_response_body(body_data)
    return data