from ..formatter import Formatter


class JavaScriptFormat(Formatter):
    def __init__(self):
        super().__init__(name='JavaScript', source='js', binary='prettier')

    def command(self):
        return [self.settings.get('node', 'node'), self.binary]

    def selection_args(self):
        return ['--stdin']

    def file_args(self, file_name):
        return ['--write', file_name]
