from pygamelib import actuators
from pygamelib import constants
from pygamelib import board_items
from pygamelib import engine
import unittest

# Test cases for all classes in pygamelib.gfx.particles.
# WARNING: This module is under heavy work, it is not ready yet.
# Therefor tests cases are just covering the current state.


class TestBase(unittest.TestCase):
    def test_actuator(self):
        a = actuators.Actuator(None)
        self.assertIsNone(a.type)
        a.start()
        self.assertEqual(a.state, constants.RUNNING)
        a.pause()
        self.assertEqual(a.state, constants.PAUSED)
        a.stop()
        self.assertEqual(a.state, constants.STOPPED)
        with self.assertRaises(NotImplementedError):
            a.next_move()
        with self.assertRaises(NotImplementedError):
            a.serialize()
        with self.assertRaises(NotImplementedError):
            a.load()

    def test_behavioral(self):
        a = actuators.Behavioral(None)
        with self.assertRaises(NotImplementedError):
            a.next_action()

    def test_random(self):
        a = actuators.RandomActuator([constants.UP])
        self.assertEqual(a.moveset, [constants.UP])
        self.assertEqual(a.next_move(), constants.UP)
        data = a.serialize()
        self.assertEqual(data["moveset"], [constants.UP])
        al = actuators.RandomActuator.load(data)
        self.assertEqual(al.moveset, [constants.UP])
        self.assertEqual(al.moveset, a.moveset)

    def test_random_empty(self):
        a = actuators.RandomActuator()
        self.assertEqual(a.moveset, [])
        self.assertEqual(a.next_move(), constants.NO_DIR)

    def test_path(self):
        a = actuators.PathActuator([constants.UP])
        a.pause()
        self.assertEqual(a.next_move(), constants.NO_DIR)
        a.start()
        self.assertEqual(a.next_move(), constants.UP)
        a.set_path([constants.DOWN])
        self.assertEqual(a.next_move(), constants.DOWN)
        data = a.serialize()
        self.assertIsNotNone(data)
        self.assertEqual(data["path"], [constants.DOWN])
        al = actuators.PathActuator.load(data)
        self.assertEqual(al.path, [constants.DOWN])
        self.assertEqual(a.state, al.state)

    def test_patrol(self):
        a = actuators.PatrolActuator(path=[constants.UP, constants.DOWN])
        data = a.serialize()
        self.assertIsNotNone(data)
        self.assertEqual(data["path"], [constants.UP, constants.DOWN])
        al = actuators.PatrolActuator.load(data)
        self.assertEqual(al.path, [constants.UP, constants.DOWN])
        self.assertEqual(a.state, al.state)
        a.pause()
        self.assertEqual(a.next_move(), constants.NO_DIR)
        a.start()
        a.next_move()
        self.assertEqual(a.next_move(), constants.DOWN)
        self.assertEqual(a.next_move(), constants.UP)
        self.assertEqual(a.next_move(), constants.DOWN)
        a.set_path([constants.LEFT, constants.RIGHT])
        self.assertEqual(a.next_move(), constants.LEFT)
        self.assertEqual(a.next_move(), constants.RIGHT)
        self.assertEqual(a.next_move(), constants.LEFT)
        self.assertEqual(a.next_move(), constants.RIGHT)
        a.set_path([constants.DLDOWN, constants.DLUP, constants.DRDOWN, constants.DRUP])
        self.assertEqual(a.next_move(), constants.DLDOWN)
        self.assertEqual(a.next_move(), constants.DLUP)
        self.assertEqual(a.next_move(), constants.DRDOWN)
        self.assertEqual(a.next_move(), constants.DRUP)
        self.assertEqual(a.next_move(), constants.DLDOWN)
        self.assertEqual(a.next_move(), constants.DLUP)
        self.assertEqual(a.next_move(), constants.DRDOWN)
        self.assertEqual(a.next_move(), constants.DRUP)

    def test_unidirectional(self):
        a = actuators.UnidirectionalActuator()
        self.assertEqual(a.next_move(), constants.RIGHT)
        a = actuators.UnidirectionalActuator(direction=None)
        self.assertEqual(a.next_move(), constants.RIGHT)
        data = a.serialize()
        self.assertIsNotNone(data)
        self.assertEqual(data["direction"], constants.RIGHT)
        al = actuators.UnidirectionalActuator.load(data)
        self.assertEqual(al.direction, constants.RIGHT)
        self.assertEqual(a.state, al.state)

    def test_pathfinder_bfs(self):
        npc = board_items.NPC()
        b = engine.Board()
        g = engine.Game()
        g.player = board_items.Player()
        g.add_board(1, b)
        g.add_npc(1, npc, 5, 5)
        g.change_level(1)
        actuators.PathFinder(actuated_object=npc)
        npc.actuator = actuators.PathFinder(parent=npc, game=g, circle_waypoints=False)
        with self.assertRaises(engine.base.PglInvalidTypeException):
            actuators.PathFinder(
                parent=npc,
                game=g,
                circle_waypoints=False,
                algorithm="constants.ALGO_BFS",
            )
        npc.actuator.set_destination(2, 2)
        npc.actuator.find_path()
        self.assertTrue(len(npc.actuator.current_path()) > 0)
        with self.assertRaises(engine.base.PglInvalidTypeException):
            npc.actuator.set_destination("2", 2)
        npc.actuator.actuated_object = None
        with self.assertRaises(engine.base.PglException) as e:
            npc.actuator.find_path()
            self.assertEqual(e.error, "actuated_object is not defined")
        npc.actuator.actuated_object = board_items.Door()
        with self.assertRaises(engine.base.PglException) as e:
            npc.actuator.find_path()
            self.assertEqual(e.error, "actuated_object not a Movable object")
        npc.actuator.actuated_object = board_items.Door()
        npc.actuator.actuated_object = npc
        npc.actuator.destination = None
        with self.assertRaises(engine.base.PglException) as e:
            npc.actuator.find_path()
            self.assertEqual(e.error, "destination is not defined")
        b.place_item(board_items.Wall(), 2, 2)
        npc.actuator.set_destination(2, 2)
        self.assertEqual(npc.actuator.find_path(), [])
        # These tests are a recipe of how to NOT do things...
        npc.actuator.destination = (None, None)
        self.assertEqual(npc.actuator.next_move(), constants.NO_DIR)
        npc.actuator.set_destination(5, 5)
        npc.actuator._current_path = []
        npc.actuator.next_move()
        npc.actuator.set_destination(2, 5)
        npc.actuator._current_path = []
        nm = npc.actuator.next_move()
        self.assertEqual(nm, constants.UP)
        npc.actuator.add_waypoint(5, 6)
        npc.actuator.add_waypoint(6, 6)
        npc.actuator.add_waypoint(5, 4)
        npc.actuator.add_waypoint(4, 6)
        nm = None
        while nm != constants.NO_DIR:
            nm = npc.actuator.next_move()
            b.move(npc, nm, npc.step)
        with self.assertRaises(engine.base.PglInvalidTypeException):
            npc.actuator.add_waypoint(5, "6")
        with self.assertRaises(engine.base.PglInvalidTypeException):
            npc.actuator.add_waypoint("5", 6)
        npc.actuator.clear_waypoints()
        self.assertEqual(npc.actuator.next_waypoint(), (None, None))
        npc.actuator.clear_waypoints()
        npc.actuator.destination = (None, None)
        npc.actuator.add_waypoint(10, 10)
        npc.actuator.add_waypoint(12, 15)
        self.assertEqual(npc.actuator.destination, (10, 10))
        self.assertEqual(npc.actuator.next_waypoint(), (10, 10))
        self.assertEqual(npc.actuator.next_waypoint(), (12, 15))
        self.assertEqual(npc.actuator.next_waypoint(), (None, None))
        npc.actuator.circle_waypoints = True
        self.assertEqual(npc.actuator.next_waypoint(), (10, 10))
        with self.assertRaises(engine.base.PglInvalidTypeException):
            npc.actuator.remove_waypoint(10, "10")
        with self.assertRaises(engine.base.PglInvalidTypeException):
            npc.actuator.remove_waypoint("10", 10)
        with self.assertRaises(engine.base.PglException) as e:
            npc.actuator.remove_waypoint(30, 30)
            self.assertEqual(e.error, "invalid_waypoint")
        self.assertIsNone(npc.actuator.remove_waypoint(10, 10))

    def test_pathfinder_astar(self):
        npc = board_items.NPC()
        b = engine.Board()
        g = engine.Game()
        g.player = board_items.Player()
        g.add_board(1, b)
        g.add_npc(1, npc, 5, 5)
        g.change_level(1)
        actuators.PathFinder(actuated_object=npc)
        npc.actuator = actuators.PathFinder(
            parent=npc, game=g, circle_waypoints=False, algorithm=constants.ALGO_ASTAR
        )
        with self.assertRaises(engine.base.PglInvalidTypeException):
            actuators.PathFinder(
                parent=npc,
                game=g,
                circle_waypoints=False,
                algorithm="constants.ALGO_ASTAR",
            )
        npc.actuator.set_destination(2, 2)
        npc.actuator.find_path()
        self.assertTrue(len(npc.actuator.current_path()) > 0)

        with self.assertRaises(engine.base.PglInvalidTypeException):
            npc.actuator.set_destination("2", 2)
        npc.actuator.actuated_object = None
        with self.assertRaises(engine.base.PglException) as e:
            npc.actuator.find_path()
            self.assertEqual(e.error, "actuated_object is not defined")
        npc.actuator.actuated_object = board_items.Door()
        with self.assertRaises(engine.base.PglException) as e:
            npc.actuator.find_path()
            self.assertEqual(e.error, "actuated_object not a Movable object")
        npc.actuator.actuated_object = npc
        npc.actuator.destination = None
        with self.assertRaises(engine.base.PglException) as e:
            npc.actuator.find_path()
            self.assertEqual(e.error, "destination is not defined")
        b.place_item(board_items.Wall(), 2, 2)
        npc.actuator.set_destination(2, 2)
        self.assertEqual(npc.actuator.find_path(), [])
        # These tests are a recipe of how to NOT do things...
        npc.actuator.destination = (None, None)
        self.assertEqual(npc.actuator.next_move(), constants.NO_DIR)
        npc.actuator.set_destination(5, 5)
        npc.actuator._current_path = []
        npc.actuator.next_move()
        npc.actuator.set_destination(2, 5)
        npc.actuator._current_path = []
        nm = npc.actuator.next_move()
        self.assertEqual(nm, constants.UP)
        npc.actuator.add_waypoint(5, 6)
        npc.actuator.add_waypoint(6, 6)
        npc.actuator.add_waypoint(5, 4)
        npc.actuator.add_waypoint(4, 6)
        nm = None
        while nm != constants.NO_DIR:
            nm = npc.actuator.next_move()
            b.move(npc, nm, npc.step)
        with self.assertRaises(engine.base.PglInvalidTypeException):
            npc.actuator.add_waypoint(5, "6")
        with self.assertRaises(engine.base.PglInvalidTypeException):
            npc.actuator.add_waypoint("5", 6)
        npc.actuator.clear_waypoints()
        self.assertEqual(npc.actuator.next_waypoint(), (None, None))
        npc.actuator.clear_waypoints()
        npc.actuator.destination = (None, None)
        npc.actuator.add_waypoint(10, 10)
        npc.actuator.add_waypoint(12, 15)
        self.assertEqual(npc.actuator.destination, (10, 10))
        self.assertEqual(npc.actuator.next_waypoint(), (10, 10))
        self.assertEqual(npc.actuator.next_waypoint(), (12, 15))
        self.assertEqual(npc.actuator.next_waypoint(), (None, None))
        npc.actuator.circle_waypoints = True
        self.assertEqual(npc.actuator.next_waypoint(), (10, 10))
        with self.assertRaises(engine.base.PglInvalidTypeException):
            npc.actuator.remove_waypoint(10, "10")
        with self.assertRaises(engine.base.PglInvalidTypeException):
            npc.actuator.remove_waypoint("10", 10)
        with self.assertRaises(engine.base.PglException) as e:
            npc.actuator.remove_waypoint(30, 30)
            self.assertEqual(e.error, "invalid_waypoint")
        self.assertIsNone(npc.actuator.remove_waypoint(10, 10))

    def test_pathfinder_serialization(self):
        a = actuators.PathFinder(parent=board_items.NPC())
        a.add_waypoint(1, 2)
        data = a.serialize()
        self.assertIsNotNone(data)
        self.assertEqual(data["waypoints"], [(1, 2)])
        al = actuators.PathFinder.load(data)
        self.assertEqual(al.waypoints, [(1, 2)])
        self.assertEqual(a.state, al.state)
        self.assertEqual(a.destination, al.destination)


if __name__ == "__main__":
    unittest.main()
