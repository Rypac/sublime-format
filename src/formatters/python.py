from .formatter import Formatter


class PythonFormat(Formatter):
    def name(self):
        return 'python'

    def command(self):
        return [self.settings().get('binary') or 'yapf']

    def file_args(self, file_name):
        return ['--in-place', file_name]
