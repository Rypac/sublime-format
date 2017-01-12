from ..settings import settings


class Formatter():
    def name(self):
        return ''

    def settings(self):
        return settings().get(self.name(), {})

    def command(self):
        return []

    def selection_args(self):
        return []

    def file_args(self, file_name):
        return []
