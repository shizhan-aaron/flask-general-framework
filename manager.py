from flask_script import Server

from application import manager, app


manager.add_command('runserver', Server(host='0.0.0.0', use_reloader=True, use_debugger=True))

if __name__ == '__main__':
    manager.run()
