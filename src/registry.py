from .formatters.javascript import JavaScriptFormat
from .formatters.rust import RustFormat
from .formatters.terraform import TerraformFormat

formatters = {
    'source.js': JavaScriptFormat(),
    'source.rust': RustFormat(),
    'source.terraform': TerraformFormat()
}


def source_file(view):
    scope = view.scope_name(0) or ''
    scopes = scope.split(' ')
    return next(iter(scopes)) if scopes else None


def has_formatter(view):
    return formatters.get(source_file(view)) is not None


def formatter_for(view):
    return formatters.get(source_file(view))
