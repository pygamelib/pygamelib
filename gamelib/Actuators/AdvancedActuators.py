from gamelib.Actuators.Actuator import Behavioral
from gamelib.HacExceptions import HacInvalidTypeException, HacException
from gamelib.Game import Game
from gamelib.BoardItem import BoardItemVoid
from gamelib.Movable import Movable
import gamelib.Constants as Constants
import collections

class PathFinder(Behavioral):
    """
    .. warning:: Do not use this module at the moment, it's a work in progress
    """
    def __init__(self,game=None,actuated_object=None,destination=(0,0)):
        Behavioral.__init__(self)
        self.actuated_object = actuated_object
        self.destination = destination
        self.game = game
        self._current_path = []
    
    def set_destination(self,row=0,column=0):
        """Set the targeted destination.

        :param row: "row" coordinate on the board grid
        :type row: int
        :param column: "column" coordinate on the board grid
        :type column: int
        :raises HacInvalidTypeException: if row or column are not int.
        
        Example::
        
            mykillernpc.actuator.set_destination( mygame.player.pos[0], mygame.player.pos[1] )
        """
        if type(row) is not int or type(column) is not int:
            raise HacInvalidTypeException("In Actuator.PathFinder.set_destination(x,y) both x and y must be integer.")
        self.destination = (row,column)
        # if self.actuated_object != None and issubclass(self.actuated_object, Movable):
        #     self.find_path()
    
    def find_path(self):
        """Find a path to the destination.
        
        Destination (PathFinder.destination) has to be set beforehand. This method implements a Breadth First Search algorithm (`Wikipedia <https://en.wikipedia.org/wiki/Breadth-first_search>`_) to find the shortest path to destination.

        Example::
        
            mykillernpc.actuator = PathFinder(game=mygame,actuated_object=mykillernpc)
            mykillernpc.actuator.set_destination( mygame.player.pos[0], mygame.player.pos[1] )
            mykillernpc.actuator.find_path()
        
        .. warning:: PathFinder.destination is a tuple! Please use PathFinder.set_destination(x,y) to avoid problems.

        """
        if self.actuated_object == None:
            raise HacException('actuated_object is not defined','PathFinder.actuated_object has to be defined.')
        if not isinstance(self.actuated_object, Movable):
            raise HacException('actuated_object not a Movable object','PathFinder.actuated_object has to be an instance of a Movable object.')
        if self.destination == None:
            raise HacException('destination is not defined','PathFinder.destination has to be defined.')

        queue = collections.deque([[(self.actuated_object.pos[0],self.actuated_object.pos[1])]]) 
        seen = set([(self.actuated_object.pos[0],self.actuated_object.pos[1])]) 
        while queue: 
            path = queue.popleft() 
            x, y = path[-1] 
            if (x,y) == self.destination: 
                self._current_path = path
                # We return only a copy of the path as we need to keep the real one untouched for our own needs.
                return path.copy() 
            for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)): 
                if 0 <= y2 < self.game.current_board().size[0] and 0 <= x2 < self.game.current_board().size[1] and self.game.current_board().item(x2,y2).overlappable() and (x2, y2) not in seen: 
                    queue.append(path + [(x2, y2)]) 
                    seen.add((x2, y2))
        return []
    
    def next_move(self):
        if len(self._current_path) == 0 and (self.actuated_object.pos[0] != self.destination[0] or self.actuated_object.pos[1] != self.destination[1]):
            self.find_path()
        if len(self._current_path) == 0:
                return Constants.NO_DIR
        next_position = self._current_path.pop(0)
        if next_position[0] == self.actuated_object.pos[0] and next_position[1] == self.actuated_object.pos[1]:
            if len(self._current_path) == 0:
                return Constants.NO_DIR
            next_position = self._current_path.pop(0)
        
        # print(f'Next position is: {next_position} and object position is {self.actuated_object.pos} _current_path length is {len(self._current_path)}')
        dr = self.actuated_object.pos[0] - next_position[0]
        dc = self.actuated_object.pos[1] - next_position[1]
        print(f'dr={dr} dc={dc}')
        if dr == -1 and dc == 0:
            return Constants.DOWN
        elif dr == 1 and dc == 0:
            return Constants.UP
        elif dr == 0 and dc == 1:
            return Constants.LEFT
        elif dr == 0 and dc == -1:
            return Constants.RIGHT
        elif dr == -1 and dc == -1:
            return Constants.DRDOWN
        elif dr == 1 and dc == -1:
            return Constants.DRUP
        elif dr == -1 and dc == 1:
            return Constants.DLDOWN
        elif dr == 1 and dc == 1:
            return Constants.DLUP
        
