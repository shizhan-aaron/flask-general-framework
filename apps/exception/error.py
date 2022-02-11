from werkzeug.exceptions import HTTPException
from flask import request, json


class APIException(HTTPException):
    code = 500
    error_code = 999
    msg = 'sorry, we make a mistake'
    data = None

    def __init__(self, code=None, error_code=None, msg=None, data=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        if data:
            self.data = data
        super(APIException, self).__init__(description=msg, response=None)

    def get_body(self, environ=None):
        body = dict(
            error_code=self.error_code,
            request=request.method + " " + self.get_url_param(),
            msg=self.msg,
            data=self.data
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [("Content-type", "application/json")]

    @staticmethod
    def get_url_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
