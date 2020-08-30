from pygamelib import engine
from pygamelib import base
from pygamelib import board_items
from pygamelib import constants
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
            self.assertGreater(dt, 0)
            g.stop()

        g = engine.Game()
        with self.assertRaises(base.PglInvalidTypeException) as e:
            g.run()
            self.assertTrue("undefined" in e.message)
        g = engine.Game(user_update=1)
        with self.assertRaises(base.PglInvalidTypeException) as e:
            g.run()
            self.assertTrue("callable" in e.message)
        g = engine.Game(user_update=user_update_placeholder, mode=constants.MODE_RT)
        g.pause()
        self.assertIsNone(g.screen.display_line("testing the Game.run() mechanic."))
        g.run()
        g = engine.Game(user_update=user_update_placeholder, mode=constants.MODE_RT)
        g.player = board_items.Player()
        g.pause()
        g.run()

    def test_menu(self):
        game = engine.Game()
        self.assertIsNone(
            game.add_menu_entry("main_menu", "d", "Go right", constants.RIGHT)
        )
        self.assertIsNone(game.add_menu_entry("main_menu", None, "-----------------"))
        self.assertIsNone(game.add_menu_entry("main_menu", "v", "Change game speed"))
        self.assertIsNone(game.add_menu_entry("destroy", None, "-----------------"))
        self.assertIsNone(game.delete_menu_category("destroy"))
        with self.assertRaises(base.PglInvalidTypeException):
            game.delete_menu_category(12)
        self.assertIsNone(
            game.update_menu_entry("main_menu", "d", "Go LEFT", constants.LEFT)
        )
        self.assertIsNone(game.get_menu_entry("main_menu_bork", "d"))
        self.assertEqual(game.get_menu_entry("main_menu", "d")["data"], constants.LEFT)
        self.assertIsNone(
            game.display_menu("main_menu", constants.ORIENTATION_HORIZONTAL, 1)
        )
        with self.assertRaises(base.PglException) as e:
            game.display_menu("main_menu_bork")
            self.assertEqual(e.error, "invalid_menu_category")
        self.assertIsNone(game.clear_screen())

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
            self.assertEqual(e.error, "unknown section")
        # Don't do that...
        g._configuration = None
        g._configuration_internals = None
        g.load_config("test-pygamelib.engine.Game.config.json", "new_high_scores")
        self.assertIsNone(g.save_config("new_high_scores", None))
        self.assertIsNone(g.save_config("new_high_scores", None, True))

    def test_board_management(self):
        b = engine.Board()
        g = engine.Game()
        self.assertIsNone(g.add_board(1, b))
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_board(1, 1)
        with self.assertRaises(base.PglInvalidTypeException):
            g.add_board("1", 1)
        with self.assertRaises(base.PglInvalidTypeException):
            g.get_board("1")
        self.assertIsInstance(g.get_board(1), engine.Board)
        with self.assertRaises(base.PglInvalidLevelException):
            g.current_board()
        with self.assertRaises(base.PglException) as e:
            g.change_level(1)
            self.assertEqual(e.error, "undefined_player")
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
        self.assertIsNone(g.add_npc(1, npc))
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


if __name__ == "__main__":
    unittest.main()
