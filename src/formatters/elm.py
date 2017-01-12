from .formatter import Formatter


class ElmFormat(Formatter):
    def __init__(self):
        super().__init__(name='elm', binary='elm-format')

    def selection_args(self):
        return ['--stdin']
