import yaml

class Manifest:
    def __init__ (self, path):
        self.path = path

    cfg_keys = ['name', 'description', 'author', 'url',
                'version', 'license', 'keywords', 'path']

    def __init__(self, path):
        self.path = path

    def parse(self):
        pass

    def load_file(self, file):
        return yaml.safe_load(file)

    def validate(self):
        with open(self.path, 'r') as stream:
            try:
                data = self.load_file(stream)
                for key in data.keys():
                    if key not in self.cfg_keys:
                        del data[key]
                if len(data) == len(self.cfg_keys):
                    return data
                else:
                    return None
            except yaml.YAMLError as ex:
                print(ex)
