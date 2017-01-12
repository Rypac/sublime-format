from ..settings import settings_for


class RustFormat():
    def command(self):
        return [settings_for('rust').get('binary') or 'rustfmt']

    def selection_args(self):
        return []

    def file_args(self, file_name):
        return ['--write-mode=overwrite', file_name]
