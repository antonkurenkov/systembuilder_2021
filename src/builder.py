import os


class Builder:
    def __init__(self, path):
        self.collection = []
        self.path = path
        self.file = 'manifest.yaml'

    def parse(self):
        for root, dirs, files in os.walk(self.path):
            if files == self.file:
                self.collection.append(os.path.abspath(dirs))
        return self.collection
