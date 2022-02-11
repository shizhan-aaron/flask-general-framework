from flask_script import Server
from flask_cors import *

from application import manager, app


manager.add_command('runserver', Server(port=5100, host='0.0.0.0', use_reloader=True, use_debugger=True))
CORS(app=app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    manager.run()
