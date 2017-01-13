from ..formatter import Formatter


class TerraformFormat(Formatter):
    def __init__(self):
        super().__init__(name='Terraform', binary='terraform')

    def command(self):
        return [self.binary, 'fmt']

    def selection_args(self):
        return ['-']
