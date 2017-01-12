from .formatter import Formatter


class RustFormat(Formatter):
    def __init__(self):
        super().__init__(name='rust', binary='rustfmt')

    def file_args(self, file_name):
        return ['--write-mode=overwrite', file_name]
