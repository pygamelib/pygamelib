from gamelib.Actuators.Actuator import Behavioral
from gamelib.HacExceptions import HacInvalidTypeException
from gamelib.Game import Game
from gamelib.BoardItem import BoardItemVoid
from gamelib.Movable import Movable
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
    
    def set_destination(self,x=0,y=0):
        """Set the targeted destination.

        Then if the actuated_object member variable is set to a Movable object, it will trigger find_path().

        :param x: x coordinate on the board grid
        :type x: int
        :param y: y coordinate on the board grid
        :type y: int
        :raises HacInvalidTypeException: if x or y are not int.
        
        Example::
        
            mykillernpc.actuator.set_destination( mygame.player.pos[0], mygame.player.pos[1] )
        """
        if type(x) is not int or type(y) is not int:
            raise HacInvalidTypeException("In Actuator.PathFinder.set_destination(x,y) both x and y must be integer.")
        self.destination = (x,y)
        if self.actuated_object != None and issubclass(self.actuated_object, Movable):
            self.find_path()
    
    def find_path(self):
        """Find a path to the destination.
        
        Destination (PathFinder.destination) has to be set beforehand. This method implements a Breadth First Search algorithm (`Wikipedia <https://en.wikipedia.org/wiki/Breadth-first_search>`_) to find the shortest path to destination.

        .. important:: This method is automatically called by PathFinder.set_destination(x,y) under certain circumstances, if you satisfy the conditions you should refrain from calling find_path() just after set_destination(x,y) as it will recalculate the path to destination right after. Achieving nothing but a decrease in performances.
        
        Example::
        
            mykillernpc.actuator.set_destination( mygame.player.pos[0], mygame.player.pos[1] )
            mykillernpc.actuator.find_path()
        
        .. warning:: PathFinder.destination is a tuple! Please use PathFinder.set_destination(x,y) to avoid problems.



        """
        pass
        # queue = collections.deque([[start]]) 
        # seen = set([start]) 
        # print("Starting to find the shortest path") 
        # while queue: 
        #     path = queue.popleft() 
        #     x, y = path[-1] 
        #     print(f"x={x} and y={y}") 
        #     if grid[y][x] == goal: 
        #         print('Goal found') 
        #         return path 
        #     for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)): 
        #         print(f"x2={x2} and y2={y2}") 
        #         if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != wall and (x2, y2) not in seen: 
        #             print(f"\tputting x2={x2} and y2={y2} in the queue") 
        #             queue.append(path + [(x2, y2)]) 
        #             seen.add((x2, y2)) 
