from wtforms import StringField
from wtforms.validators import Email, DataRequired, Regexp

from apps.validators.BaseForm import BaseForm


class LoginForm(BaseForm):
    account = StringField(validators=[Email(message="Invalid email address")])
    password = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')])
