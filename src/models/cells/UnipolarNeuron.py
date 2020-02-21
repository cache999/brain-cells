from importlib import import_module

MODULE_PATH = 'src/models/cells'
n = import_module('BaseBrainClasses', package=MODULE_PATH)


class UnipolarNeuron(n.Neuron):
    def __init__(self):
        super()
