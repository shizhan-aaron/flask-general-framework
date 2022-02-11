# from collections import namedtuple

from flask import current_app, g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from apps.exception.error_code import AuthFailed

auth = HTTPBasicAuth()


def verity_token(account, password):
    user_info = verity_auth_token(account)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True


def verity_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=4102)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=4103)
    uid = data['uid']
    return uid
