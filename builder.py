import subprocess
import os.path
import json
import time


class Builder:

    def __init__(self, path):
        self.path = path
        self.collection = []
        self.file_name = 'manifest.yml'
        self.status_map = {}

    def parse(self):
        for path, directories, files in os.walk(self.path):
            if self.file_name in files:
                self.collection.append(os.path.join(path, self.file_name))

        return self.collection

    def build(self):
        try:
            self.update_status()
            subprocess.run(['docker', 'buildx', 'build', self.path])
            return "sucess"
        except Exception as error:
            return error

    def update_status(self):
        with open("README.md") as f_obj:
            version = (f_obj.readline().rstrip().split(" "))[2][2:]
        building_time = time.asctime()
        # Время сборки
        self.status_map[building_time] = {}
        for file in self.collection:
            if file not in self.status_map[building_time].keys():
                if self.build() == "sucess":
                    self.status_map[building_time][file] = {"builder_release": version, "status": True, "message": "null"}
                else:
                    self.status_map[building_time][file] = {"builder_release": version, "status": False, "message": self.build()}
                print(self.status_map)
            with open("status.json", "w") as json_obj:
                json.dump(self.status_map, json_obj)
 
