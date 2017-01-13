from ..formatter import Formatter


class GoFormat(Formatter):
    def __init__(self):
        super().__init__(name='Go', binary='gofmt')

    def file_args(self, file_name):
        return ['-w', file_name]
