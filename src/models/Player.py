from importlib import import_module

MODULE_PATH = 'src/models'
Brain = import_module('.Brain', package=MODULE_PATH)
Inventory = import_module('.Inventory', package=MODULE_PATH)
config = import_module('.config', package='src')


class Player:
    '''
    Basic player class that will be used to represent any single discord user.
    '''
    def __init__(self, uid):
        self.uid = uid
        self.brain = Brain.Brain()
        self.inventory = Inventory.Inventory()