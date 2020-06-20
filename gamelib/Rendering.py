from gamelib.BoardItem import BoardMultiItem, BoardItemVoid
from gamelib.Movable import Movable
from gamelib.Board import Board
from gamelib import Structures
from gamelib.Characters import NPC


class Sprite(object):
    def __init__(self, size=[2, 2], sprixels=None, default_sprixel=" ", parent=None):
        super().__init__()
        self.size = size
        self.parent = parent
        self.default_sprixel = default_sprixel
        # They are not pixels but they are atoms of the Sprite molecule...
        if sprixels is not None and len(sprixels) > 0:
            self._sprixels = []
            for row in range(0, size[1]):
                self._sprixels.append([])
                for column in range(0, size[0]):
                    self._sprixels[row].append(sprixels[row][column])

        else:
            self._sprixels = [
                [default_sprixel for i in range(0, size[1])] for i in range(0, size[0])
            ]

    def __repr__(self):
        string = []
        for scanline in self._sprixels:
            string.append("".join(scanline))
        return "\n".join(string)

    def __str__(self):
        return self.__repr__()

    def sprixel(self, row=0, column=None):
        # WARNING: For performance consideration sprixel() does not check the size of
        # its matrix.
        if column is None:
            return self._sprixels[row]
        else:
            return self._sprixels[row][column]

    def set_sprixel(self, row, column, val):
        self._sprixels[row][column] = val

    def load_from_file(self, filename):
        with open(filename, "r") as sprite_file:
            sprixels_list = []
            line_count = 0
            max_width = 0
            while True:
                line = sprite_file.readline()
                if not line:
                    break
                width = 0
                sprixels_list.append([])
                for s in line.rstrip().split("▄"):
                    if s == "\x1b[0m":
                        sprixels_list[line_count][width - 1] += s
                    else:
                        sprixels_list[line_count].append(f"{s}▄")
                        width += 1
                if width > max_width:
                    max_width = width
                # sprixels_list[line_count][width - 1] = sprixels_list[line_count][
                #     width - 1
                # ][:-1]
                line_count += 1
            for row in range(0, len(sprixels_list)):
                if len(sprixels_list[row]) < max_width:
                    for column in range(len(sprixels_list[row]), max_width):
                        sprixels_list[row].append(self.default_sprixel)
            self._sprixels = sprixels_list
            self.size = [max_width, line_count]

    def dimension(self):
        # Warning: dimension recalculate the size of the Sprite, it is much faster
        # although not safe to use self.size
        height = 0
        max_width = 0
        for row in self._sprixels:
            width = 0
            for col in row:
                width += 1
            if width > max_width:
                max_width = width
            height += 1
        return [max_width, height]


class Sprixel(object):
    pass


class Screen(object):
    pass


# These shouldn't be here
class Tile(BoardMultiItem):
    def __init__(self, **kwargs):
        kwargs["base_item_type"] = Structures.Door
        super().__init__(**kwargs)

    def overlappable(self):
        return True

    def can_move(self):
        return False

    def pickable(self):
        return False


class MovableTile(Movable, BoardMultiItem):
    def __init__(self, **kwargs):
        Movable.__init__(self, **kwargs)
        kwargs["base_item_type"] = NPC
        BoardMultiItem.__init__(self, **kwargs)

    def overlappable(self):
        return False

    def pickable(self):
        return False

    def move(self, direction, step):
        if self.parent is None or not isinstance(self.parent, Board):
            return
        for row in range(0, self.dimension[1]):
            for col in range(1, self.dimension[0] + 1):
                if not isinstance(self._item_matrix[row][-col], BoardItemVoid):
                    print(
                        f"About to move sprixel {row},-{col} => {type(self._item_matrix[row][-col])}"
                    )
                    self.parent.move(self._item_matrix[row][-col], direction, step)
