from wtforms import StringField
from wtforms.validators import DataRequired

from apps.validators.BaseForm import BaseForm


class DistributePermissionForm(BaseForm):
    permissions = StringField(validators=[DataRequired()])
