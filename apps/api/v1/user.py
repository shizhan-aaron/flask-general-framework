from apps.libs.red_print import Redprint

api = Redprint('user')


@api.route('/get')
def get_user():
    return 'get user'
