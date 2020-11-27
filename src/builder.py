import subprocess
import os.path


class Builder:

    def __init__(self, path):
        self.path = path
        self.collection = []
        self.file_name = 'manifest.yml'
        self.status_map = None

    def parse(self):
        for path, directories, files in os.walk(self.path):
            if self.file_name in files:
                self.collection.append(os.path.join(path, self.file_name))

        return self.collection

    def update_status(self):
        pass

    def build(self):
        try:
            self.update_status()
            subprocess.run(['docker', 'buildx', 'build', self.path])
        except Exception as error:
            return error



