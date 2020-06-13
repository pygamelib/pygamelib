from gamelib.Board import Board
from gamelib.Structures import Wall

walls = []
for i in range(0, 11):
    walls.append(Wall())

b = Board(size=[10, 10])
for i in range(0, 10):
    b.place_item(walls[i], i, i)

b.place_item(Wall(model="*", type="round"), 0, 9)
b.place_item(Wall(model="*", type="round"), 1, 9)
print(b.get_immovables())
for i in b.get_immovables(type="round"):
    print(f"{i}: {i.name} pos: {i.pos} ({id(i)})")

print("DISCARDING")
b._immovables.discard(b.item(1, 9))

for i in b.get_immovables(type="round"):
    print(f"{i}: {i.name} pos: {i.pos} ({id(i)})")
