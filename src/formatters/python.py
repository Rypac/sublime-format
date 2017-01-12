from ..settings import settings_for


class PythonFormat():
    def command(self):
        return [settings_for('python').get('binary') or 'yapf']

    def selection_args(self):
        return []

    def file_args(self, file_name):
        return ['--in-place', file_name]
