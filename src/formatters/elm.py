from ..settings import settings_for


class ElmFormat():
    def command(self):
        return [settings_for('elm').get('binary') or 'elm-format']

    def selection_args(self):
        return ['--stdin']

    def file_args(self, file_name):
        return [file_name]
