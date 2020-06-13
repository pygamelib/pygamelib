from gamelib.Animation import Animation
from gamelib.Characters import NPC
import gamelib.Constants as Constants
import unittest


class TestAnimation(unittest.TestCase):
    def redraw(self):
        pass

    def test_create_animation(self):
        self.item = NPC(model="-o-", name="Dancer")
        self.animation = Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.assertEqual(self.item.name, self.animation.parent.name)

    def test_start(self):
        self.item = NPC(model="-o-", name="Dancer")
        self.animation = Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.animation.start()
        self.assertEqual(self.animation.state, Constants.RUNNING)

    def test_pause(self):
        self.item = NPC(model="-o-", name="Dancer")
        self.animation = Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.animation.pause()
        self.assertEqual(self.animation.state, Constants.PAUSED)

    def test_stop(self):
        self.item = NPC(model="-o-", name="Dancer")
        self.animation = Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.animation.stop()
        self.assertEqual(self.animation.state, Constants.STOPPED)

    def test_add_frame(self):
        self.item = NPC(model="-o-", name="Dancer")
        self.animation = Animation(
            parent=self.item, refresh_screen=self.redraw, display_time=0.5
        )
        self.animation.add_frame("\\o-")
        with self.assertRaises(Exception) as context:
            self.animation.add_frame(2)
        self.assertTrue("must be a string" in str(context.exception))

    def test_search_frame(self):
        self.item = NPC(model="-o-", name="Dancer")
        self.animation = Animation(
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
        self.item = NPC(model="-o-", name="Dancer")
        self.animation = Animation(
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

    def test_current_frame(self):
        self.item = NPC(model="-o-", name="Dancer")
        self.animation = Animation(
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
        self.item = NPC(model="-o-", name="Dancer")
        self.animation = Animation(
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
        self.animation.parent = "This is going to break!"
        with self.assertRaises(Exception) as context:
            self.animation.next_frame()
        self.assertTrue(
            "needs to be a sub class of BoardItem" in str(context.exception)
        )

    def test_play_all(self):
        self.item = NPC(model="-o-", name="Dancer")
        self.animation = Animation(
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
        self.animation = Animation(
            parent="breaking", refresh_screen=self.redraw, display_time=0.5
        )
        with self.assertRaises(Exception) as context:
            self.animation.play_all()
        self.assertTrue(
            "needs to be a sub class of BoardItem" in str(context.exception)
        )

        self.animation = Animation(
            parent=self.item, refresh_screen="breaking", display_time=0.5
        )
        with self.assertRaises(Exception) as context:
            self.animation.play_all()
        self.assertTrue(
            "needs to be a callback function reference" in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
