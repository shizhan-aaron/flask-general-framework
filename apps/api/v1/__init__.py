from flask import Blueprint
from apps.api.v1.authorization import user
from apps.api.v1.authorization import permission
from apps.api.v1.authorization import role


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    user.api.register(bp_v1)
    permission.api.register(bp_v1)
    role.api.register(bp_v1)
    return bp_v1
