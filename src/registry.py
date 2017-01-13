from .formatters.elm import ElmFormat
from .formatters.go import GoFormat
from .formatters.javascript import JavaScriptFormat
from .formatters.python import PythonFormat
from .formatters.rust import RustFormat
from .formatters.terraform import TerraformFormat

registered_formatters = [
    ElmFormat(),
    GoFormat(),
    JavaScriptFormat(),
    PythonFormat(),
    RustFormat(),
    TerraformFormat()
]


def source_file(view):
    scope = view.scope_name(0) or ''
    return next(iter(scope.split(' ')))


def formatter_for(view):
    source = source_file(view)
    return next((x for x in registered_formatters if x.source == source), None)


def formatter_named(name):
    return next((x for x in registered_formatters if x.name == name), None)


def formatters():
    return registered_formatters
