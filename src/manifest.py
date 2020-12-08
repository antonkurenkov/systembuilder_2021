import yaml


class Manifest:
    def __init__(self, path):
        self.path = path
        self.cfg_keys = ['name', 'description', 'author', 'url',
                         'version', 'license', 'keywords', 'path']

    def parse(self):
        structure = self.load_file()
        return self.validate(structure)

    def load_file(self):
        try:
            with open(self.path) as f_obj:
                data = yaml.safe_load(f_obj)
        except FileNotFoundError:
            print("Не удается найти указанный файл")
            return None
        except Exception as e:
            print(e)
        else:
            return data

    def validate(self, data):
        if data:
            try:
                dict_data = dict(data)
                for key in dict_data.keys():
                    if key not in self.cfg_keys:
                        del data[key]
                if len(data) == len(self.cfg_keys):
                    return data
                else:
                    return None
            except Exception as e:
                print(e)
        else:
            return None 
