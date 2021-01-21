# import pygamelib.board_items as pgl_board_items
from pygamelib import board_items
from pygamelib import constants
import pygamelib.gfx.core as gfx_core
import unittest


class TestBoard(unittest.TestCase):
    def test_create_default_boardItem(self):
        self.boardItem = board_items.BoardItem()
        self.assertEqual(self.boardItem.name, "Board item")
        self.assertEqual(self.boardItem.type, "item")
        self.assertEqual(self.boardItem.pos, [None, None])
        self.assertEqual(self.boardItem.model, "*")
        self.assertEqual(self.boardItem.__str__(), self.boardItem.__repr__())

    def test_custom_boardItem(self):
        self.boardItem = board_items.BoardItem(
            name="test_boardItem", type="test_type", pos=[10, 10], model="test_model"
        )
        self.assertEqual(self.boardItem.name, "test_boardItem")
        self.assertEqual(self.boardItem.type, "test_type")
        self.assertEqual(self.boardItem.pos, [10, 10])
        self.assertEqual(self.boardItem.model, "test_model")
        self.assertEqual(self.boardItem.__repr__(), "test_model\x1b[0m")
        self.assertIsNone(self.boardItem.display())
        self.assertIn("'model' = 'test_model'", self.boardItem.debug_info())
        self.assertEqual(self.boardItem.position_as_vector().row, 10)
        self.assertEqual(self.boardItem.position_as_vector().column, 10)
        self.assertEqual(self.boardItem.row, 10)
        self.assertEqual(self.boardItem.column, 10)
        self.assertEqual(self.boardItem.width, 1)
        self.assertEqual(self.boardItem.height, 1)
        bi = board_items.BoardItem(
            name="test_boardItem", type="test_type", pos=[10, 10], model="test_model"
        )
        self.assertTrue(self.boardItem.collides_with(bi))
        bi.store_position(8, 9)
        self.assertFalse(self.boardItem.collides_with(bi))
        with self.assertRaises(Exception) as context:
            self.boardItem.collides_with(12)

        self.assertAlmostEqual(self.boardItem.distance_to(bi), 2.23606797749979)
        self.assertTrue("require a BoardItem as parameter" in str(context.exception))
        with self.assertRaises(Exception) as context:
            self.boardItem.distance_to(12)

        self.assertTrue("require a BoardItem as parameter" in str(context.exception))

        bi = board_items.BoardItem(sprixel=gfx_core.Sprixel("-"))
        self.assertEqual(bi.__str__(), gfx_core.Sprixel("-").__repr__())

    def test_default_boarditem_implementation(self):
        bi = board_items.BoardItem()
        with self.assertRaises(NotImplementedError):
            bi.can_move()
        with self.assertRaises(NotImplementedError):
            bi.pickable()
        with self.assertRaises(NotImplementedError):
            bi.overlappable()
        with self.assertRaises(NotImplementedError):
            bi.inventory_space()

    def test_boarditemvoid(self):
        bi = board_items.BoardItemVoid()
        self.assertEqual(bi.name, "void_cell")
        self.assertFalse(bi.pickable())
        self.assertTrue(bi.overlappable())

    def test_boarditemcomplexcomponent(self):
        bi = board_items.BoardItemComplexComponent(parent=None)
        self.assertFalse(bi.restorable())
        self.assertFalse(bi.overlappable())
        self.assertFalse(bi.can_move())
        self.assertFalse(bi.pickable())
        bic = board_items.ComplexPlayer()
        bi = board_items.BoardItemComplexComponent(parent=bic)
        bic = board_items.Tile()
        # Please never do that... Python allowing it is bad enough.
        bic.can_move = True
        bic.overlappable = True
        bi = board_items.BoardItemComplexComponent(parent=bic)

    def test_boardcomplexitem(self):
        bic = board_items.BoardComplexItem(
            size=[3, 3], null_sprixel=board_items.core.Sprixel()
        )
        self.assertIsInstance(bic.item(1, 1), board_items.BoardItemVoid)
        with self.assertRaises(board_items.base.PglOutOfItemBoundException):
            bic.item(5, 6)

    def test_movable(self):
        bi = board_items.Movable(step=2)
        bi = board_items.Movable(step_vertical=2, step_horizontal=1)
        self.assertEqual(bi.dtmove, 0.0)
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            bi.dtmove = "crash"

        with self.assertRaises(NotImplementedError):
            bi.has_inventory()

    def test_projectile(self):
        with self.assertRaises(board_items.base.PglException) as e:
            board_items.Projectile(range=6, step=4)
            self.assertEqual(e.error, "incorrect_range_step")
        p = board_items.Projectile()
        self.assertFalse(p.has_inventory())
        self.assertTrue(p.overlappable())
        self.assertTrue(p.restorable())
        # Directional animations
        p.add_directional_animation(constants.DOWN, gfx_core.Animation())
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            p.add_directional_animation("crash", gfx_core.Animation())
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            p.add_directional_animation(constants.DOWN, "crash")
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            p.directional_animation("crash")
        self.assertIsInstance(
            p.directional_animation(constants.DOWN), gfx_core.Animation
        )
        self.assertIsNone(p.directional_animation(constants.UP))
        p.movement_animation = gfx_core.Animation()
        self.assertIsInstance(p.directional_animation(constants.UP), gfx_core.Animation)
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            p.remove_directional_animation("crash")
        self.assertIsNone(p.remove_directional_animation(constants.DOWN))
        # Directional models
        p.add_directional_model(constants.DOWN, "|")
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            p.add_directional_model("crash", "|")
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            p.add_directional_model(constants.DOWN, 1)
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            p.directional_model("crash")
        self.assertEqual(p.directional_model(constants.DOWN), "|")
        self.assertEqual(p.directional_model(constants.UP), "⌁")
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            p.remove_directional_model("crash")
        self.assertIsNone(p.remove_directional_model(constants.DOWN))
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            p.set_direction("crash")
        self.assertIsNone(p.set_direction(constants.DOWN))
        p.animation = gfx_core.Animation()
        p.hit_model = "*"
        self.assertIsNone(p.hit([board_items.BoardItemVoid]))

        def _r():
            pass

        p.hit_animation = gfx_core.Animation(refresh_screen=_r, parent=p)
        self.assertIsNone(p.hit([board_items.BoardItemVoid]))

        def _cb(p, o, params):
            return True

        p.hit_callback = _cb
        self.assertIsNone(p.hit([board_items.BoardItemVoid]))

    def test_immovable(self):
        bi = board_items.Immovable(inventory_space=2)
        self.assertFalse(bi.can_move())
        self.assertEqual(bi.inventory_space(), 2)
        with self.assertRaises(NotImplementedError):
            bi.restorable()

    def test_actionable(self):
        bi = board_items.Actionable()

        def _act(p):
            t = p[0]
            t.assertEqual(p[1], 1)

        bi = board_items.Actionable(
            action=_act,
            action_parameters=[self, 1],
            perm=constants.ALL_MOVABLE_AUTHORIZED,
        )
        self.assertIsNone(bi.activate())

    def test_player(self):
        p = board_items.Player(inventory=board_items.engine.Inventory())
        self.assertFalse(p.pickable())
        self.assertTrue(p.has_inventory())

    def test_npc(self):
        npc = board_items.NPC(actuator=board_items.actuators.RandomActuator(), step=1)
        self.assertFalse(npc.pickable())
        self.assertFalse(npc.overlappable())
        self.assertFalse(npc.has_inventory())

    def test_character(self):
        character = board_items.Character(max_hp=20, intelligence=27)
        self.assertEqual(character.max_hp, 20)
        self.assertEqual(character.intelligence, 27)

    def test_complexnpc(self):
        board_items.ComplexNPC()

    def test_textitem(self):
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            board_items.TextItem(text=board_items.TextItem(text="crash"))
        bi = board_items.TextItem(text="test")
        self.assertEqual(bi.text.text, "test")
        bi = board_items.TextItem(text=board_items.base.Text("test"))
        self.assertEqual(bi.text.text, "test")
        bi.text = "value change"
        self.assertEqual(bi.text.text, "value change")
        bi.text = board_items.base.Text("value change")
        self.assertEqual(bi.text.text, "value change")
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            bi.text = board_items.BoardComplexItem()

    def test_wall(self):
        bi = board_items.Wall()
        self.assertFalse(bi.pickable())
        self.assertFalse(bi.overlappable())
        self.assertFalse(bi.restorable())

    def test_genericstructure(self):
        bi = board_items.GenericStructure(value=5)
        self.assertFalse(bi.pickable())
        self.assertFalse(bi.overlappable())
        self.assertFalse(bi.restorable())
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            bi.set_restorable(1)
        bi.set_restorable(True)
        self.assertTrue(bi.restorable())
        bi = board_items.GenericActionableStructure()

    def test_treasure(self):
        bi = board_items.Treasure(value=1000, inventory_space=5)
        self.assertTrue(bi.pickable())
        self.assertFalse(bi.overlappable())
        self.assertFalse(bi.restorable())

    def test_door(self):
        bi = board_items.Door()
        self.assertEqual(bi.model, "]")
        self.assertEqual(bi.name, "Door")
        self.assertEqual(bi.type, "door")
        bi = board_items.Door(
            value=1,
            inventory_space=5,
            model="]",
            name="The door",
            type="closed_door",
            pickable=False,
            overlappable=False,
            restorable=True,
        )
        self.assertFalse(bi.pickable())
        self.assertFalse(bi.overlappable())
        self.assertTrue(bi.restorable())

    def test_tile(self):
        bi = board_items.Tile()
        self.assertFalse(bi.pickable())

    def test_complex_version(self):
        ci = board_items.ComplexDoor()
        self.assertFalse(ci.pickable())
        self.assertTrue(ci.overlappable())
        ci = board_items.ComplexWall()
        self.assertFalse(ci.pickable())
        self.assertFalse(ci.overlappable())
        ci = board_items.ComplexTreasure()
        self.assertTrue(ci.pickable())
        self.assertFalse(ci.overlappable())

    def test_camera(self):
        cam = board_items.Camera()
        cam = board_items.Camera(actuator=42)
        self.assertEqual(cam.actuator, 42)
        cam.row = 12
        cam.column = 34
        self.assertEqual(cam.row, 12)
        self.assertEqual(cam.column, 34)


if __name__ == "__main__":
    unittest.main()
