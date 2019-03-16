from gamelib.Board import Board
from gamelib.BoardItem import BoardItem
from gamelib.Utils import warn, fatal, info,debug

from gamelib.Structures import Wall,Treasure

board = Board(name='Level_1',size=[20,10])
print(board)

debug('displaying empty board')
board.display()


w = Wall()
t = Treasure()

board.place_item(w,3,3)
board.place_item(t,3,2)
board.display()
