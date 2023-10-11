from pygamelib.gfx.ui import Widget, UiConfig, GridLayout
from pygamelib import engine
import unittest


class TestGridLayout(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.game = engine.Game.instance()
        self.game.screen = engine.Screen(50, 50)
        self.ui_config = UiConfig.instance(game=self.game)

    # Add a widget to the grid layout
    def test_add_widget_to_grid_layout(self):
        layout = GridLayout()
        widget = Widget()
        self.assertTrue(layout.add_widget(widget))
        self.assertEqual(layout.count(), 1)
        self.assertEqual(layout.widgets(), {widget})

    # Set row minimum height
    def test_set_row_minimum_height(self):
        layout = GridLayout()
        layout.row_minimum_height = 10
        self.assertEqual(layout.row_minimum_height, 10)

    # Set column minimum width
    def test_set_column_minimum_width(self):
        layout = GridLayout()
        layout.column_minimum_width = 20
        self.assertEqual(layout.column_minimum_width, 20)

    # Add widget with row greater than or equal to number of rows
    def test_add_widget_with_greater_row(self):
        layout = GridLayout()
        widget = Widget()
        layout.add_widget(widget, row=1)
        self.assertEqual(layout.count_rows(), 1)

    # Add widget with column greater than or equal to number of columns
    def test_add_widget_with_greater_column(self):
        layout = GridLayout()
        widget = Widget()
        layout.add_widget(widget, column=1)
        self.assertEqual(layout.count_columns(), 1)

    # Add widget that exceeds grid layout size
    def test_add_widget_exceeding_size(self):
        layout = GridLayout()
        widget = Widget(width=10, height=10)
        layout.row_minimum_height = 5
        layout.column_minimum_width = 5
        self.assertTrue(layout.add_widget(widget, row=1, column=1))
        self.assertEqual(layout.count(), 1)

    # test the spacing properties
    def test_spacing_properties(self):
        layout = GridLayout()
        layout.spacing = 10
        self.assertEqual(layout.spacing, 10)
        self.assertEqual(layout.horizontal_spacing, 10)
        self.assertEqual(layout.vertical_spacing, 10)

        layout.horizontal_spacing = 5
        self.assertEqual(layout.spacing, -1)
        self.assertEqual(layout.horizontal_spacing, 5)
        self.assertEqual(layout.vertical_spacing, 10)

        layout.vertical_spacing = 7
        self.assertEqual(layout.spacing, -1)
        self.assertEqual(layout.horizontal_spacing, 5)
        self.assertEqual(layout.vertical_spacing, 7)

    # test that if you add 3 widgets to the GridLayout over 2 rows, then when you add a
    # fourth widget it will occupy cell (3,3)
    def test_add_fourth_widget(self):
        layout = GridLayout()
        widget1 = Widget()
        widget2 = Widget()
        widget3 = Widget()
        layout.add_widget(widget1, row=0, column=0)
        layout.add_widget(widget2, row=0, column=1)
        layout.add_widget(widget3, row=1, column=0)
        widget4 = Widget()
        layout.add_widget(widget4)
        self.assertEqual(layout.count_rows(), 2)
        self.assertEqual(layout.count_columns(), 2)
        self.assertEqual(layout.count(), 4)
        self.assertEqual(layout.widgets(), {widget1, widget2, widget3, widget4})

    # test that when add_widget() is used without a widget, it returns false
    def test_add_widget_without_widget_returns_false(self):
        layout = GridLayout()
        result = layout.add_widget(None)
        self.assertFalse(result)

    # test that when adding a widget with a bigger height than existing widgets in a
    # row, the add_widget function still return true
    def test_add_widget_with_bigger_height(self):
        layout = GridLayout()
        widget1 = Widget(height=10)
        widget2 = Widget(height=15)
        layout.add_widget(widget1, row=0, column=0)
        result = layout.add_widget(widget2, row=0, column=1)
        self.assertTrue(result)

    # test the rendering loop
    def test_render_loop(self):
        layout = GridLayout()
        widget1 = Widget(10, 10)
        widget2 = Widget(20, 20)
        layout.add_widget(widget1)
        layout.add_widget(widget2)

        self.assertIsNone(
            layout.render_to_buffer(self.game.screen.buffer, 0, 0, 30, 30)
        )

        self.assertEqual(widget1.screen_row, 0)
        self.assertEqual(widget1.screen_column, 0)
        self.assertEqual(widget2.screen_row, 10)
        self.assertEqual(widget2.screen_column, 0)
        self.assertEqual(layout.width, 20)
        self.assertEqual(layout.height, 30)

        # Test widget culling by giving a smaller area to render into
        self.assertIsNone(
            layout.render_to_buffer(self.game.screen.buffer, 0, 0, 10, 10)
        )

    # test the rendering loop with an empty cell between two widgets
    def test_render_loop_with_empty_cell(self):
        layout = GridLayout()
        widget1 = Widget(10, 10)
        widget2 = Widget(20, 20)
        layout.add_widget(widget1, 0, 0)
        layout.add_widget(widget2, row=0, column=2)

        self.assertIsNone(
            layout.render_to_buffer(self.game.screen.buffer, 0, 0, 30, 30)
        )

        self.assertEqual(widget1.screen_row, 0)
        self.assertEqual(widget1.screen_column, 0)
        self.assertEqual(widget2.screen_row, 0)
        self.assertEqual(widget2.screen_column, 10)
        self.assertEqual(layout.width, 30)
        self.assertEqual(layout.height, 20)

        # Test widget culling by giving a smaller area to render into
        self.assertIsNone(
            layout.render_to_buffer(self.game.screen.buffer, 0, 0, 10, 10)
        )

    # test the handle_notification method
    def test_handle_notification(self):
        layout = GridLayout()
        widget = Widget()
        layout.add_widget(widget, row=0, column=0)
        widget.height = 10
        layout.handle_notification(
            widget, attribute="pygamelib.gfx.ui.Widget.resizeEvent:height", value=10
        )
        self.assertEqual(layout._GridLayout__rows_geometry[0], 10)
