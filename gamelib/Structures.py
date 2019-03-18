from gamelib.Immovable import Immovable

class Wall(Immovable):
    def __init__(self,**kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = '#'
        if 'name' not in kwargs.keys():
            kwargs['name'] = 'wall'
        Immovable.__init__(self,**kwargs)
    
    def pickable(self):
        return False
    
    def overlappable(self):
        return False

class GenericStructure(Immovable):
    def __init__(self,**kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = '#'
        if 'name' not in kwargs.keys():
            kwargs['name'] = 'wall'
        Immovable.__init__(self,**kwargs)
        self.__is_pickable = False
        self.__is_overlappable = False
    
    def pickable(self):
        return self.__is_pickable

    def set_pickable(self,val):
        if type(val) is bool:
            self.__is_pickable = val

    def overlappable(self):
        return self.__is_overlappable

    def set_overlappable(self,val):
        if type(val) is bool:
            self.__is_overlappable = val


class Treasure(Immovable):
    def __init__(self,**kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = '¤'
        Immovable.__init__(self,**kwargs)

    def pickable(self):
        return True
    
    def overlappable(self):
        return False
