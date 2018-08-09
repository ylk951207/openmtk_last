from rest_framework.exceptions import *

class RespNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
#    default_detail = _('Not found.')

