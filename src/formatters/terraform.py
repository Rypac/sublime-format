from ..settings import settings_for


class TerraformFormat():
    def command(self):
        binary = settings_for('terraform').get('binary') or 'terraform'
        return [binary, 'fmt']

    def selection_args(self):
        return ['-']

    def file_args(self, file_name):
        return [file_name]
