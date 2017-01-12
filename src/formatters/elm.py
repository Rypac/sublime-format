from .formatter import Formatter


class ElmFormat(Formatter):
    def name(self):
        return 'elm'

    def command(self):
        return [self.settings().get('binary') or 'elm-format']

    def selection_args(self):
        return ['--stdin']

    def file_args(self, file_name):
        return [file_name]
