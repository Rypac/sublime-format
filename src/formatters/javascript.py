from .formatter import Formatter


class JavaScriptFormat(Formatter):
    def name(self):
        return 'javascript'

    def command(self):
        node = self.settings().get('node') or 'node'
        binary = self.settings().get('binary') or 'prettier'
        return [node, binary]

    def file_args(self, file_name):
        return ['--write', file_name]
