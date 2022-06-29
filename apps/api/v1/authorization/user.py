import datetime

from flask import current_app, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from apps.exception.error_code import Success, ParameterException
from apps.libs.common.jsonify import jsonify
from apps.libs.common.red_print import Redprint
from apps.libs.common.token_auth import verity_auth_token
from apps.models.authorization import User, Role, MenuPermission, FunctionalPermission, RoleToPermission
from apps.models.base import db
from apps.validators.PageForm import PageForm
from apps.validators.authorization.LoginForm import LoginForm
from apps.validators.authorization.PutRoleForm import PutRoleForm
from apps.validators.authorization.RegisterForm import RegisterForm

api = Redprint('user')


@api.route('/register', methods=["POST"])
def register():
    form = RegisterForm().validate_api()
    with db.auto_commit():
        user = User()
        user.account = form.account.data
        user.password = form.password.data
        user.nickname = form.nickname.data
        user.telephone_number = form.telephone_number.data
        user.role_id = form.role_id.data
        if form.desc.data:
            user.remarks = form.desc.data
        user.enable = int(form.enable.data)
        db.session.add(user)
    return Success()


@api.route("/token", methods=["POST"])
def get_token():
    form = LoginForm().validate_api()
    identity = User.verity(form.account.data, form.password.data)
    expiration = current_app.config["TOKEN_EXPIRATION"]

    with db.auto_commit():
        user = User.query.filter_by(id=identity["uid"]).first()
        user.last_login = int(datetime.datetime.now().timestamp())

    token = generate_auth_token(identity["uid"], expiration)
    t = {
        "token": token.decode("ascii"),
    }
    return jsonify(t), 201


def generate_auth_token(uid, expiration=3600):
    s = Serializer(secret_key=current_app.config["SECRET_KEY"],
                   expires_in=expiration)
    return s.dumps({
        "uid": uid
    })


@api.route("/profile")
def get_user_info():
    authorization = request.headers.get('Authorization')
    if not authorization:
        raise ParameterException(msg='未获取到token值')
    token = authorization.split(" ")[1]

    # 获取用户信息
    uid = verity_auth_token(token)
    user = User.query.filter_by(id=uid).first()

    # 获得角色信息
    role_id = user.role_id
    role = Role.query.filter_by(id=role_id).first()
    role.hide('desc')

    # 获取权限信息
    permission = {
        'menus': [],
        'functional': []
    }
    # role_to_permission = RoleToPermission.query.filter_by(role_id=role_id).first()
    # if not role_to_permission:
    #     raise ParameterException(msg='未获取到权限信息')
    # permissions = role_to_permission.permission_list
    # permission_list = permissions.split(',')
    # for item in permission_list:
    #     if '-' in item:
    #         permission_id = item.split('-')[1]
    #         functional = FunctionalPermission.query.filter_by(id=permission_id).first()
    #         permission['functional'].append(functional.mark)
    #     else:
    #         menu = MenuPermission.query.filter_by(id=item).first()
    #         permission['menus'].append(menu.mark)

    # 拼接结果
    result = {
        'role': role,
        'permission': permission
    }
    return jsonify(result)


@api.route('/list')
def user_list():
    form = PageForm().validate_api()
    result = {
        'list': [],
        'total': User.query.filter_by().count()
    }
    users = User.query.filter_by().paginate(page=form.page.data, per_page=form.per_page.data).items
    for user in users:
        user_info = {
            'id': user.id,
            'account': user.account,
            'nickname': user.nickname,
            'role': user.role,
            'telephone_number': user.telephone_number,
            'create_time': user.create_time_format
        }
        result['list'].append(user_info)
    return jsonify(result)


@api.route('/<int:uid>/role', methods=['GET', 'PUT'])
def get_user_role(uid):
    if request.method == 'GET':
        # 获取指定用户角色
        user = User.query.filter_by(id=uid).first()
        return jsonify(user.role)
    if request.method == 'PUT':
        # 为用户分配角色
        form = PutRoleForm().validate_api()
        with db.auto_commit():
            user = User.query.filter_by(id=uid).first()
            user.role_id = form.id.data
            user.update_time = int(datetime.datetime.now().timestamp())
        return Success()
