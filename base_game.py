from gamelib.Board import Board
from gamelib.Utils import warn, fatal, info,debug

board = Board(name='Level_1',size=[80,80])
print(board)

debug('displaying empty board')
board.display()