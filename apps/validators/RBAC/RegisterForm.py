from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length, Regexp

from apps.exception.error_code import ParameterException
from apps.models.RBAC import Users
from apps.validators.BaseForm import BaseForm


class RegisterForm(BaseForm):
    account = StringField(validators=[Email(message="Invalid email address")])
    nickname = StringField(validators=[DataRequired(), Length(min=2, max=20)])
    telephone_number = StringField(validators=[DataRequired(), Length(min=11, max=11)])
    password = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')])
    role_id = StringField(validators=[DataRequired()])
    desc = StringField(validators=[])
    enable = StringField(validators=[], default=1)

    def validate_account(self, value):
        if Users.query.filter_by(account=value.data).first():
            raise ParameterException(msg="账户重复")

    def validate_auth(self, value):
        if value.data == 1:
            raise ParameterException(msg='注册权限错误')
