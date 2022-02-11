import os

from flask import Flask
from flask.json import JSONEncoder as _JSONEncoder
from flask_script import Manager

from apps.exception.error import APIException, HTTPException
from apps.models.base import db


def register_blueprint(core):
    from apps.api.v1 import create_blueprint_v1
    core.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            new_dict = dict(o)
            return new_dict
        raise APIException(error_code=5008)


class Application(Flask):
    def __init__(self, import_name):
        super(Application, self).__init__(import_name)
        self.config.from_pyfile('config/base_setting.py')
        if 'ops_config' in os.environ:
            self.config.from_pyfile('config/%s_setting.py' % os.environ['ops_config'])

        # 注册蓝图
        register_blueprint(self)

        # 注册模型
        db.init_app(self)
        db.create_all(app=self)

    json_encoder = JSONEncoder


app = Application(__name__)
manager = Manager(app=app)


@app.errorhandler(Exception)
def frames_work_error(e):
    if isinstance(e, APIException):
        return e
    elif isinstance(e, HTTPException):
        code = e.code
        error_code = 1007
        msg = e.description
        return APIException(code=code, error_code=error_code, msg=msg)
    else:
        # 调试模式
        if not app.config['DEBUG']:
            return APIException()
        else:
            return e
