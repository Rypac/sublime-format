from .formatter import Formatter


class RustFormat(Formatter):
    def name(self):
        return 'rust'

    def command(self):
        return [self.settings().get('binary') or 'rustfmt']

    def file_args(self, file_name):
        return ['--write-mode=overwrite', file_name]
