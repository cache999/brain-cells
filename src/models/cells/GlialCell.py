import importlib
bc = importlib.import_module('BrainCell')


class GlialCell(bc.BrainCell):
    def __init__(self):
        super()