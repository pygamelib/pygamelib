from gamelib.BoardItem import BoardItem
from gamelib.HacExceptions import HacInvalidTypeException, HacInventoryException
import uuid

class Inventory():
    def __init__(self,max_size=10):
        self.max_size = max_size
        self.__items = {}
    
    def __str__(self):
        s =  '=============\n'
        s += '= inventory =\n'
        s += '============='
        types = {}
        for k in self.__items.keys():
            if self.__items[k].type in types.keys():
                types[self.__items[k].type]['size'] += self.__items[k].size()
            else:
                types[self.__items[k].type] = {'size':self.__items[k].size(),'model':self.__items[k].model}
        for k in types.keys():
            s += f"\n{types[k]['model']} : {types[k]['size']}"
        return s
    
    def add_item(self, item):
        if isinstance(item, BoardItem):
            if item.pickable():
                if item.name == None or item.name == '' or item.name in self.__items.keys():
                    item.name += '_'+uuid.uuid4().hex
                if hasattr(item,'_size') and self.max_size >= self.size()+item.size():
                    self.__items[item.name] = item
                else:
                    raise HacInventoryException('not_enough_space','There is not enough space left in the inventory. Max. size: '+self.max_size+', current inventory size: '+self.size()+' and item size: '+item.size())
            else:
                raise HacInventoryException('not_pickable',f"The item (name='{item.name}') is not pickable. Make sure to only add pickable objects to the inventory.")
        else:
            raise HacInvalidTypeException("The item is not an instance of BoardItem. The item is of type: "+type(item))
    
    def size(self):
        val = 0
        for k in self.__items.keys():
            if hasattr(self.__items[k],'size'):
                val += self.__items[k].size()
        return val

    def value(self):
        """
        Return the cumulated value of the inventory.
        It can be used for scoring for example.
        Ex: 
        if inventory,value() >= 10:
            print('Victory!')
            break
        """
        val = 0
        for k in self.__items.keys():
            if hasattr(self.__items[k],'value'):
                val += self.__items[k].value
        return val

    def items_name(self):
        return self.__items.keys()
    
    def get_item(self,name):
        if name in self.__items.keys():
            return self.__items[name]
        else:
            raise HacInventoryException('no_item_by_that_name',f'There is no item named "{name}" in the inventory.')

    def delete_item(self,name):
        if name in self.__items.keys():
            del self.__items[name]
        else:
            raise HacInventoryException('no_item_by_that_name',f'There is no item named "{name}" in the inventory.')