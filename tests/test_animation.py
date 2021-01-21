import pygamelib.gfx.core as gfx_core
import pygamelib.base as pgl_base
import pygamelib.board_items as pgl_board_items
import pygamelib.constants as pgl_constants
import pygamelib.engine as pgl_engine
import unittest


class TestAnimation(unittest.TestCase):
    def redraw(self):
        pass

    def test_create_animation(self):
        self.item = pgl_board_items.NPC(model="-o-", name="Dancer")
        self.animation = gfx_core.Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.assertEqual(self.item.name, self.animation.parent.name)
        a = gfx_core.Animation(
            animated_object=self.item,
            refresh_screen=self.redraw,
            display_time=0.5,
            initial_index=2,
        )
        self.assertEqual(a._initial_index, 2)
        a.reset()
        self.assertEqual(a._initial_index, a._frame_index)
        col = gfx_core.SpriteCollection()
        col.add(gfx_core.Sprite(name="s1"))
        col.add(gfx_core.Sprite(name="s2"))
        i = pgl_board_items.ComplexNPC(sprite=col["s1"])
        a = gfx_core.Animation(frames=col, parent=i)
        i.animation = a
        self.assertIsInstance(a, gfx_core.Animation)
        self.assertEqual(len(a.frames), 2)
        # I shouldn't test that here but I'm tired of writting test!
        self.assertIsInstance(a.next_frame(), gfx_core.Sprite)

    def test_start(self):
        self.item = pgl_board_items.NPC(model="-o-", name="Dancer")
        self.animation = gfx_core.Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.animation.start()
        self.assertEqual(self.animation.state, pgl_constants.RUNNING)

    def test_pause(self):
        self.item = pgl_board_items.NPC(model="-o-", name="Dancer")
        self.animation = gfx_core.Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.animation.pause()
        self.assertEqual(self.animation.state, pgl_constants.PAUSED)

    def test_stop(self):
        self.item = pgl_board_items.NPC(model="-o-", name="Dancer")
        self.animation = gfx_core.Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.animation.stop()
        self.assertEqual(self.animation.state, pgl_constants.STOPPED)

    def test_add_frame(self):
        self.item = pgl_board_items.NPC(model="-o-", name="Dancer")
        self.animation = gfx_core.Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.animation.add_frame("\\o-")
        with self.assertRaises(Exception) as context:
            self.animation.add_frame(2)
        self.assertTrue("must be a string" in str(context.exception))

    def test_search_frame(self):
        self.item = pgl_board_items.NPC(model="-o-", name="Dancer")
        self.animation = gfx_core.Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.animation.add_frame("-o-")
        self.animation.add_frame("\\o-")
        self.animation.add_frame("\\o-")
        self.assertEqual(self.animation.search_frame("\\o-"), 1)
        self.assertNotEqual(self.animation.search_frame("\\o-"), 2)
        with self.assertRaises(Exception) as context:
            self.animation.search_frame(2)
        self.assertTrue("must be a string" in str(context.exception))

    def test_remove_frame(self):
        self.item = pgl_board_items.NPC(model="-o-", name="Dancer")
        self.animation = gfx_core.Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.animation.add_frame("-o-")
        self.animation.add_frame("\\o-")
        self.animation.add_frame("\\o\\")
        self.animation.add_frame("|o|")
        self.animation.add_frame("/o/")
        self.animation.add_frame("-o/")
        with self.assertRaises(Exception) as context:
            self.animation.remove_frame(999)
        self.assertTrue("out of range" in str(context.exception))
        self.assertEqual(self.animation.remove_frame(0), "-o-")
        self.animation.next_frame()
        self.animation.next_frame()
        self.assertEqual(self.animation.remove_frame(2), "|o|")
        self.assertEqual(self.animation.current_frame(), "\\o\\")
        self.assertEqual(self.animation.next_frame(), "/o/")
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            self.animation.remove_frame("999")

    def test_current_frame(self):
        self.item = pgl_board_items.NPC(model="-o-", name="Dancer")
        self.animation = gfx_core.Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.animation.add_frame("-o-")
        self.animation.add_frame("\\o-")
        self.animation.add_frame("\\o\\")
        self.animation.add_frame("|o|")
        self.assertEqual(self.animation.current_frame(), "-o-")
        self.animation.next_frame()
        self.assertEqual(self.animation.current_frame(), "\\o-")

    def test_next_frame(self):
        self.item = pgl_board_items.NPC(model="-o-", name="Dancer")
        self.animation = gfx_core.Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.animation.add_frame("-o-")
        self.animation.add_frame("\\o-")
        self.animation.add_frame("\\o\\")
        self.animation.add_frame("|o|")
        self.assertEqual(self.animation.next_frame(), "\\o-")
        self.animation.pause()
        self.assertEqual(self.animation.next_frame(), "\\o-")
        self.animation.stop()
        self.assertIsNone(self.animation.next_frame())
        self.animation.start()
        self.animation.next_frame()
        self.animation.next_frame()
        self.animation.next_frame()
        self.animation.reset()
        self.animation.auto_replay = False
        self.animation.next_frame()
        self.animation.next_frame()
        self.animation.next_frame()
        self.animation.next_frame()
        self.animation.next_frame()
        self.assertEqual(self.animation._frame_index, 3)
        self.animation.parent = "This is going to break!"
        with self.assertRaises(Exception) as context:
            self.animation.next_frame()
        self.assertTrue(
            "needs to be a sub class of BoardItem" in str(context.exception)
        )

    def test_play_all(self):
        self.item = pgl_board_items.NPC(model="-o-", name="Dancer")
        self.animation = gfx_core.Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.animation.add_frame("-o-")
        self.animation.add_frame("\\o-")
        self.animation.add_frame("\\o\\")
        self.animation.add_frame("|o|")
        self.assertTrue(self.animation.play_all())
        self.animation.pause()
        self.assertFalse(self.animation.play_all())
        self.animation.stop()
        self.assertFalse(self.animation.play_all())
        self.animation = gfx_core.Animation(
            parent="breaking", refresh_screen=self.redraw, display_time=0.5
        )
        with self.assertRaises(Exception) as context:
            self.animation.play_all()
        self.assertTrue(
            "needs to be a sub class of BoardItem" in str(context.exception)
        )

        self.animation = gfx_core.Animation(
            parent=self.item, refresh_screen="breaking", display_time=0.5
        )
        with self.assertRaises(Exception) as context:
            self.animation.play_all()
        self.assertTrue(
            "needs to be a callback function reference" in str(context.exception)
        )

    def test_with_sprixel(self):
        i = pgl_board_items.NPC(sprixel=gfx_core.Sprixel())
        i.animation = gfx_core.Animation(parent=i)
        i.animation.add_frame(gfx_core.Sprixel("-"))
        i.animation.add_frame(gfx_core.Sprixel("+"))
        self.assertIsInstance(i.animation, gfx_core.Animation)
        self.assertEqual(len(i.animation.frames), 2)
        # I shouldn't test that here but I'm tired of writting test!
        self.assertIsInstance(i.animation.next_frame(), gfx_core.Sprixel)
        i.animation.frames[1] = pgl_base.Vector2D()
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            i.animation.next_frame()
            i.animation.next_frame()

    def test_with_sprite(self):
        spr = gfx_core.Sprite(
            sprixels=[
                [
                    gfx_core.Sprixel.cyan_rect(),
                    gfx_core.Sprixel.red_rect(),
                    gfx_core.Sprixel.green_rect(),
                ],
                [
                    gfx_core.Sprixel.yellow_rect(),
                    gfx_core.Sprixel.blue_rect(),
                    gfx_core.Sprixel.white_rect(),
                ],
            ]
        )
        blue_spr = gfx_core.Sprite(
            sprixels=[
                [
                    gfx_core.Sprixel.blue_rect(),
                    gfx_core.Sprixel.blue_rect(),
                    gfx_core.Sprixel.blue_rect(),
                ],
                [
                    gfx_core.Sprixel.blue_rect(),
                    gfx_core.Sprixel.blue_rect(),
                    gfx_core.Sprixel.blue_rect(),
                ],
            ]
        )
        red_spr = gfx_core.Sprite(
            sprixels=[
                [
                    gfx_core.Sprixel.red_rect(),
                    gfx_core.Sprixel.red_rect(),
                    gfx_core.Sprixel.red_rect(),
                ],
                [
                    gfx_core.Sprixel.red_rect(),
                    gfx_core.Sprixel.red_rect(),
                    gfx_core.Sprixel.red_rect(),
                ],
            ]
        )
        b = pgl_engine.Board(size=[30, 30])
        i = pgl_board_items.ComplexNPC(sprite=spr, parent=b)
        i.animation = gfx_core.Animation(
            parent=i, refresh_screen=self.redraw, display_time=0.1
        )
        i.animation.add_frame(blue_spr)
        i.animation.add_frame(red_spr)
        b.place_item(i, 2, 2)
        self.assertTrue(i.animation.play_all())
        # Now with Game
        g = pgl_engine.Game()
        g.add_board(1, b)
        g.player = pgl_constants.NO_PLAYER
        g.change_level(1)
        i = pgl_board_items.ComplexNPC(sprite=spr, parent=g)
        i.animation = gfx_core.Animation(
            parent=i, refresh_screen=self.redraw, display_time=0.1
        )
        i.animation.add_frame(blue_spr)
        i.animation.add_frame(red_spr)
        # b.place_item(i, 2, 2)
        self.assertIsNone(i.animation.play_all())

    def test_dtdisplay(self):
        a = gfx_core.Animation()
        a.dtanimate = 1.0
        self.assertEqual(a.dtanimate, 1.0)
        a.dtanimate = 1
        self.assertEqual(a.dtanimate, 1)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            a.dtanimate = "1.0"


if __name__ == "__main__":
    unittest.main()
