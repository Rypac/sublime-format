from ..formatter import Formatter


class PythonFormat(Formatter):
    def __init__(self):
        super().__init__(name='Python', binary='yapf')

    def file_args(self, file_name):
        return ['--in-place', file_name]
