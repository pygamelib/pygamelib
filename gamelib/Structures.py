from gamelib.Immovable import Immovable

class Wall(Immovable):
    def __init__(self,**kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = '#'
        Immovable.__init__(self,**kwargs)


class Treasure(Immovable):
    def __init__(self,**kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = '¤'
        Immovable.__init__(self,**kwargs)
