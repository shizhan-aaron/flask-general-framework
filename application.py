import os

from flask import Flask
from flask_script import Manager


def register_blueprint(core):
    from apps.api.v1 import create_blueprint_v1
    core.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


class Application(Flask):
    def __init__(self, import_name):
        super(Application, self).__init__(import_name)
        self.config.from_pyfile('config/base_setting.py')
        if 'ops_config' in os.environ:
            self.config.from_pyfile('config/%s_setting.py' % os.environ['ops_config'])

        register_blueprint(self)


app = Application(__name__)
manager = Manager(app=app)
