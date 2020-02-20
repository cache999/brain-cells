from abc import ABC
import json


# here we define several base classes to be inherited from.
class BrainCell(ABC):
    # always call setup first!!!
    attributes = None
    aliases = []
    ext_name = int_name = None

    @classmethod
    def setup(cls):
        ext_name = None
        int_name = cls.__class__.__name__

        with open('./cells.json') as file:
            cfg = json.loads(file.read())
            file.close()
        attrs = cfg[cls.__class__]
        if attrs is not None:
            cls.attributes = attrs
        else:
            raise LookupError("Config for " + int_name + " not found!")

        with open('./cell_aliases.json') as file:
            cfg = json.loads(file.read())
            file.close()
        aliases = cfg[int_name]
        if aliases is not None:
            cls.aliases = aliases

    @classmethod
    def __getitem__(cls, item):
        return cls.attributes[item]

    @classmethod
    def __setitem__(cls, item, val):
        cls.attributes[item] = val
        raise Warning("Changing attributes during runtime is discouraged!")

    @classmethod
    def get_external_name(cls):
        return cls.ext_name

class Neuron(BrainCell):
    pass

class GlialCell(BrainCell):
    pass

class Structure(BrainCell):
    @classmethod
    def setup(cls):
        super().setup()
        cls.prerequisites = [] # read this from config