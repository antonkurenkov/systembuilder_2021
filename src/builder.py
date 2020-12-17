import subprocess
import os.path
import json
import time

from manifest import Manifest


class Builder:

    # def __init__(self, path):
    #     self.path = path
    #     self.collection = []
    #     self.file_name = 'manifest.yml'
    #
    #     self.status_map = None
    #
    # def parse(self):
    #     for path, directories, files in os.walk(self.path):
    #         if self.file_name in files:
    #             self.collection.append(os.path.join(path, self.file_name))
    #
    #     return self.collection
    #
    # def update_status(self):
    #     pass
    #
    # def build(self):
    #     try:
    #         self.update_status()
    #         subprocess.run(['docker', 'buildx', 'build', self.path])
    #     except Exception as error:
    #         return error

    def __init__(self, path):
        self.path = path
        self.collection = []
        self.file_name = 'manifest.yml'
        self.status_map = {}

        with open("README.md") as file:
            self.version = float(file.read().split("\n")[1].split(' ')[-1])

    def parse(self):
        for path, directories, files in os.walk(self.path):
            if self.file_name in files:
                self.collection.append(os.path.join(path, self.file_name))
        self.collection.sort()

        pretty_names = [i.split('/')[-2] for i in self.collection]
        print(f'COLLECTION CONTAINS {pretty_names}')

        # return self.collection

    def build(self):
        default_work_dir = os.getcwd()
        building_time = time.asctime()
        self.status_map[building_time] = {}

        for project in self.collection:

            data = {
                'name': project.split('/')[-2],
                'building_time': building_time,
            }

            try:
                print(f'PARSING {data["name"]}')
                m = Manifest(project)
                project_map = m.parse()
                os.putenv('DOCKER_CLI_EXPERIMENTAL', 'enabled')
                project_dir = os.path.dirname(project)

                print(f'BUILDING {data["name"]}')
                os.chdir(project_dir)
                subprocess.check_call(['docker', 'buildx', 'build', project_map['path']])
                os.chdir(default_work_dir)

                data['status'] = True
                data['message'] = None
            except Exception as e:
                data['status'] = False
                data['message'] = str(e)

            self.update_status(data)

    def update_status(self, data):

        building_time = data['building_time']
        project_name = data['name']

        self.status_map[building_time][project_name] = {
            "builder_release": self.version,
            "status": data['status'],
            "message": data['message']
        }

        with open("status.json", "w+") as file:
            json.dump(self.status_map, file)



        # building_time = time.asctime()
        # # Время сборки
        # self.status_map[building_time] = {}
        # for file in self.collection:
        #     if file not in self.status_map[building_time].keys():
        #         if self.build() == "sucess":
        #             self.status_map[building_time][file] = {"builder_release": version, "status": True, "message": "null"}
        #         else:
        #             self.status_map[building_time][file] = {"builder_release": version, "status": False, "message": self.build()}
        #         print(self.status_map)
        #     with open("status.json", "w") as json_obj:
        #         json.dump(self.status_map, json_obj)




collection_path = '/home/runner/work/systembuilder_2021/systembuilder_2021/repo/collection/'
b = Builder(collection_path)
b.parse()  # get the collection
b.build()  # build element