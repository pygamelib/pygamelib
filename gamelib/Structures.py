from gamelib.Immovable import Immovable, Actionnable
from gamelib.HacExceptions import HacInvalidTypeException

class Wall(Immovable):
    """
    A Wall is a specialized :class:`~gamelib.Immovable.Immovable` object that as unmodifiable characteristics:
        * It is not pickable (and cannot be).
        * It is not overlappable (and cannot be).
        * It is not restorable (and cannot be).
    
    As such it's an object that cannot be moved, cannot be picked up or modified by Player or NPC and block their ways. It is therefor advised to create one per board and reuse it in many places.

    :param model: The representation of the Wall on the Board.
    :type model: str
    :param name: The name of the Wall.
    :type name: str
    :param size: The size of the Wall. This parameter will probably be depracated as size is only used for pickable objects.
    :type size: int
    """
    def __init__(self,**kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = '#'
        if 'name' not in kwargs.keys():
            kwargs['name'] = 'wall'
        if 'size' not in kwargs.keys():
            kwargs['size'] = 1
        Immovable.__init__(self,**kwargs)
    
    def pickable(self):
        """ This represent the capacity for a :class:`~gamelib.BoardItem.BoardItem` to be pick-up by player or NPC.

        :return: False
        :rtype: bool
        
        Example::
        
            if mywall.pickable():
                print('Whoaa this wall is really light... and small...')
            else:
                print('Really? Trying to pick-up a wall?')
        """
        return False
    
    def overlappable(self):
        """ This represent the capacity for a :class:`~gamelib.BoardItem.BoardItem` to be overlapped by player or NPC.

        :return: False
        :rtype: bool
        """
        return False
    
    def restorable(self):
        """ 
        This represent the capacity for an :class:`~gamelib.Immovable.Immovable` :class:`~gamelib.BoardItem.BoardItem` (in this case a Wall item) to be restored by the board if the item is overlappable and has been overlapped by another :class:`~gamelib.Movable.Movable` item.
        A wall is not overlappable.
        
        :return: False
        :rtype: bool
        """
        return False

class GenericStructure(Immovable):
    """
    A GenericStructure is as the name suggest, a generic object to create all kind of structures.

    It can be tweaked with all the properties of :class:`~gamelib.BoardItem.BoardItem`, :class:`~gamelib.Immovable.Immovable` and it can be made pickable, overlappable or restorable or any combination of these.

    If you need an action to be done when a Player and/or a NPC touch the structure please have a look at :class:`gamelib.Structures.GenericActionnableStructure`.

    :param pickable: Define if the structure can be picked-up by a Player or NPC.
    :type pickable: bool
    :param overlappable: Define if the structure can be overlapped by a Player or NPC.
    :type overlappable: bool
    :param restorable: Define if the structure can be restored by the Board after a Player or NPC passed through. For example, you want a door or an activator structure (see GenericActionnableStructure for that) to remain on the board after it's been overlapped by a player. But you could also want to develop some kind of Space Invaders game were the protection block are overlappable but not restorable.
    :type restorable: bool

    On top of these, this object takes all parameters of :class:`~gamelib.BoardItem.BoardItem` and :class:`~gamelib.Immovable.Immovable`

    .. important:: If you need a structure with a permission system please have a look at :class:`~gamelib.Structures.GenericActionnableStructure`. This class has a permission system for activation.

    """
    def __init__(self,**kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = '#'
        if 'name' not in kwargs.keys():
            kwargs['name'] = 'structure'
        Immovable.__init__(self,**kwargs)
        if 'value' not in kwargs.keys():
            self.value = 0
        else:
            self.value = kwargs['value']
        if 'pickable' in kwargs.keys():
            self.__is_pickable = kwargs['pickable']
        else:
            self.__is_pickable = False
        if 'overlappable' in kwargs.keys():
            self.__is_overlappable = kwargs['overlappable']
        else:
            self.__is_overlappable = False
        
        if 'restorable' in kwargs.keys():
            self.__is_restorable = kwargs['restorable']
        else:
            self.__is_restorable = False
    
    def pickable(self):
        """ This represent the capacity for a BoardItem to be picked-up by player or NPC.

        To set this value please use :meth:`~gamelib.Structures.GenericStructure.set_pickable`

        :return: True or False
        :rtype: bool
        """
        return self.__is_pickable

    def set_pickable(self,val):
        """Make the structure pickable or not.

        :param val: True or False depending on the pickability of the structure.
        :type val: bool
        
        Example::
        
            myneatstructure.set_pickable(True)
        """
        if type(val) is bool:
            self.__is_pickable = val
    """ This represent the capacity for a :class:`~gamelib.BoardItem.BoardItem` to be overlapped by player or NPC.

        :return: False
        :rtype: bool
        """
    def overlappable(self):
        return self.__is_overlappable

    def set_overlappable(self,val):
        if type(val) is bool:
            self.__is_overlappable = val
    
    def restorable(self):
        """ 
        This represent the capacity for an :class:`~gamelib.Immovable.Immovable` :class:`~gamelib.BoardItem.BoardItem` (in this case a GenericStructure item) to be restored by the board if the item is overlappable and has been overlapped by another :class:`~gamelib.Movable.Movable` item.

        The value of this property is set with :meth:`~.set_restorable`
        
        :return: False
        :rtype: bool
        """
        return self.__is_restorable
        
    
    def set_restorable(self,val):
        """Make the structure restorable or not.

        :param val: True or False depending on the pickability of the structure.
        :type val: bool
        
        Example::
        
            myneatstructure.set_restorable(True)
        """
        if type(val) is bool:
            self.__is_restorable = val
        else:
            raise HacInvalidTypeException('set_restorable(bool) takes a boolean as paramater.')

class GenericActionnableStructure(GenericStructure,Actionnable):
    """
    .. TODO:: Documentation
    """
    def __init__(self,**kwargs):
        GenericStructure.__init__(self,**kwargs)
        Actionnable.__init__(self,**kwargs)


class Treasure(Immovable):
    """
    .. TODO:: Documentation
    """
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
            self._size = kwargs['size']

    def pickable(self):
        return True
    
    def overlappable(self):
        return False

    def restorable(self):
        return False

class Door(GenericStructure):
    """
    .. TODO:: Documentation
    """
    def __init__(self,**kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = ']'
        Immovable.__init__(self,**kwargs)
        if 'value' not in kwargs.keys():
            self.value = 0
        else:
            self.value = kwargs['value']
        if 'size' not in kwargs.keys():
            self._size = 1
        else:
            self._size = kwargs['size']
        if 'name' not in kwargs.keys():
            self.name = 'Door'
        else:
            self.name = kwargs['name']
        if 'type' not in kwargs.keys():
            self.type = 'door'
        else:
            self.type = kwargs['type']
        if 'pickable' not in kwargs.keys():
            self.set_pickable( False )
        else:
            self.set_pickable( kwargs['pickable'] )
        if 'overlappable' not in kwargs.keys():
            self.set_overlappable( True )
        else:
            self.set_overlappable( kwargs['overlappable'] )
        if 'restorable' not in kwargs.keys():
            self.set_restorable( True )
        else:
            self.set_restorable( kwargs['restorable'] )
        
    
