import importlib
Brain = importlib.import_module('Brain')
Inventory = importlib.import_module('Inventory')
config = importlib.import_module('config')


class Player:
    '''
    Basic player class that will be used to represent any single discord user.
    '''
    def __init__(self, uid):
        self.uid = uid
        self.brain = Brain.Brain()
        self.inventory = Inventory.Inventory()