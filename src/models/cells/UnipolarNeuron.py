import importlib
n = importlib.import_module('Neuron')


class UnipolarNeuron(n.Neuron):
    def __init__(self):
        super()