import os.path
import json
import subprocess


class Builder:
    def __init__(self, path):
        self.path = path
        self.collection = []
        self.file = 'manifest.yml'
        self.status_map = []

    def parse(self):
        for root, dirs, files in os.walk(self.path):
            if self.file in files:
                self.collection.append(os.abspath.join(self.dirs))

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
            self.update_status()
            subprocess.run(['docker', 'buildx', 'build', self.path])
        except Exception as error:
            return error

