import importlib
bc = importlib.import_module('BrainCell')


class Neuron(bc.BrainCell):
    def __init__(self):
        super()