import yaml


class Manifest:

    # структура конфигурационного файла manifest.yml
    structure = ['name', 'description', 'author', 'url', 'version', 'license', 'keywords', 'path']

    def __init__(self, path):
        self.path = path

    def load_file(self, file):
        return yaml.safe_load(file)

    def validate(self):
        with open(self.path) as file_obj:
            try:
                data = self.load_file(file_obj)
                # с помощью dict создаю копию словаря
                data_dict = dict(data)
                for key in data.keys():
                    if key not in self.structure:
                        del data_dict[key]
                if len(data_dict) == len(self.structure):
                    return data_dict
                else:
                    return None
            except yaml.YAMLError as exclusion:
                print(exclusion)
