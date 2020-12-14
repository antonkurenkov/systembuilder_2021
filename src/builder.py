import subprocess
import os.path
import json
from manifest import Manifest


class Builder:

    def __init__(self, path):
        self.path = path
        self.collection = []
        self.file_name = 'manifest.yml'
        self.status_map = None

    def run(self):
        self.parse()
        for element in self.collection:
            man = Manifest(element)
            # returns dict
            man.parse()
            # build includes update status
            self.build()

    def parse(self):
        for path, directories, files in os.walk(self.path):
            if self.file_name in files:
                self.collection.append(os.path.join(path, self.file_name))

        return self.collection

    def update_status(self):
        try:
            with open("status (2).json", 'r') as status_file:
                data_status = json.load(status_file)
                for data in data_status.keys():
                    self.status_map.append(data)
                    for name in data_status[data].keys():
                        self.status_map.append(name)
                        for sym in data_status[data][name].keys():
                            if sym == 'status':
                                status = data_status[data][name][sym]
                                self.status_map.append(status)
            with open("README.md", 'r') as file:
                for line in file:
                    if 'v.' in line:
                        version = eval(line[2:])
                        self.status_map.append(version)
            return self.status_map
        except Exception as error:
            return error

    def build(self):
        try:
            subprocess.run(['docker', 'buildx', 'build', self.path])
            self.update_status()
        except Exception as error:
            return error


if __name__ == "__main__":
    builder = Builder(".")
    builder.run()
