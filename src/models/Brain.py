import importlib
config = importlib.import_module('config')


class Brain(object):
    def __init__(self):
        # setup basic brain with 100% structural stability
        self.cells = {
            "NeuronUnipolar": 1,
            "GliaRadial": config.structural_int_load_ratio
        }
        self.total_cells = 1 + config.structural_int_load_ratio
        self.type_counts = {
            "Neuron": 1,
            "Glia": config.structural_int_load_ratio
        }