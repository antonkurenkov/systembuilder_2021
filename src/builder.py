import os.path


class Builder:
    def __init__(self, path):
        self.path = path
        self.collection = []
        self.file = 'manifest.yml'

    def parse(self):
        for root, dirs, files in os.walk(self.path):
            if self.file in files:
                self.collection.append(os.abspath.join(self.dirs))

        return self.collection
