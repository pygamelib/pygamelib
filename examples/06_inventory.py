import examples_includes
from gamelib.Inventory import Inventory
from gamelib.Structures import Treasure

inv = Inventory(max_size=5)
print('Inventory size:'+str(inv.size()))
inv.add_item(Treasure(name='money'))
print('Inventory size:'+str(inv.size()))
inv.add_item(Treasure(name='money'))
print('Inventory size:'+str(inv.size()))
inv.add_item(Treasure(name='money'))
print('Inventory size:'+str(inv.size()))
inv.add_item(Treasure(name='money'))
print('Inventory size:'+str(inv.size()))
inv.add_item(Treasure(name='money'))
print('Inventory size:'+str(inv.size()))

print(inv)
print("Inventory value:"+str(inv.value()))

print( "Item named 'money':" + str(inv.get_item('money')) )

inv.delete_item('money')
print('Inventory size:'+str(inv.size()))
print("Inventory value:"+str(inv.value()))
print(inv)