from pygamelib import actuators, engine
from pygamelib import base
from pygamelib import board_items
from pygamelib import constants
from pygamelib.gfx import core
import unittest

# Test cases for all classes in pygamelib.gfx.core except for Animation.


class TestBase(unittest.TestCase):
    def test_game_create(self):
        def user_update_placeholder(p):
            pass

        self.assertIsInstance(
            engine.Game(user_update=user_update_placeholder), engine.Game
        )

    def test_run(self):
        def user_update_placeholder(g, i, dt):
            print("user_update_placeholder")
            self.assertGreater(dt, 0)
            if hasattr(g, "test_counter"):
                g.test_counter += 1
            else:
                g.test_counter = 1
            print(f"test_counter={g.test_counter}")
            if g.test_counter == 5:
                g.pause()
            elif g.test_counter > 10:
                g.stop()

        def user_update_paused_placeholder(g, i, dt):
            print("user_update_paused_placeholder")
            self.assertGreater(dt, 0)
            if hasattr(g, "test_counter"):
                g.test_counter += 1
            g.state = constants.RUNNING

        g = engine.Game()
        with self.assertRaises(base.PglInvalidTypeException) as e:
            g.run()
            self.assertTrue("undefined" in e.message)
        g = engine.Game(user_update=1)
        with self.assertRaises(base.PglInvalidTypeException) as e:
            g.run()
            self.assertTrue("callable" in e.message)
        g = engine.Game(
            user_update=user_update_placeholder,
            user_update_paused=user_update_paused_placeholder,
            mode=constants.MODE_RT,
        )
        self.assertIsNone(g.screen.display_line("testing the Game.run() mechanic."))
        g.run()
        g = engine.Game(
            user_update=user_update_placeholder,
            user_update_paused=user_update_paused_placeholder,
            mode=constants.MODE_RT,
        )
        g.player = board_items.Player()
        g.add_board(1, engine.Board())
        g.change_level(1)
        g.pause()
        g.run()
        self.assertTrue(g.player.dtmove > 0)
        # Now test the pause/resume mechanism without explicitly setting an update while
        # paused callback.
        g = engine.Game(
            user_update=user_update_placeholder,
            mode=constants.MODE_RT,
        )
        g.run()
        self.assertEqual(g.state, constants.STOPPED)

    def test_config(self):
        g = engine.Game()
        self.assertIsNone(g.create_config("high_scores"))
        g.config("high_scores")["first_place"] = "Test"
        self.assertEqual(g.config("high_scores")["first_place"], "Test")
        self.assertIsNone(
            g.save_config("high_scores", "test-pygamelib.engine.Game.config.json")
        )
        with self.assertRaises(base.PglInvalidTypeException):
            g.save_config(None, "test-pygamelib.engine.Game.config.json")
        with self.assertRaises(base.PglInvalidTypeException):
            g.save_config("high_scores", None)
        with self.assertRaises(base.PglException) as e:
            g.save_config("Unknown", "test-pygamelib.engine.Game.config.json")
        self.assertEqual(e.exception.error, "unknown section")
        # Don't do that...
        g._configuration = None
        g._configuration_internals = None
        g.load_config("test-pygamelib.engine.Game.config.json", "new_high_scores")
        self.assertIsNone(g.save_config("new_high_scores", None))
        self.assertIsNone(g.save_config("new_high_scores", None, True))

    def test_board_management(self):
        b = engine.Board()
        g = engine.Game(player=board_items.Player())
        self.assertIsNone(g.add_board(19, b))
        self.assertIsNone(g.change_level(19))
        self.assertIsNone(g.display_board())
        # Test display_board but with partial display on.
        g.enable_partial_display = True
        g.partial_display_viewport = [2, 2]
        g.partial_display_focus = board_items.Camera()
        self.assertIsNone(g.display_board())
        g.add_board(1, b)
        self.assertTrue(b.enable_partial_display)
        # Reset
        g = engine.Game()
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_board(1, 1)
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_board("1", 1)
        with self.assertRaises(base.PglInvalidTypeException):
            g.get_board("1")
        g.add_board(1, b)
        self.assertIsInstance(g.get_board(1), engine.Board)
        with self.assertRaises(base.PglInvalidLevelException):
            g.current_board()
        with self.assertRaises(base.PglException) as e:
            g.change_level(1)
        self.assertEqual(e.exception.error, "undefined_player")
        g.player = board_items.Player()
        self.assertIsNone(g.change_level(1))
        self.assertIsNone(g.add_board(2, engine.Board()))
        self.assertIsNone(g.change_level(2))
        self.assertIsNone(g.change_level(1))
        with self.assertRaises(base.PglInvalidLevelException):
            g.change_level(99)
        with self.assertRaises(base.PglInvalidTypeException):
            g.change_level("2")

    def test_npc_management(self):
        b = engine.Board()
        g = engine.Game()
        self.assertIsNone(g.add_board(1, b))
        npc = board_items.NPC(step=None)
        npc.step = None
        self.assertIsNone(g.add_npc(1, npc))
        self.assertEqual(npc.step, 1)
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_npc(1, board_items.NPC(step=None), "1")
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_npc(1, board_items.NPC(step=None), None, "1")
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_npc(1, board_items.NPC(step=None), 1, "1")
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_npc(1, board_items.NPC(step=None), "1", 1)
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_npc(1, 1)
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_npc("1", board_items.NPC())
        self.assertIsNone(g.actuate_npcs(1))
        g.mode = constants.MODE_RT
        self.assertIsNone(g.actuate_npcs(1))
        with self.assertRaises(base.PglInvalidLevelException):
            g.actuate_npcs(99)
        with self.assertRaises(base.PglInvalidTypeException):
            g.actuate_npcs("1")
        g.remove_npc(1, npc)

    def test_projectile_management(self):
        def _hit(p, t, ex):
            if len(ex) > 0:
                ex[0].stop()

        def _fake_hit(p, t, ex):
            pass

        def _upd(g, i, dt):
            pass

        b = engine.Board()
        g = engine.Game(user_update=_upd)
        g.player = constants.NO_PLAYER
        self.assertIsNone(g.add_board(1, b))
        g.change_level(1)
        p = board_items.Projectile(
            hit_model="*", hit_callback=_fake_hit, callback_parameters=[g]
        )
        p.actuator = None
        p.step = None
        self.assertIsNone(g.add_projectile(1, p, 1, 1))
        self.assertIsNone(g.add_projectile(1, board_items.Projectile(), 1, 100))
        b.place_item(board_items.Wall(), 5, 5)
        b.place_item(board_items.Wall(), 1, 3)
        p2 = board_items.Projectile(
            hit_model="*", hit_callback=_fake_hit, callback_parameters=[g]
        )
        p2.set_direction(constants.LEFT)
        g.add_projectile(1, p2, 1, 5)
        g.add_projectile(
            1,
            board_items.Projectile(
                hit_model="*", hit_callback=_hit, callback_parameters=[g]
            ),
            8,
            1,
        )
        g.add_projectile(
            1,
            board_items.Projectile(
                hit_model="*",
                hit_callback=_fake_hit,
                callback_parameters=[g],
                range=3,
                is_aoe=True,
            ),
            9,
            1,
        )
        g.add_projectile(
            1,
            board_items.Projectile(
                hit_model="*", hit_callback=_hit, callback_parameters=[g], range=-1
            ),
            9,
            1,
        )
        self.assertIsNone(
            g.add_projectile(1, board_items.Projectile(hit_callback=_hit), 5, 5)
        )
        self.assertIsNone(
            g.add_projectile(
                1, board_items.Projectile(hit_callback=_hit, is_aoe=True), 5, 5
            )
        )
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_projectile(1, board_items.Projectile(), "1")
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_projectile(1, board_items.Projectile(), None, "1")
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_projectile(1, board_items.Projectile(), 1, "1")
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_projectile(1, board_items.Projectile(), "1", 1)
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_projectile(1, 1)
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_projectile("1", board_items.NPC())
        self.assertIsNone(g.actuate_projectiles(1))
        g.mode = constants.MODE_RT
        g.start()
        self.assertIsNone(g.actuate_projectiles(1))
        with self.assertRaises(base.PglInvalidLevelException):
            g.actuate_projectiles(99)
        with self.assertRaises(base.PglInvalidTypeException):
            g.actuate_projectiles("1")
        g.actuate_projectiles(1)
        g.run()

    def test_projectile_hit(self):
        def _fake_hit(p, t, ex):
            pass

        def _upd(g: engine.Game, i, dt):
            self.assertIsNotNone(g.run_counter)
            if g.run_counter <= 3:
                p = board_items.Projectile(
                    hit_model="*",
                    hit_callback=_fake_hit,
                    callback_parameters=[g],
                    direction=constants.RIGHT,
                    is_aoe=True,
                    range=1,
                    movement_speed=0.05,
                )
                self.assertIsNone(g.add_projectile(1, p, 1, 6))
            if g.run_counter < 10:
                g.actuate_projectiles(1)
                g.run_counter += 1
            if g.run_counter >= 10:
                g.stop()

        b = engine.Board()
        g = engine.Game(user_update=_upd, mode=constants.MODE_RT)
        g.player = constants.NO_PLAYER
        setattr(g, "run_counter", 0)
        self.assertIsNone(g.add_board(1, b))
        self.assertEqual(g.run_counter, 0)
        g.change_level(1)
        p = board_items.Projectile(
            hit_model="*",
            hit_callback=_fake_hit,
            callback_parameters=[g],
            direction=constants.RIGHT,
        )
        self.assertIsNone(g.add_projectile(1, p, 1, 1))
        p2 = board_items.Projectile(
            hit_model="*",
            hit_callback=_fake_hit,
            callback_parameters=[g],
            direction=constants.RIGHT,
            is_aoe=True,
        )
        self.assertIsNone(g.add_projectile(1, p2, 2, 1))
        self.assertIsNone(g.add_projectile(1, board_items.Projectile(), 1, 100))
        self.assertIsNone(
            g.add_projectile(
                1,
                board_items.Projectile(
                    hit_model="*",
                    hit_callback=_fake_hit,
                    callback_parameters=[g],
                    direction=base.Vector2D(1, 1),
                    range=1000,
                    movement_speed=0.05,
                ),
                b.height - 1,
                b.width - 1,
            )
        )
        for r in range(0, 5):
            b.place_item(board_items.Wall(), r, 2)
        g.run()

    def test_tools_function(self):
        b = engine.Board()
        g = engine.Game()
        g.player = constants.NO_PLAYER
        self.assertIsNone(g.add_board(1, b))
        self.assertIsNone(g.change_level(1))
        self.assertIsNone(
            g.add_npc(1, board_items.NPC(value=10, inventory_space=1), 1, 1)
        )
        tmp_npc = g.get_board(1).item(1, 1)
        tmp_npc.actuator = actuators.PathFinder(game=g, actuated_object=tmp_npc)
        tmp_npc.actuator.set_destination(2, 5)
        tmp_npc.actuator.find_path()
        self.assertIsNone(
            b.place_item(board_items.Door(value=10, inventory_space=1), 1, 2)
        )
        self.assertIsNone(
            b.place_item(board_items.Wall(value=10, inventory_space=1), 1, 3)
        )
        self.assertIsNone(
            b.place_item(
                board_items.GenericStructure(value=10, inventory_space=1), 1, 4
            )
        )
        self.assertIsNone(
            b.place_item(
                board_items.GenericActionableStructure(value=10, inventory_space=1),
                1,
                5,
            )
        )
        self.assertIsNone(
            b.place_item(
                board_items.Door(
                    value=10, inventory_space=1, sprixel=core.Sprixel("#")
                ),
                2,
                2,
            )
        )
        self.assertIsNone(
            b.place_item(board_items.Treasure(value=10, inventory_space=1), 1, 6)
        )
        with self.assertRaises(base.PglInvalidTypeException):
            g.neighbors("2")

        with self.assertRaises(base.PglInvalidTypeException):
            g.neighbors(2, "crash")

        g.object_library.append(board_items.NPC())
        self.assertIsNone(g.save_board(1, "test-pygamelib.engine.Game.lvl1.json"))
        with self.assertRaises(base.PglInvalidTypeException):
            g.save_board("1", "test-pygamelib.engine.Game.lvl1.json")
        with self.assertRaises(base.PglInvalidTypeException):
            g.save_board(1, 1)
        with self.assertRaises(base.PglInvalidLevelException):
            g.save_board(11, "test-pygamelib.engine.Game.lvl1.json")
        self.assertIsInstance(
            g.load_board("test-pygamelib.engine.Game.lvl1.json", 1), engine.Board
        )
        self.assertEqual(g._string_to_constant("UP"), constants.UP)
        self.assertEqual(g._string_to_constant("DOWN"), constants.DOWN)
        self.assertEqual(g._string_to_constant("LEFT"), constants.LEFT)
        self.assertEqual(g._string_to_constant("RIGHT"), constants.RIGHT)
        self.assertEqual(g._string_to_constant("DRUP"), constants.DRUP)
        self.assertEqual(g._string_to_constant("DRDOWN"), constants.DRDOWN)
        self.assertEqual(g._string_to_constant("DLUP"), constants.DLUP)
        self.assertEqual(g._string_to_constant("DLDOWN"), constants.DLDOWN)

        with self.assertRaises(base.PglInvalidTypeException):
            g.delete_level()
        with self.assertRaises(base.PglInvalidLevelException):
            g.delete_level(42)
        g.delete_level(1)
        g.delete_all_levels()
        self.assertIsNone(g.current_board())
        bi = board_items.Door(
            value=10,
            inventory_space=0,
            pickable=False,
            overlappable=True,
            restorable=True,
        )
        obj = engine.Game._ref2obj(bi.serialize())
        self.assertIsInstance(obj, board_items.Door)
        bi = board_items.Treasure(
            value=10,
            inventory_space=0,
            pickable=False,
            overlappable=True,
            restorable=True,
        )
        obj = engine.Game._ref2obj(bi.serialize())
        self.assertIsInstance(obj, board_items.Treasure)
        bi = board_items.GenericActionableStructure(
            value=10,
            inventory_space=0,
            pickable=False,
            overlappable=True,
            restorable=True,
        )
        obj = engine.Game._ref2obj(bi.serialize())
        self.assertIsInstance(obj, board_items.GenericActionableStructure)
        bi = board_items.NPC(
            value=10,
            inventory_space=10,
            pickable=False,
            overlappable=True,
            restorable=True,
        )
        bi.actuator = actuators.PathActuator(path=[constants.UP])
        obj = engine.Game._ref2obj(bi.serialize())
        self.assertIsInstance(obj, board_items.NPC)
        bi.actuator = actuators.PatrolActuator(path=[constants.UP])
        obj = engine.Game._ref2obj(bi.serialize())
        self.assertIsInstance(obj.actuator, actuators.PatrolActuator)

    def test_singleton(self):
        mygame = engine.Game.instance()
        mygame.test_singleton = True
        self.assertTrue(engine.Game.instance(), "test_singleton")
        self.assertTrue(engine.Game.instance().test_singleton)
        self.assertTrue(mygame is engine.Game.instance())

    def test_logs(self):
        mygame = engine.Game.instance()
        mygame.ENABLE_SESSION_LOGS = True
        self.assertEqual(mygame.session_logs(), list())
        mygame.session_log("test")
        self.assertEqual(mygame.session_logs()[0], "test")
        mygame.clear_session_logs()
        self.assertEqual(mygame.session_logs(), list())

    def test_level_insertion(self):
        g = engine.Game.instance()
        g.insert_board(1, engine.Board(name="lvl1"))
        g.insert_board(2, engine.Board(name="lvl2"))
        g.insert_board(3, engine.Board(name="lvl3"))
        self.assertEqual(g.get_board(1).name, "lvl1")
        g.insert_board(1, engine.Board(name="lvl4"))
        self.assertEqual(g.get_board(1).name, "lvl4")
        self.assertEqual(g.get_board(2).name, "lvl1")
        g.insert_board(41, engine.Board(name="lvl41"))
        self.assertEqual(g.get_board(41).name, "lvl41")
        with self.assertRaises(base.PglInvalidTypeException):
            g.insert_board("1", engine.Board())
        with self.assertRaises(base.PglInvalidTypeException):
            g.insert_board(1, "engine.Board()")

    def test_animation_management(self):
        col = core.SpriteCollection()
        col.add(core.Sprite(name="s1"))
        col.add(core.Sprite(name="s2"))
        i = board_items.ComplexNPC(sprite=col["s1"])
        a = core.Animation(frames=col, parent=i)
        i.animation = a
        b = engine.Board(size=[10, 10])
        b.place_item(i, 0, 0)
        g = engine.Game(mode=constants.MODE_RT)
        g.add_board(1, b)
        g.state = constants.RUNNING
        g.animate_items(1, 0.01)
        self.assertEqual(i.sprite, col["s1"])
        g.animate_items(1, 3.0)
        self.assertEqual(i.sprite, col["s2"])
        with self.assertRaises(base.PglInvalidTypeException):
            g.animate_items("level one")
        with self.assertRaises(base.PglInvalidLevelException):
            g.animate_items(5)

    def test_base_object(self):
        obj = base.PglBaseObject()
        obj.store_screen_position(2, 4)
        self.assertEqual(obj.screen_row, 2)
        self.assertEqual(obj.screen_column, 4)


if __name__ == "__main__":
    unittest.main()
