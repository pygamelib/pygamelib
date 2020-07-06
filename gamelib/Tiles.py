import gamelib.BoardItem
from gamelib.Movable import Movable
from gamelib import Structures
from gamelib.Characters import NPC


# These shouldn't be here
class Tile(gamelib.BoardItem.BoardComplexItem):
    def __init__(self, **kwargs):
        kwargs["base_item_type"] = Structures.Door
        super().__init__(**kwargs)

    def overlappable(self):
        return True

    def can_move(self):
        return False

    def pickable(self):
        return False


class MovableTile(Movable, gamelib.BoardItem.BoardComplexItem):
    def __init__(self, **kwargs):
        Movable.__init__(self, **kwargs)
        kwargs["base_item_type"] = NPC
        gamelib.BoardItem.BoardComplexItem.__init__(self, **kwargs)

    def overlappable(self):
        return False

    def pickable(self):
        return False
