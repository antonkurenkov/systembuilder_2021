import yaml


class Manifest:
    def __init__(self, path):
        self.path = path
        self.structure
        self.cfg_keys = ['name', 'description', 'author', 'url',
                         'version', 'license', 'keywords', 'path']

    def parse(self):
        self.load_file()
        result = self.validate()
        if (result):
            return self.structure
        else:
            return None

    def load_file(self):
        with open(self.path, 'r') as stream:
            try:
                self.structure = yaml.safe_load(stream)
            except Exception as e:
                print(e)

    def validate(self):
        for key in self.structure.keys():
            if key not in self.cfg_keys:
                self.structure.pop(key)
        if len(self.structure) == len(self.cfg_keys):
            return True
        else:
            return False
