from gamelib.Game import Game
from gamelib.Characters import Player
from gamelib.Board import Board
from gamelib.Structures import Wall, Door
import gamelib.Sprites as Sprites
import gamelib.Utils as Utils
import gamelib.Constants as Constants

from math import sqrt
from random import random, choice
from random import randrange


class DungeonSqr:
    def __init__(self, sqr):
        self.sqr = sqr

    def get_ch(self):
        return self.sqr


class Room:
    def __init__(self, r, c, h, w):
        self.row = r
        self.col = c
        self.height = h
        self.width = w


class RLDungeonGenerator:
    def __init__(self, w, h):
        self.MAX = 15  # Cutoff for when we want to stop dividing sections
        self.width = w
        self.height = h
        self.leaves = []
        self.dungeon = []
        self.rooms = []

        for h in range(self.height):
            row = []
            for w in range(self.width):
                row.append(DungeonSqr("#"))

            self.dungeon.append(row)

    def random_split(self, min_row, min_col, max_row, max_col):
        # We want to keep splitting until the sections get down to the threshold
        seg_height = max_row - min_row
        seg_width = max_col - min_col

        if seg_height < self.MAX and seg_width < self.MAX:
            self.leaves.append((min_row, min_col, max_row, max_col))
        elif seg_height < self.MAX and seg_width >= self.MAX:
            self.split_on_vertical(min_row, min_col, max_row, max_col)
        elif seg_height >= self.MAX and seg_width < self.MAX:
            self.split_on_horizontal(min_row, min_col, max_row, max_col)
        else:
            if random() < 0.5:
                self.split_on_horizontal(min_row, min_col, max_row, max_col)
            else:
                self.split_on_vertical(min_row, min_col, max_row, max_col)

    def split_on_horizontal(self, min_row, min_col, max_row, max_col):
        split = (min_row + max_row) // 2 + choice((-2, -1, 0, 1, 2))
        self.random_split(min_row, min_col, split, max_col)
        self.random_split(split + 1, min_col, max_row, max_col)

    def split_on_vertical(self, min_row, min_col, max_row, max_col):
        split = (min_col + max_col) // 2 + choice((-2, -1, 0, 1, 2))
        self.random_split(min_row, min_col, max_row, split)
        self.random_split(min_row, split + 1, max_row, max_col)

    def carve_rooms(self):
        for leaf in self.leaves:
            # We don't want to fill in every possible room or the
            # dungeon looks too uniform
            if random() > 0.80:
                continue
            section_width = leaf[3] - leaf[1]
            section_height = leaf[2] - leaf[0]

            # The actual room's height and width will be 60-100% of the
            # available section.
            room_width = round(randrange(60, 100) / 100 * section_width)
            room_height = round(randrange(60, 100) / 100 * section_height)

            # If the room doesn't occupy the entire section we are carving it from,
            # 'jiggle' it a bit in the square
            if section_height > room_height:
                room_start_row = leaf[0] + randrange(section_height - room_height)
            else:
                room_start_row = leaf[0]

            if section_width > room_width:
                room_start_col = leaf[1] + randrange(section_width - room_width)
            else:
                room_start_col = leaf[1]

            self.rooms.append(
                Room(room_start_row, room_start_col, room_height, room_width)
            )
            for r in range(room_start_row, room_start_row + room_height):
                for c in range(room_start_col, room_start_col + room_width):
                    self.dungeon[r][c] = DungeonSqr(".")

    def are_rooms_adjacent(self, room1, room2):
        adj_rows = []
        adj_cols = []
        for r in range(room1.row, room1.row + room1.height):
            if r >= room2.row and r < room2.row + room2.height:
                adj_rows.append(r)

        for c in range(room1.col, room1.col + room1.width):
            if c >= room2.col and c < room2.col + room2.width:
                adj_cols.append(c)

        return (adj_rows, adj_cols)

    def distance_between_rooms(self, room1, room2):
        centre1 = (room1.row + room1.height // 2, room1.col + room1.width // 2)
        centre2 = (room2.row + room2.height // 2, room2.col + room2.width // 2)

        return sqrt((centre1[0] - centre2[0]) ** 2 + (centre1[1] - centre2[1]) ** 2)

    def carve_corridor_between_rooms(self, room1, room2):
        if room2[2] == "rows":
            row = choice(room2[1])
            # Figure out which room is to the left of the other
            if room1.col + room1.width < room2[0].col:
                start_col = room1.col + room1.width
                end_col = room2[0].col
            else:
                start_col = room2[0].col + room2[0].width
                end_col = room1.col
            for c in range(start_col, end_col):
                self.dungeon[row][c] = DungeonSqr(".")

            if end_col - start_col >= 4:
                self.dungeon[row][start_col] = DungeonSqr("+")
                self.dungeon[row][end_col - 1] = DungeonSqr("+")
            elif start_col == end_col - 1:
                self.dungeon[row][start_col] = DungeonSqr("+")
        else:
            col = choice(room2[1])
            # Figure out which room is above the other
            if room1.row + room1.height < room2[0].row:
                start_row = room1.row + room1.height
                end_row = room2[0].row
            else:
                start_row = room2[0].row + room2[0].height
                end_row = room1.row

            for r in range(start_row, end_row):
                self.dungeon[r][col] = DungeonSqr(".")

            if end_row - start_row >= 4:
                self.dungeon[start_row][col] = DungeonSqr("+")
                self.dungeon[end_row - 1][col] = DungeonSqr("+")
            elif start_row == end_row - 1:
                self.dungeon[start_row][col] = DungeonSqr("+")

    # Find two nearby rooms that are in difference groups, draw
    # a corridor between them and merge the groups
    def find_closest_unconnect_groups(self, groups, room_dict):
        shortest_distance = 99999
        start = None
        start_group = None
        nearest = None
        for group in groups:
            for room in group:
                key = (room.row, room.col)
                for other in room_dict[key]:
                    if not other[0] in group and other[3] < shortest_distance:
                        shortest_distance = other[3]
                        start = room
                        nearest = other
                        start_group = group

        self.carve_corridor_between_rooms(start, nearest)

        # Merge the groups
        other_group = None
        for group in groups:
            if nearest[0] in group:
                other_group = group
                break

        start_group += other_group
        groups.remove(other_group)

    def connect_rooms(self):
        # Build a dictionary containing an entry for each room. Each bucket will
        # hold a list of the adjacent rooms, weather they are adjacent along rows or
        # columns and the distance between them.
        #
        # Also build the initial groups (which start of as a list of individual rooms)
        groups = []
        room_dict = {}
        nbr = len(self.rooms)
        idx = 1
        for room in self.rooms:
            print(f"\rGrouping rooms ({idx}/{nbr})...", end="")
            key = (room.row, room.col)
            room_dict[key] = []
            for other in self.rooms:
                other_key = (other.row, other.col)
                if key == other_key:
                    continue
                adj = self.are_rooms_adjacent(room, other)
                if len(adj[0]) > 0:
                    room_dict[key].append(
                        (
                            other,
                            adj[0],
                            "rows",
                            self.distance_between_rooms(room, other),
                        )
                    )
                elif len(adj[1]) > 0:
                    room_dict[key].append(
                        (
                            other,
                            adj[1],
                            "cols",
                            self.distance_between_rooms(room, other),
                        )
                    )

            groups.append([room])
            idx += 1
        print("done")
        while len(groups) > 1:
            print(f"\rconnecting groups ({len(groups)} remaining)...", end="")
            self.find_closest_unconnect_groups(groups, room_dict)
        print("done")

    def generate_map(self):
        print("Spliting the map")
        self.random_split(1, 1, self.height - 1, self.width - 1)
        print("Splitting complete, now carving rooms.")
        self.carve_rooms()
        print("Room carved, now connecting rooms")
        self.connect_rooms()
        print("Rooms connected")

    def print_map(self):
        for r in range(self.height):
            row = ""
            for c in range(self.width):
                row += self.dungeon[r][c].get_ch()
            print(row)


dg_height = 100
dg_width = 100
print("Generating random dungeon...", end="")
dg = RLDungeonGenerator(dg_width, dg_height)
dg.generate_map()
print("done")
print("\rBuilding the map...", end="")
random_board = Board(
    size=[dg_width, dg_height],
    name="Random dungeon",
    ui_borders=Utils.WHITE_SQUARE,
    ui_board_void_cell=Utils.BLACK_SQUARE,
    DISPLAY_SIZE_WARNINGS=False,
)
potential_starting_position = []
for r in range(dg.height):
    for c in range(dg.width):
        if dg.dungeon[r][c].get_ch() == "#":
            random_board.place_item(Wall(model=Sprites.WALL), r, c)
        elif dg.dungeon[r][c].get_ch() == "+":
            random_board.place_item(Door(model=Sprites.DOOR), r, c)
        elif dg.dungeon[r][c].get_ch() == ".":
            potential_starting_position.append([r, c])
random_board.player_starting_position = choice(potential_starting_position)
print("done")
print(f"starting position chosen: {random_board.player_starting_position}")

# dg.print_map()
# random_board.display()
input("New random dungeon generated. Next?")

g = Game()
g.enable_partial_display = True
# g.load_board('/home/arnaud/Code/Games/hgl-editor/Large_Dungeon.json', 1)
g.player = Player(model=Sprites.MAGE)
g.add_board(1, random_board)
g.change_level(1)

key = None
viewport = [10, 10]
g.partial_display_viewport = viewport
while True:
    if key == "Q":
        break
    elif key == "S":
        g.save_board(1, f"random-dungeon-{randrange(1000,9999)}.json")
    elif key == "1":
        viewport = [10, 10]
        g.partial_display_viewport = viewport
    elif key == "2":
        viewport = [15, 30]
        g.partial_display_viewport = viewport
    elif key == "3":
        viewport = [20, 20]
        g.partial_display_viewport = viewport
    elif key == Utils.key.UP:
        g.move_player(Constants.UP, 1)
    elif key == Utils.key.DOWN:
        g.move_player(Constants.DOWN, 1)
    elif key == Utils.key.LEFT:
        g.move_player(Constants.LEFT, 1)
    elif key == Utils.key.RIGHT:
        g.move_player(Constants.RIGHT, 1)
    g.clear_screen()
    print(f"Player position: {g.player.pos}")
    g.display_board()
    # g.current_board().display_around(g.player, viewport[0], viewport[1])
    if viewport[0] == 10:
        print("1 - viewport 20x20 *")
    else:
        print("1 - viewport 20x20")
    if viewport[0] == 15:
        print("2 - viewport 30x60 *")
    else:
        print("2 - viewport 30x60")
    if viewport[0] == 20:
        print("3 - viewport 40x40 *")
    else:
        print("3 - viewport 40x40")
    key = Utils.get_key()
