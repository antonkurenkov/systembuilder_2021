import yaml


class Manifest:

    # структура конфигурационного файла manifest.yml
    keywords = ['name', 'description', 'author', 'url', 'version', 'license', 'keywords', 'path']

    def __init__(self, path):
        self.path = path

    def validate(self):
        with open(self.path) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        # с помощью dict создаю копию словаря
        data_dict = dict(data)
        for key in data.keys():
            if key not in self.keywords:
                del data_dict[key]
        if len(data_dict) == len(self.keywords):
            return data_dict
        else:
            return None
