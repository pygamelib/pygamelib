import pygamelib.engine as pgl_engine
import pygamelib.base as pgl_base
import pygamelib.board_items as pgl_board_items
import pygamelib.gfx.core as gfx_core
from pygamelib import constants
import unittest


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = pgl_engine.Board(
            name="test_board",
            size=[10, 10],
            player_starting_position=[5, 5],
        )

    def test_create_board(self):
        self.board = pgl_engine.Board(
            name="test_board",
            size=[10, 10],
            player_starting_position=[5, 5],
            ui_borders="*",
        )
        self.assertEqual(self.board.name, "test_board")
        self.assertEqual(self.board.ui_border_bottom, "*")
        ret = self.board.__str__()
        self.assertIsNotNone(ret)
        b = pgl_engine.Board(
            name="test_board_sprixel",
            size=[10, 10],
            player_starting_position=[5, 5],
            ui_board_void_cell_sprixel=gfx_core.Sprixel(),
        )
        vc = b.generate_void_cell()
        self.assertIsInstance(vc.sprixel, gfx_core.Sprixel)

    def test_sanity_size_is_list(self):
        with self.assertRaises(Exception) as context:
            self.board = pgl_engine.Board(
                name="test_board", size="bad", player_starting_position=[5, 5]
            )

        self.assertTrue("must be a list." in str(context.exception))

    def test_sanity_size_has_two_elements(self):
        with self.assertRaises(Exception) as context:
            self.board = pgl_engine.Board(
                name="test_board", size=["one"], player_starting_position=[5, 5]
            )

        self.assertTrue("must be a list of 2 elements" in str(context.exception))

    def test_sanity_size_element_one_int(self):
        with self.assertRaises(Exception) as context:
            self.board = pgl_engine.Board(
                name="test_board", size=["one", "two"], player_starting_position=[5, 5]
            )

        self.assertTrue("first element of the" in str(context.exception))

    def test_sanity_size_element_two_int(self):
        with self.assertRaises(Exception) as context:
            self.board = pgl_engine.Board(
                name="test_board", size=[10, "two"], player_starting_position=[5, 5]
            )

        self.assertTrue("second element of the" in str(context.exception))

    def test_sanity_name_string(self):
        with self.assertRaises(Exception) as context:
            self.board = pgl_engine.Board(
                name=100, size=[10, 10], player_starting_position=[5, 5]
            )

        self.assertTrue("must be a string" in str(context.exception))

    def test_sanity_ui_border_bottom_string(self):
        with self.assertRaises(pgl_base.PglException) as context:
            self.board = pgl_engine.Board(
                name="test", size=[10, 10], ui_border_bottom=[]
            )
            self.assertEqual(context.error, "SANITY_CHECK_KO")

    def test_sanity_ui_border_top_string(self):
        with self.assertRaises(Exception) as context:
            self.board = pgl_engine.Board(
                name="test_board", size=[10, 10], ui_border_top=[]
            )

        self.assertTrue("must be a string" in str(context.exception))

    def test_sanity_ui_border_left_string(self):
        with self.assertRaises(Exception) as context:
            self.board = pgl_engine.Board(
                name="test_board", size=[10, 10], ui_border_left=[]
            )

        self.assertTrue("must be a string" in str(context.exception))

    def test_sanity_ui_border_right_string(self):
        with self.assertRaises(Exception) as context:
            self.board = pgl_engine.Board(
                name="test_board", size=[10, 10], ui_border_right=[]
            )

        self.assertTrue("must be a string" in str(context.exception))

    def test_sanity_ui_board_void_cell_string(self):
        with self.assertRaises(Exception) as context:
            self.board = pgl_engine.Board(
                name="test_board", size=[10, 10], ui_board_void_cell=[]
            )
        self.assertTrue("must be a string" in str(context.exception))

    def test_sanity_ui_board_void_cell_sprixel(self):
        with self.assertRaises(pgl_base.PglException) as context:
            self.board = pgl_engine.Board(
                name="test_board", size=[10, 10], ui_board_void_cell_sprixel=[]
            )
            self.assertEqual(context.error, "SANITY_CHECK_KO")
        b = pgl_engine.Board(
            name="test_board",
            size=[90, 90],
            DISPLAY_SIZE_WARNINGS=True,
            ui_board_void_cell_sprixel=gfx_core.Sprixel(),
        )
        self.assertIsInstance(b, pgl_engine.Board)
        self.assertIsNone(b.display())
        self.board.item(0, 2).model = "#"
        self.assertIsNone(self.board.display())

    def test_item(self):
        self.board = pgl_engine.Board(
            name="test_board", size=[10, 10], player_starting_position=[5, 5]
        )
        self.placed_item = pgl_board_items.BoardItem()

        self.board.place_item(self.placed_item, 1, 1)
        self.returned_item = self.board.item(1, 1)
        self.assertEqual(self.placed_item, self.returned_item)

        with self.assertRaises(pgl_base.PglOutOfBoardBoundException) as excinfo:
            self.board.item(15, 15)
        self.assertTrue("out of the board boundaries" in str(excinfo.exception))
        sprix = gfx_core.Sprixel(bg_color=gfx_core.Color(45, 45, 45))
        sprix.is_bg_transparent = True
        self.board.place_item(
            pgl_board_items.Door(
                sprixel=gfx_core.Sprixel(bg_color=gfx_core.Color(15, 15, 15))
            ),
            5,
            5,
        )
        i = pgl_board_items.NPC(sprixel=sprix)
        self.assertIsNone(self.board.place_item(i, 5, 5))
        self.assertIsNone(
            self.board.place_item(
                pgl_board_items.ComplexNPC(base_item_type=pgl_board_items.Movable), 8, 8
            )
        )
        self.assertIsNone(self.board.place_item(pgl_board_items.Tile(), 8, 2))
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            self.board.place_item(1, 1, 1)
        with self.assertRaises(pgl_base.PglOutOfBoardBoundException):
            self.board.place_item(i, 100, 100)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            self.board.remove_item(1)
        # Let's try to break things
        j = pgl_board_items.NPC()
        j.store_position(2, 2)
        with self.assertRaises(pgl_base.PglException) as e:
            self.board.remove_item(j)
            self.assertEqual(e.error, "invalid_item")
        self.assertTrue(self.board.remove_item(i))
        b = pgl_engine.Board()
        i = pgl_board_items.ComplexNPC()
        self.assertIsNone(b.place_item(i, 5, 5))
        self.assertTrue(b.remove_item(i))

    def test_move_complex(self):
        def _act(p):
            p[0].assertEqual(p[1], 1)

        self.board = pgl_engine.Board(
            name="test_board",
            size=[10, 10],
            player_starting_position=[5, 5],
        )
        i = pgl_board_items.ComplexNPC(
            sprite=gfx_core.Sprite(default_sprixel=gfx_core.Sprixel("*"))
        )
        g = pgl_engine.Game(mode=constants.MODE_RT)
        self.board.place_item(i, 1, 1)
        self.assertIsInstance(self.board.item(1, 1), pgl_board_items.ComplexNPC)
        self.assertIsNone(self.board.move(i, constants.RIGHT, 1))
        i = pgl_board_items.ComplexPlayer(
            sprite=gfx_core.Sprite(default_sprixel=gfx_core.Sprixel("*"))
        )
        self.board.place_item(i, 3, 1)
        self.assertIsInstance(self.board.item(3, 1), pgl_board_items.ComplexPlayer)
        self.board.place_item(
            pgl_board_items.GenericActionableStructure(
                action=_act, action_parameters=[self, 1]
            ),
            i.row,
            i.column + i.width,
        )
        self.assertIsNone(self.board.move(i, constants.RIGHT, 1))
        self.board.place_item(
            pgl_board_items.Treasure(value=50), i.row + i.height, i.column
        )
        self.assertIsNone(self.board.move(i, constants.DOWN, 1))
        self.assertEqual(i.inventory.value(), 50)
        i.parent = g
        i.dtmove = 0.0
        self.assertIsNone(self.board.move(i, pgl_base.Vector2D(1, 0)))
        i.dtmove = 5.0
        self.assertIsNone(self.board.move(i, pgl_base.Vector2D(1, 0)))
        with self.assertRaises(pgl_base.PglObjectIsNotMovableException):
            self.board.move(pgl_board_items.Immovable(), constants.DOWN, 1)
        g.mode = constants.MODE_TBT
        self.board.place_item(pgl_board_items.Door(), i.row, i.column + i.width)
        self.assertIsNone(self.board.move(i, constants.RIGHT, 1))
        self.assertIsNone(self.board.move(i, constants.RIGHT, 2))
        self.assertIsNone(self.board.move(i, constants.DOWN, 2))
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            self.board.move(i, constants.DOWN, "1")
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            self.board.move(i, "constants.DOWN", 1)

    def test_move_simple(self):
        def _act(p):
            p[0].assertEqual(p[1], 1)

        i = pgl_board_items.Player(sprixel=gfx_core.Sprixel("*"))
        i.sprixel.is_bg_transparent = True
        b = pgl_engine.Board(
            name="test_board",
            size=[10, 10],
            player_starting_position=[0, 0],
        )
        b.place_item(i, 0, 0)
        self.assertIsNone(b.move(i, constants.DOWN, 1))
        self.assertIsNone(b.move(i, constants.UP, 1))
        self.assertIsNone(b.move(i, constants.RIGHT, 1))
        self.assertIsNone(b.move(i, constants.LEFT, 1))
        self.assertIsNone(b.move(i, constants.DRDOWN, 1))
        self.assertIsNone(b.move(i, constants.DRUP, 1))
        self.assertIsNone(b.move(i, constants.DLDOWN, 1))
        self.assertIsNone(b.move(i, constants.DLUP, 1))
        self.assertIsNone(b.move(i, pgl_base.Vector2D(0, 0)))
        self.assertEqual(i.pos, [0, 0])
        b.place_item(
            pgl_board_items.GenericActionableStructure(
                action=_act, action_parameters=[self, 1]
            ),
            0,
            1,
        )
        self.assertIsNone(b.move(i, constants.RIGHT, 1))
        self.assertIsNone(b.move(i, constants.RIGHT, 1))
        b.place_item(pgl_board_items.Treasure(value=50), i.row + 1, i.column)
        self.assertIsNone(b.move(i, constants.DOWN, 1))
        self.assertEqual(i.inventory.value(), 50)
        b.place_item(
            pgl_board_items.Door(
                sprixel=gfx_core.Sprixel(bg_color=gfx_core.Color(45, 45, 45))
            ),
            i.row + 1,
            i.column,
        )
        b.place_item(
            pgl_board_items.Door(
                sprixel=gfx_core.Sprixel(bg_color=gfx_core.Color(45, 45, 45))
            ),
            i.row + 2,
            i.column,
        )
        self.assertIsNone(b.move(i, constants.DOWN, 1))
        self.assertIsNone(b.move(i, constants.DOWN, 1))
        self.assertIsNone(b.clear_cell(i.row, i.column))

    def test_get_objects(self):
        b = pgl_engine.Board(
            name="test_board",
            size=[10, 10],
            player_starting_position=[0, 0],
        )
        for i in range(1, 4):
            b.place_item(pgl_board_items.NPC(name=f"mover{i}", type="mover"), 0, i)
        for i in range(1, 4):
            b.place_item(pgl_board_items.Wall(name=f"static{i}", type="static"), i, 0)
        ret = b.get_immovables(type="static")
        self.assertEqual(len(ret), 3)
        self.assertEqual(len(ret), len(b.get_immovables()))
        ret = b.get_movables(type="static")
        self.assertEqual(len(ret), 0)
        ret = b.get_movables(type="mover")
        self.assertEqual(len(ret), 3)
        self.assertEqual(len(ret), len(b.get_movables()))

    def test_clear_cell(self):
        self.board = pgl_engine.Board(
            name="test_board", size=[10, 10], player_starting_position=[5, 5]
        )
        self.placed_item = pgl_board_items.BoardItem()
        self.board.place_item(item=self.placed_item, row=1, column=1)
        self.assertIsInstance(self.board.item(1, 1), pgl_board_items.BoardItem)

        self.board.clear_cell(1, 1)
        self.assertIsInstance(self.board.item(1, 1), pgl_board_items.BoardItemVoid)

    def test_size(self):
        board = pgl_engine.Board(
            name="test_board", size=[20, 30], player_starting_position=[5, 5]
        )
        self.assertEqual(board.height, 30)
        self.assertEqual(board.width, 20)

    def test_display_around(self):
        i = pgl_board_items.NPC()
        self.board.place_item(i, 2, 2)
        self.board.display_around(i, 2, 2)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            self.board.display_around(1, 2, 2)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            self.board.display_around(i, "2", 2)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            self.board.display_around(i, 2, "2")
        self.assertIsNone(self.board.display_around(i, 20, 20))
        self.assertIsNone(self.board.display_around(i, 2, 20))
        self.assertIsNone(self.board.display_around(i, 20, 2))
        self.board.item(2, 3).model = "#"
        self.assertIsNone(self.board.display_around(i, 2, 2))
        self.board.clear_cell(2, 2)
        i = pgl_board_items.ComplexNPC()
        self.board.place_item(i, 2, 2)
        self.assertIsNone(self.board.display_around(i, 2, 2))
        b = pgl_engine.Board(parent=pgl_engine.Game())
        self.assertIsInstance(b, pgl_engine.Board)
        b.place_item(i, 2, 2)
        self.assertIsNone(self.board.display_around(i, 2, 2))
        self.assertIsNone(self.board.display())


if __name__ == "__main__":
    unittest.main()
