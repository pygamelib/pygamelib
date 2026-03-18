"""
Comprehensive unit tests for the Frame widget.
"""

import unittest
from pygamelib.gfx.ui import Frame, UiConfig, BoxLayout, LineInput
from pygamelib.gfx.core import Color, Sprixel
from pygamelib.engine import Game, Screen
from pygamelib import constants
from pygamelib import base


class TestFrame(unittest.TestCase):
    """Extended test suite for the Frame widget."""

    def setUp(self):
        """Common setup before each test."""
        self.game = Game.instance()
        self.screen = Screen(60, 25)
        self.game.screen = self.screen
        self.config = UiConfig.instance(game=self.game)

    def test_basic_frame_creation(self):
        """Test basic frame creation and rendering."""
        frame = Frame(width=30, height=8, title="Test Frame", config=self.config)
        self.assertEqual(frame.width, 30)
        self.assertEqual(frame.height, 8)
        self.assertEqual(frame.title, "Test Frame")

        # Rendering shouldn’t raise an error
        self.screen.place(frame, 5, 5)
        self.screen.update()

    def test_frame_with_fill(self):
        """Test frame with fill property."""
        frame = Frame(width=25, height=6, title="Filled", config=self.config, fill=True)
        self.assertTrue(frame.fill)
        self.screen.place(frame, 2, 2)
        self.screen.update()

    def test_frame_property_changes(self):
        """Test changing frame properties."""
        frame = Frame(width=20, height=5, title="Original", config=self.config)
        frame.title = "Modified"
        self.assertEqual(frame.title, "Modified")

        frame.width = 35
        frame.height = 10
        self.assertEqual(frame.width, 35)
        self.assertEqual(frame.height, 10)

        frame.fill = True
        self.assertTrue(frame.fill)

    def test_frame_with_layout_and_widgets(self):
        """Test frame with BoxLayout and child widgets."""
        frame = Frame(width=50, height=15, title="Form Frame", config=self.config)
        frame.layout = BoxLayout(orientation=constants.Orientation.VERTICAL)

        input1 = LineInput("First field", config=self.config, maximum_width=40)
        input2 = LineInput("Second field", config=self.config, maximum_width=40)
        frame.layout.add_widget(input1)
        frame.layout.add_widget(input2)

        self.assertIsNotNone(frame.layout)
        self.assertEqual(frame.layout.count(), 2)

        self.screen.place(frame, 3, 3)
        self.screen.update()

    def test_frame_rendering_on_screen(self):
        """Test multiple frames rendering on screen."""
        frame1 = Frame(width=25, height=8,
                       title="Frame 1",
                       config=self.config)
        frame2 = Frame(width=25, height=8,
                       title="Frame 2", config=self.config,
                       fill=True)

        self.screen.place(frame1, 2, 2)
        self.screen.place(frame2, 2, 30)
        self.screen.update()

        self.assertEqual(frame1.title, "Frame 1")
        self.assertEqual(frame2.title, "Frame 2")

    def test_frame_widget_constraints(self):
        """Test that Frame respects Widget constraints."""
        frame = Frame(
            width=20,
            height=10,
            minimum_width=10,
            minimum_height=5,
            maximum_width=50,
            maximum_height=30,
            config=self.config,
        )

        self.assertEqual(frame.minimum_width, 10)
        self.assertEqual(frame.minimum_height, 5)
        self.assertEqual(frame.maximum_width, 50)
        self.assertEqual(frame.maximum_height, 30)

        # Check clamping
        frame.width = 5
        self.assertEqual(frame.width, 10)  # minimum clamp

        frame.width = 100
        self.assertEqual(frame.width, 50)  # maximum clamp

    # ----------------- Additional Comprehensive Tests -----------------

    def test_title_alignment_and_colors(self):
        """Test title alignment and custom colors."""
        frame = Frame(
            width=30,
            height=10,
            title="Aligned Frame",
            config=self.config,
            title_alignment=constants.Alignment.RIGHT,
            bg_color=Color(10, 10, 10),
        )
        self.assertEqual(frame.title, "Aligned Frame")
        self.assertEqual(frame._Frame__title_alignment, constants.Alignment.RIGHT)
        self.assertIsInstance(frame.ui_config, UiConfig)

    def test_filling_sprixel_usage(self):
        """Test frame creation with a filling sprixel."""
        sprixel = Sprixel(
            model="*",
            fg_color=Color(255, 255, 0),
            bg_color=Color(0, 0, 0)
        )
        frame = Frame(width=15, height=6,
                      fill=True, filling_sprixel=sprixel,
                      config=self.config)
        self.assertEqual(frame.filling_sprixel, sprixel)
        self.assertTrue(frame.fill)

    def test_invalid_title_type_raises_exception(self):
        """Frame.title must be str or Text."""
        frame = Frame(config=self.config)
        with self.assertRaises(base.PglInvalidTypeException):
            frame.title = 123  # invalid type

    def test_repr_returns_expected_string(self):
        """Test __repr__ output."""
        frame = Frame(width=10, height=5, title="Box", config=self.config)
        rep = repr(frame)
        self.assertIn("Frame", rep)
        self.assertIn("Box", rep)

    def test_post_processing_updates_box(self):
        """Ensure post_processing correctly syncs Box dimensions."""
        frame = Frame(width=10, height=5, title="Sync", config=self.config)
        frame.width = 20
        frame.post_processing("width")
        self.assertEqual(frame._Frame__box.width, 20)

    def test_resize_and_rerender(self):
        """Frame should re-render cleanly after resize."""
        frame = Frame(width=15, height=6, title="Resize", config=self.config)
        self.screen.place(frame, 4, 4)
        self.screen.update()

        # Resize and render again
        frame.width = 25
        frame.height = 10
        self.screen.place(frame, 4, 4)
        self.screen.update()

        self.assertEqual(frame.width, 25)
        self.assertEqual(frame.height, 10)

    def test_layout_rendering_offset(self):
        """Ensure layout content is drawn inside borders."""
        frame = Frame(width=30, height=10, title="Offset", config=self.config)
        layout = BoxLayout(orientation=constants.Orientation.VERTICAL)
        layout.add_widget(LineInput("Field 1", config=self.config))
        frame.layout = layout
        self.screen.place(frame, 1, 1)
        self.screen.update()

        self.assertIsNotNone(frame.layout)
        self.assertEqual(frame.layout.count(), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=False, failfast=False)
