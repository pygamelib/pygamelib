from pygamelib import engine, board_items, functions, base
from pygamelib.gfx.core import SpriteCollection, Sprixel, Color, Sprite, Font
from pygamelib.gfx import particles
import unittest


class TB(base.PglBaseObject):
    def __init__(self):
        super().__init__()

    def render_to_buffer(self, buff, r, c, h, w):
        buff[r][c] = "T"
        buff[r][c + 1] = "B"


# Test cases for all classes in pygamelib.gfx.core except for Animation.


class TestBase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.screen = engine.Screen(50, 50)
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
        self.assertEqual(self.screen.width, 50)
        self.assertEqual(self.screen.height, 50)

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
                int(self.screen.height / 2),
                int(self.screen.width / 2),
                Sprixel(" "),
            )
        )

    def test_screen_buffer(self):
        sprites_panda = SpriteCollection.load_json_file("tests/panda.spr")
        b = engine.Board(size=[20, 20])
        s = engine.Screen(50, 50)
        # Because CircleCI return a console with no size (most probably because we are
        # not attached to any terminal), we need to make sure that the partial display
        # tests work in that environment too
        screen_width = 0
        screen_height = 0
        if s.width <= 0:
            screen_width = 50
        else:
            screen_width = s.width
        if s.height <= 0:
            screen_height = 50
        else:
            screen_height = s.height
        self.assertEqual(s.vcenter, int(s.height / 2))
        self.assertEqual(s.hcenter, int(s.width / 2))
        b.place_item(board_items.Tile(sprite=sprites_panda["panda"]), 0, 0)
        self.assertIsInstance(b.render_cell(1, 1), Sprixel)
        b.item(19, 19).model = "@"
        b.item(19, 19).sprixel = None
        self.assertIsInstance(b.render_cell(19, 19), Sprixel)
        self.assertEqual(b.render_cell(19, 19), Sprixel())
        b.place_item(board_items.Door(), 19, 19)
        b.place_item(
            board_items.Door(
                sprixel=Sprixel("*", Color(125, 125, 0), is_bg_transparent=False),
            ),
            19,
            19,
        )
        b.place_item(
            board_items.Door(sprixel=Sprixel("#", is_bg_transparent=True)), 19, 19
        )
        b.place_item(
            board_items.NPC(sprixel=Sprixel("$", is_bg_transparent=True)), 19, 19
        )
        self.assertEqual(b.layers(19, 19), 4)
        b.place_item(
            board_items.BoardItemVoid(sprixel=Sprixel(is_bg_transparent=True)), 19, 19
        )
        b.place_item(
            board_items.BoardItemVoid(sprixel=Sprixel(is_bg_transparent=True)), 19, 19
        )
        self.assertIsInstance(b.render_cell(19, 19), Sprixel)
        b._clean_layers(19, 19)
        self.assertEqual(b.layers(19, 19), 3)
        b._clean_layers(18, 19)
        self.assertEqual(b.layers(18, 19), 1)
        with self.assertRaises(base.PglOutOfBoardBoundException):
            b.render_cell(50, 50)
        self.assertIsNone(s.clear_buffers())
        self.assertIsNone(s.clear_frame_buffer())
        self.assertTrue(s._is_dirty)
        self.assertTrue(functions.pgl_isinstance(s.buffer, "numpy.ndarray"))
        self.assertIsNone(s.update())
        b = engine.Board(size=[1, 1])
        emt = particles.ParticleEmitter(particles.EmitterProperties(lifespan=5))
        b.place_item(
            board_items.Wall(model="##", particle_emitter=emt),
            0,
            0,
        )
        self.assertIsNone(s.place("test", 0, 0))
        self.assertIsNone(s.place(b, 1, 0))
        self.assertIsInstance(s.get(1, 0), engine.Board)
        t = base.Text("test 2")
        self.assertIsNone(s.place(t, 2, 0))
        self.assertIsNone(s.place(sprites_panda["panda"], 0, 5))
        self.assertIsNone(s.place(TB(), 3, 0))
        self.assertIsNone(s.place(board_items.BoardItem(model="##"), 10, 0))
        self.assertIsNone(
            s.place(
                board_items.Tile(
                    sprite=Sprite(
                        sprixels=[
                            [Sprixel("##"), Sprixel("##")],
                            [Sprixel("##"), Sprixel("##")],
                        ]
                    )
                ),
                4,
                0,
            )
        )
        self.assertIsNone(
            s.place(
                Sprite(
                    sprixels=[
                        [Sprixel("##"), Sprixel("##")],
                        [Sprixel("###"), Sprixel("##")],
                    ]
                ),
                8,
                0,
            )
        )
        while not emt.finished():
            s.force_render()
        with self.assertRaises(base.PglInvalidTypeException):
            s.place(None, 0, 0)
        with self.assertRaises(base.PglInvalidTypeException):
            s.place(1, 0, 0)
        with self.assertRaises(base.PglException):
            s.place(TB(), 400, 0)
        with self.assertRaises(base.PglException):
            s.place(TB(), 0, 400)
        s.force_update()
        t.text = "update"
        self.assertIsNone(
            s.place(sprites_panda["panda"], screen_height - 2, screen_width - 2)
        )
        self.assertIsNone(s.place("test", 1, screen_width - 2))
        s.update()
        self.assertIsNone(s.render())  # Should not render
        self.assertFalse(s.need_rendering)
        s.trigger_rendering()
        self.assertTrue(s.need_rendering)
        # Now testing partial display
        camera = board_items.Camera()
        camera.row = 0
        camera.column = 0

        b = engine.Board(
            size=[screen_width * 2, screen_height * 2],
            enable_partial_display=True,
            partial_display_viewport=[
                int(screen_height / 2) - 1,
                int(screen_width / 2) - 1,
            ],
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
        self.assertIsNone(s.place(b, 0, 0, 2))
        s.trigger_rendering()
        self.assertIsNone(s.update())
        b.partial_display_viewport = [
            int(screen_height / 2) - 1,
            int(screen_width / 2) - 1,
        ]
        camera.row = b.height - 1
        camera.column = b.width - 1
        self.assertIsNone(s.trigger_rendering())
        self.assertIsNone(s.update())
        camera = board_items.Tile(
            sprite=Sprite(
                sprixels=[[Sprixel("+"), Sprixel("+")], [Sprixel("+"), Sprixel("+")]]
            )
        )
        b.partial_display_focus = camera
        # Please never do that in real life...
        camera.pos = [1, 1]
        self.assertIsNone(s.trigger_rendering())
        self.assertIsNone(s.render())
        self.assertIsNone(s.update())
        # This will succeed but the str type cannot benefit from deferred rendering.
        self.assertIsNone(s.place("test delete", 0, 0, 2))
        self.assertIsNone(s.update())
        self.assertIsNone(s.delete(0, 0))
        self.assertIsNone(s.update())
        self.assertIsNone(
            functions.render_string_to_buffer(
                "hello",
                s._display_buffer,
                0,
                0,
                s._display_buffer.shape[0],
                s._display_buffer.shape[1],
            )
        )
        # This test has nothing to do here... but I'm lazy.
        self.assertEqual(5, functions.clamp(5, 0, 10))
        self.assertEqual(0, functions.clamp(-5, 0, 10))
        self.assertEqual(10, functions.clamp(15, 0, 10))
        # This one either and it's even worst: it's going to disappear!
        t = base.Text("this is a text\non multiple lines")
        t.render_to_buffer(
            s._display_buffer,
            s._display_buffer.shape[0] - 1,
            s._display_buffer.shape[1] - 5,
            s._display_buffer.shape[0],
            s._display_buffer.shape[1],
        )
        s.update()
        t = base.Text(
            "this is a text",
            Color(0, 0, 0),
            Color(255, 255, 255),
            font=Font("8bits"),
        )
        t.render_to_buffer(
            s._display_buffer,
            s._display_buffer.shape[0] - 1,
            s._display_buffer.shape[1] - 5,
            s._display_buffer.shape[0],
            s._display_buffer.shape[1],
        )
        s.update()

    def test_screen_observer(self):
        s = engine.Screen(10, 10)
        obj = TB()
        self.assertFalse(s._is_dirty)
        s.place(obj, 0, 0)
        self.assertTrue(s._is_dirty)
        s.render()
        self.assertFalse(s._is_dirty)
        s.handle_notification("unimportant")
        self.assertTrue(s._is_dirty)
        s.delete(0, 0)
        self.assertEqual(len(obj._observers), 0)


if __name__ == "__main__":
    unittest.main()
