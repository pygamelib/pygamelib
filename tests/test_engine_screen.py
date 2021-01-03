from pygamelib import engine, board_items, functions, base
from pygamelib.gfx.core import SpriteCollection, Sprixel, Color, Sprite
import unittest


# Test cases for all classes in pygamelib.gfx.core except for Animation.


class TestBase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.screen = engine.Screen()
        self.assertIsInstance(self.screen, engine.Screen)

    # def test_screen_create_empty(self):
    #     with self.assertRaises(Exception) as context:
    #         engine.Screen()

    #     self.assertTrue("terminal_is_missing" in str(context.exception))

    # def test_screen_create_bad(self):
    #     with self.assertRaises(Exception) as context:
    #         engine.Screen("Terminal")

    #     self.assertTrue("terminal_not_blessed" in str(context.exception))

    def test_screen_create_good(self):
        scr = engine.Screen()
        self.assertIsInstance(scr, engine.Screen)

    def test_clear(self):
        self.assertIsNone(self.screen.clear())

    def test_screen_dimension(self):
        self.assertEqual(self.screen.terminal.width, self.screen.width)
        self.assertEqual(self.screen.terminal.height, self.screen.height)

    def test_screen_display(self):
        self.assertIsNone(
            self.screen.display_at(
                "This is centered",
                int(self.screen.height / 2),
                int(self.screen.width / 2),
                clear_eol=True,
            )
        )

    def test_screen_display_sprite(self):
        sprites_panda = SpriteCollection.load_json_file("tests/panda.spr")
        self.assertIsNone(
            self.screen.display_sprite(sprites_panda["panda"], filler=Sprixel(" "))
        )

    def test_screen_display_sprite_at(self):
        sprites_panda = SpriteCollection.load_json_file("tests/panda.spr")
        self.assertIsNone(
            self.screen.display_sprite_at(
                sprites_panda["panda"],
                Sprixel(" "),
                int(self.screen.height / 2),
                int(self.screen.width / 2),
            )
        )

    def test_screen_buffer(self):
        sprites_panda = SpriteCollection.load_json_file("tests/panda.spr")
        b = engine.Board(size=[20, 20])
        s = engine.Screen()
        b.place_item(board_items.Tile(sprite=sprites_panda["panda"]), 0, 0)
        self.assertIsInstance(b.render_cell(1, 1), Sprixel)
        b.item(19, 19).model = "@"
        b.item(19, 19).sprixel = None
        self.assertIsInstance(b.render_cell(19, 19), Sprixel)
        self.assertEqual(b.render_cell(19, 19), Sprixel())
        with self.assertRaises(engine.base.PglOutOfBoardBoundException):
            b.render_cell(50, 50)
        self.assertIsNone(s.clear_buffers())
        self.assertIsNone(s.clear_screen_buffer())
        self.assertTrue(s._is_dirty)
        self.assertTrue(functions.pgl_isinstance(s.buffer, "numpy.ndarray"))
        self.assertIsNone(s.update())
        b = engine.Board(size=[1, 1])
        self.assertIsNone(s.place("test", 0, 0))
        self.assertIsNone(s.place(b, 1, 0))
        t = base.Text("test")
        self.assertIsNone(s.place(t, 2, 0))
        self.assertIsNone(s.place(sprites_panda["panda"], 0, 5))
        s.update()
        t.text = "update"
        self.assertIsNone(s.place(sprites_panda["panda"], s.height - 2, s.width - 2))
        self.assertIsNone(s.place("test", 1, s.width - 2))
        s.update()
        # Now testing partial display
        camera = board_items.Camera()
        camera.row = 0
        camera.column = 0
        b = engine.Board(
            size=[s.width * 2, s.height * 2],
            enable_partial_display=True,
            partial_display_viewport=[int(s.height / 2) - 1, int(s.width / 2) - 1],
            partial_display_focus=camera,
            DISPLAY_SIZE_WARNINGS=False,
        )
        for row in range(0, b.height):
            for col in range(0, b.width):
                b.place_item(
                    board_items.Wall(
                        sprixel=Sprixel(" ", Color(row * 4, col, int((row + col) / 2))),
                    ),
                    row,
                    col,
                )
        self.assertIsNone(s.place(b, 0, 0))
        self.assertIsNone(s.update())
        b.partial_display_viewport = [int(s.height * 3) - 1, int(s.width * 3) - 1]
        camera.row += 1
        with self.assertRaises(IndexError):
            s.render()
            s.update()
        b.partial_display_viewport = [int(s.height / 2) - 1, int(s.width / 2) - 1]
        camera = board_items.Tile(
            sprite=Sprite(
                sprixels=[[Sprixel("+"), Sprixel("+")], [Sprixel("+"), Sprixel("+")]]
            )
        )
        b.partial_display_focus = camera
        # Please never do that in real life...
        camera.pos = [1, 1]
        s.render()
        s.update()
        self.assertIsNone(s.place("test delete", 0, 0))
        s.update()
        self.assertIsNone(s.delete(0, 0))
        s.update()


if __name__ == "__main__":
    unittest.main()
