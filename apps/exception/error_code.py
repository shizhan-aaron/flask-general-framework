from apps.exception.error import APIException


class Success(APIException):
    code = 201
    error_code = 0
    msg = "it's OK"


class ParameterException(APIException):
    code = 406
    error_code = 4600
    msg = "invalid parameter"


class AuthFailed(APIException):
    code = 401
    error_code = 4100
    msg = "authorization failed"


class NotFound(APIException):
    code = 404
    error_code = 4400
    msg = "the resource are not found"


class Forbidden(APIException):
    code = 403
    error_code = 4300
    msg = "forbidden, not in scope"


class SystemException(APIException):
    code = 500
    error_code = 5000
    msg = "系统异常"
