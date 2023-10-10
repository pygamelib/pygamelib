from pygamelib.base import History
import unittest


class TestHistory(unittest.TestCase):

    # add action and get current action
    def test_add_action_and_get_current_action(self):
        history = History.instance()
        history.add("Action 1")
        self.assertEqual(history.current, "Action 1")

    # undo and redo actions
    def test_undo_and_redo_actions(self):
        history = History.instance()
        history.add("Action 1")
        history.add("Action 2")
        history.undo()
        self.assertEqual(history.current, "Action 1")
        history.redo()
        self.assertEqual(history.current, "Action 2")

    # reset history to initial state
    def test_reset_history(self):
        history = History.instance()
        history.add("Action 1")
        history.reset()
        self.assertIsNone(history.current)

    # undo when there are no past actions
    def test_undo_no_past_actions(self):
        history = History()
        history.undo()
        self.assertIsNone(history.current)

    # redo when there are no future actions
    def test_redo_no_future_actions(self):
        history = History()
        history.redo()
        self.assertIsNone(history.current)

    # add action after undoing past actions
    def test_add_action_after_undo(self):
        history = History.instance()
        history.add("Action 1")
        history.add("Action 2")
        history.undo()
        history.add("Action 3")
        self.assertEqual(history.current, "Action 3")
