from wtforms import IntegerField
from wtforms.validators import DataRequired

from apps.validators.BaseForm import BaseForm


class PutRoleForm(BaseForm):
    id = IntegerField(validators=[DataRequired()])
