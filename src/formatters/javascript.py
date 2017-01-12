from ..settings import settings, settings_for


class JavaScriptFormat():
    def command(self):
        node = settings().get('node_binary') or 'node'
        binary = settings_for('javascript').get('binary') or 'prettier'
        return [node, binary]

    def selection_args(self):
        return []

    def file_args(self, file_name):
        return ['--write', file_name]
