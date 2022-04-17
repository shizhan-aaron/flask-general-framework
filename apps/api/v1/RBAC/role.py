from flask import request

from apps.exception.error_code import Success
from apps.libs.common.jsonify import jsonify
from apps.libs.common.red_print import Redprint
from apps.models.RBAC import Role, RoleToPermission
from apps.models.base import db
from apps.validators.RBAC.DistributePermissionForm import DistributePermissionForm

api = Redprint('role')


@api.route('/', methods=['POST'])
def add_role():
    return Success()


@api.route('/list')
def role_list():
    roles = Role.query.filter_by().all()
    return jsonify(roles)


@api.route('/<int:role_id>/permission', methods=['GET', 'PUT'])
def get_role_permission(role_id):
    if request.method == 'GET':
        role_2_permission = RoleToPermission.query.filter_by(role_id=role_id).first()
        result = role_2_permission.permission_list.split(',')
        return jsonify(result)
    if request.method == 'PUT':
        form = DistributePermissionForm().validate_api()
        with db.auto_commit():
            role = RoleToPermission.query.filter_by(role_id=role_id).first()
            role.permission_list = form.permissions.data
        return Success()
