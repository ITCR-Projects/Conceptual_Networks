from abc import ABC
from File import File

class TextFile(File, ABC):
    def __init__(self, name, url_file):
        super().__init__(name, url_file)

    def get_text(self):
        pass
