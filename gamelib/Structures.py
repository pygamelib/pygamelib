from gamelib.Immovable import Immovable, Actionnable

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

class GenericActionnableStructure(GenericStructure,Actionnable):
    def __init__(self,**kwargs):
        GenericStructure.__init__(self,**kwargs)
        Actionnable.__init__(self,**kwargs)


class Treasure(Immovable):
    def __init__(self,**kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = '¤'
        Immovable.__init__(self,**kwargs)
        if 'value' not in kwargs.keys():
            self.value = 10
        else:
            self.value = kwargs['value']
        if 'size' not in kwargs.keys():
            self._size = 1
        else:
            self._size = kwargs['value']

    def pickable(self):
        return True
    
    def overlappable(self):
        return False
    
    def size(self):
        return self._size
