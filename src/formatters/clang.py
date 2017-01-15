from ..formatter import Formatter


class ClangFormat(Formatter):
    def __init__(self):
        super().__init__(name='Clang', source='c++', binary='clang-format')

    def file_args(self, file_name):
        return ['-i', file_name]
