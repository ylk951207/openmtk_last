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
        log_info(LOG_MODULE_RESPONSE, "Set Response = ", str(self.response))

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
        log_info(LOG_MODULE_RESPONSE, "Response Body = ", str(body_data))
        return body_data

def response_make_simple_success_body():
    response = APgentResponseMessgae()
    response.set_response_value(200, "Successful", True)
    data = response.make_response_body(None)
    return data
