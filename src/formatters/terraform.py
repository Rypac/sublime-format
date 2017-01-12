from .formatter import Formatter


class TerraformFormat(Formatter):
    def name(self):
        return 'terraform'

    def command(self):
        binary = self.settings().get('binary') or 'terraform'
        return [binary, 'fmt']

    def selection_args(self):
        return ['-']

    def file_args(self, file_name):
        return [file_name]
