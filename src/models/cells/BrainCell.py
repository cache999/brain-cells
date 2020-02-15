from abc import ABC
import json


class BrainCell(ABC):

    def __init__(self):
        self.class_name = __class__.__name__
        self.load_from_config()

    def load_from_config(self, config_name):
        with open('./cells.json') as file:
            cfg = json.loads(file.read())
            file.close()
        attrs = cfg[config_name]
        if attrs is not None:
            self.attributes = attrs
        else:
            raise LookupError("Config for " + config_name + " not found!")

        with open('./cell_aliases.json') as file:
            cfg = json.loads(file.read())
            file.close()
        aliases = cfg[config_name]
        if aliases is not None:
            self.aliases = aliases
        else:
            self.alaises = []

    def __getitem__(self, item):
        return self.attributes[item]

    def __setitem__(self, item, val):
        self.attributes[item] = val
        raise Warning("Changing attributes during runtime is discouraged!")
