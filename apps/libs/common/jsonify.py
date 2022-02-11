from flask import current_app
from flask.json import dumps

from apps.libs.common.conversion import recursion_underline_to_hump


def jsonify(*args, **kwargs):
    indent = None
    separators = (",", ":")

    if current_app.config["JSONIFY_PRETTYPRINT_REGULAR"] or current_app.debug:
        indent = 2
        separators = (", ", ": ")

    if args and kwargs:
        raise TypeError("jsonify() behavior undefined when passed both args and kwargs")
    elif len(args) == 1:  # single args are passed directly to dumps()
        data = recursion_underline_to_hump(args[0])
    else:
        data = args or kwargs

    return current_app.response_class(
        dumps(data, indent=indent, separators=separators) + "\n",
        mimetype=current_app.config["JSONIFY_MIMETYPE"],
    )
