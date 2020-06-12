from gamelib.BoardItem import BoardItem, BoardItemVoid
from gamelib.Game import Game
from gamelib.Characters import Player
import gamelib.Constants as Constants
import unittest


def readable_board_item(boarditem):
    return f"{boarditem.pos}\t{boarditem.name.strip()}"


def readable_board_items(board_item_list):
    return (
        "[" + ", ".join([readable_board_item(item) for item in board_item_list]) + "]"
    )


class GameNeighborTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.game = Game()
        self.board = self.game.load_board("hac-maps/kneighbors.json", 1)
        self.game.player = Player(name="player")
        self.game.change_level(1)
        self.tree26 = self.board.item(2, 6)
        self.treasure38 = self.board.item(3, 8)
        self.tree39 = self.board.item(3, 9)
        self.wall45 = self.board.item(4, 5)
        self.wall46 = self.board.item(4, 6)
        self.wall47 = self.board.item(4, 7)
        self.wall57 = self.board.item(5, 7)
        self.npc77 = self.board.item(7, 7)
        self.treasure1212 = self.board.item(12, 12)
        self.tree1310 = self.board.item(13, 10)
        self.npc168 = self.board.item(16, 8)

    def test_player_neighbors(self):
        testcases = (
            ([3, 3], []),
            ([3, 5], [self.tree26, self.wall45, self.wall46]),
            ([3, 6], [self.tree26, self.wall45, self.wall46, self.wall47]),
            ([3, 7], [self.tree26, self.wall46, self.wall47, self.treasure38]),
            ([4, 8], [self.wall47, self.wall57, self.treasure38, self.tree39]),
            ([5, 6], [self.wall45, self.wall46, self.wall47, self.wall57]),
        )

        for pos, expected_board_items in testcases:
            with self.subTest(str(pos)):
                self.game.player.pos = pos
                actual_board_items = self.game.neighbors()
                assertion_message = " ".join(
                    [
                        readable_board_items(expected_board_items),
                        "!=",
                        readable_board_items(actual_board_items),
                    ]
                )
                self.assertSetEqual(
                    set(expected_board_items),
                    set(actual_board_items),
                    assertion_message,
                )

    def test_npc_neighbors(self):
        def move_player_next_to_npc77():
            pos_next_to_npc = [7, 8]
            self.game.move_player(Constants.DOWN, pos_next_to_npc[0])
            self.game.move_player(Constants.RIGHT, pos_next_to_npc[1])
            self.assertEqual(pos_next_to_npc, self.game.player.pos)

        actual_board_items = self.game.neighbors(1, self.npc77)
        self.assertSetEqual(set(), set(actual_board_items))

        move_player_next_to_npc77()
        actual_board_items = self.game.neighbors(1, self.npc77)
        self.assertSetEqual({self.game.player}, set(actual_board_items))

    def dump_board_items(self):
        h, w = self.board.size
        for y in range(h):
            for x in range(w):
                boarditem = self.board.item(y, x)
                assert isinstance(boarditem, BoardItem)
                if isinstance(boarditem, BoardItemVoid):
                    continue
                print(readable_board_item(boarditem))
