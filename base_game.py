from gamelib.Board import Board
from gamelib.BoardItem import BoardItem
from gamelib.Utils import warn, fatal, info,debug
from gamelib.Game import Game

from gamelib.Structures import Wall,Treasure

game = Game(name='HAC Game')

board = Board(name='Level_1',size=[20,10])
print(board)

debug('displaying empty board')
board.display()


w = Wall()
t = Treasure()

board.place_item(w,3,3)
board.place_item(t,3,2)
board.display()

game.add_menu_entry('w','Go up')
game.add_menu_entry('s','Go down')
game.add_menu_entry('a','Go left')
game.add_menu_entry('d','Go right')

game.clear_screen()
board.display()
game.print_menu()