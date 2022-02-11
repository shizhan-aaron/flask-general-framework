from wtforms import IntegerField
from wtforms.validators import DataRequired

from apps.validators.BaseForm import BaseForm


class PageForm(BaseForm):
    page = IntegerField(validators=[DataRequired()])
    per_page = IntegerField(validators=[DataRequired()])
