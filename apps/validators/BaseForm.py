from flask import request
from wtforms import Form
from apps.exception.error_code import ParameterException
from apps.libs.common.conversion import recursion_hump_to_underline


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = recursion_hump_to_underline(request.args.to_dict())
        data_to_hump = recursion_hump_to_underline(data)
        super(BaseForm, self).__init__(data=data_to_hump, **args)

    def validate_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=str(self.errors))
        return self
