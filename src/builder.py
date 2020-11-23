import os.path

class Builder:

    def __init__(self, path):
        self.path = path
        self.collection = []
        self.file_name = 'manifest.yml'

    def parse(self):
        for path, directories, files in os.walk(self.path):
            if self.file_name in files:
                self.collection.append(os.path.join(path, self.file_name))

        return self.collection

    def build(self):
        pass