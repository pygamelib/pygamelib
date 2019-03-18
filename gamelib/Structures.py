from gamelib.Immovable import Immovable

class Wall(Immovable):
    def __init__(self,**kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = '#'
        Immovable.__init__(self,**kwargs)
    
    def pickable(self):
        return False
    
    def overlappable(self):
        return False


class Treasure(Immovable):
    def __init__(self,**kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = '¤'
        Immovable.__init__(self,**kwargs)

    def pickable(self):
        return True
    
    def overlappable(self):
        return False
