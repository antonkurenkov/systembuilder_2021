import yaml


class Manifest:

    def parse(self):
        pass

    def load_file(self):
        return yaml.safe_load(self.path)
