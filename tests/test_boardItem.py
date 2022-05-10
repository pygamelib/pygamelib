# import pygamelib.board_items as pgl_board_items
from pygamelib import board_items, constants, base, actuators
import pygamelib.gfx.core as gfx_core
from pygamelib.gfx import particles
import unittest


class TestBoard(unittest.TestCase):
    def test_create_default_boardItem(self):
        self.boardItem = board_items.BoardItem()
        self.assertEqual(self.boardItem.name, "Board item")
        self.assertEqual(self.boardItem.type, "item")
        self.assertEqual(self.boardItem.pos, [None, None, None])
        self.assertEqual(self.boardItem.model, "*")
        self.assertEqual(self.boardItem.__str__(), self.boardItem.__repr__())

    def test_custom_boardItem(self):
        self.boardItem = board_items.BoardItem(
            name="test_boardItem",
            item_type="test_type",
            pos=[10, 10],
            model="test_model",
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
            name="test_boardItem",
            item_type="test_type",
            pos=[10, 10],
            model="test_model",
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
        self.assertEqual(bi.inventory_space, 1)
        self.assertEqual(bi.size, [1, 1])
        self.assertEqual(bi.restorable(), False)
        self.assertEqual(bi.overlappable(), False)
        self.assertEqual(bi.pickable(), False)
        self.assertEqual(bi.type, "item")
        self.assertEqual(bi.name, "Board item")
        self.assertEqual(bi.can_move(), False)
        self.assertEqual(bi.sprixel.model, "*")
        self.assertEqual(bi.sprixel.is_bg_transparent, True)
        self.assertIsNone(bi.value)
        bi = board_items.BoardItem(
            overlappable=None, pickable=None, restorable=None, can_move=None
        )
        self.assertFalse(bi.overlappable())
        self.assertFalse(bi.restorable())
        self.assertFalse(bi.pickable())
        self.assertFalse(bi.can_move())
        bi = board_items.BoardItem(overlappable=True, pickable=True, restorable=True)
        self.assertFalse(bi.pickable())
        bi = board_items.BoardItem(overlappable=False, pickable=True, restorable=True)
        self.assertFalse(bi.restorable())
        bi.sprixel = None
        self.assertEqual(str(bi), "")
        self.assertEqual(bi.inventory_space, 1)
        bi.inventory_space = 2
        self.assertEqual(bi.inventory_space, 2)
        with self.assertRaises(base.PglInvalidTypeException):
            bi.inventory_space = "2"
        with self.assertRaises(base.PglInvalidTypeException):
            bi.set_overlappable("False")
        self.assertIsNone(bi.set_can_move(True))
        with self.assertRaises(base.PglInvalidTypeException):
            bi.set_can_move("True")
        with self.assertRaises(base.PglInvalidTypeException):
            bi.set_pickable("False")
        bi = board_items.BoardItem(particle_emitter=particles.ParticleEmitter())
        self.assertIsInstance(bi.particle_emitter, particles.ParticleEmitter)
        bi.store_position(2, 3)
        self.assertEqual(bi.particle_emitter.row, 2)
        self.assertEqual(bi.particle_emitter.column, 3)
        self.assertEqual(bi.particle_emitter.row, bi.row)
        self.assertEqual(bi.particle_emitter.column, bi.column)
        bi.store_position(3, 3)
        self.assertEqual(bi.heading, base.Vector2D(1, 0))

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
        self.assertIsInstance(bic.sprite, gfx_core.Sprite)
        self.assertIsInstance(bic.item(1, 1), board_items.BoardItemVoid)
        with self.assertRaises(board_items.base.PglOutOfItemBoundException):
            bic.item(5, 6)
        data = bic.serialize()
        data["has_inventory"] = False
        self.assertEqual(bic.size, data["size"])
        bic2 = board_items.BoardComplexItem.load(data)
        self.assertEqual(bic.size, bic2.size)
        data = bic2.serialize()
        del data["null_sprixel"]
        bic3 = board_items.BoardComplexItem.load(data)
        self.assertIsInstance(bic3.null_sprixel, gfx_core.Sprixel)

    def test_movable(self):
        bi = board_items.Movable(step=2)
        bi = board_items.Movable(step_vertical=2, step_horizontal=1)
        self.assertEqual(bi.dtmove, 0.0)
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            bi.dtmove = "crash"

        with self.assertRaises(NotImplementedError):
            bi.has_inventory()
        data = bi.serialize()
        self.assertIsNotNone(data)
        self.assertEqual(data["step_vertical"], 2)
        self.assertEqual(data["step_horizontal"], 1)
        bil = board_items.Movable.load(data)
        self.assertEqual(bil.step_vertical, 2)
        self.assertEqual(bil.step_horizontal, 1)

    def test_projectile(self):
        with self.assertRaises(board_items.base.PglException) as e:
            board_items.Projectile(range=6, step=4)
        self.assertEqual(e.exception.error, "incorrect_range_step")
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
        self.assertEqual(bi.inventory_space, 2)
        # with self.assertRaises(NotImplementedError):
        #     bi.restorable()
        with self.assertRaises(board_items.base.PglInvalidTypeException):
            bi.inventory_space = "2"
        bi.inventory_space = 3
        self.assertEqual(bi.inventory_space, 3)

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
        sprite = gfx_core.Sprite(
            name="test_sprite",
            sprixels=[
                [
                    gfx_core.Sprixel(" ", gfx_core.Color(255, 0, 0)),
                    gfx_core.Sprixel(" ", gfx_core.Color(255, 0, 0)),
                ]
            ],
        )
        n = board_items.ComplexPlayer(name="Test Player", sprite=sprite)
        n.actuator = actuators.RandomActuator()
        data = n.serialize()
        self.assertEqual(n.name, data["name"])
        self.assertEqual(n.sprite.name, data["sprite"]["name"])
        n2 = board_items.ComplexPlayer.load(data)
        self.assertEqual(n.name, n2.name)
        data = n2.serialize()
        del data["null_sprixel"]
        n3 = board_items.ComplexPlayer.load(data)
        self.assertIsInstance(n3.null_sprixel, gfx_core.Sprixel)

    def test_npc(self):
        npc = board_items.NPC(actuator=board_items.actuators.RandomActuator(), step=1)
        self.assertFalse(npc.pickable())
        self.assertFalse(npc.overlappable())
        self.assertFalse(npc.has_inventory())

    def test_character(self):
        character = board_items.Character(
            max_hp=20,
            max_mp=10,
            mp=10,
            defense_power=10,
            strength=2,
            agility=0,
            intelligence=27,
        )
        self.assertEqual(character.max_hp, 20)
        self.assertEqual(character.max_mp, 10)
        self.assertEqual(character.mp, 10)
        self.assertEqual(character.intelligence, 27)
        self.assertEqual(character.defense_power, 10)
        self.assertEqual(character.strength, 2)
        self.assertEqual(character.agility, 0)
        data = character.serialize()
        self.assertIsNotNone(data)
        self.assertEqual(data["max_hp"], 20)
        self.assertEqual(data["intelligence"], 27)
        cl = board_items.Character.load(data)
        self.assertEqual(cl.max_hp, 20)
        self.assertEqual(cl.intelligence, 27)

    def test_complexnpc(self):
        sprite = gfx_core.Sprite(
            name="test_sprite",
            sprixels=[
                [
                    gfx_core.Sprixel(" ", gfx_core.Color(255, 0, 0)),
                    gfx_core.Sprixel(" ", gfx_core.Color(255, 0, 0)),
                ]
            ],
        )
        n = board_items.ComplexNPC(name="Test NPC", sprite=sprite)
        n.actuator = actuators.RandomActuator()
        data = n.serialize()
        self.assertEqual(n.name, data["name"])
        self.assertEqual(n.sprite.name, data["sprite"]["name"])
        n2 = board_items.ComplexNPC.load(data)
        self.assertEqual(n.name, n2.name)
        data = n2.serialize()
        del data["null_sprixel"]
        n3 = board_items.ComplexNPC.load(data)
        self.assertIsInstance(n3.null_sprixel, gfx_core.Sprixel)

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
        data = bi.serialize()
        data["has_inventory"] = False
        bi2 = board_items.TextItem.load(data)
        self.assertEqual(bi.text.text, bi2.text.text)

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
        bi = board_items.GenericActionableStructure(model="T")
        self.assertEqual(bi.sprixel.model, "T")

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
            item_type="closed_door",
            pickable=False,
            overlappable=False,
            restorable=True,
        )
        self.assertEqual(bi.inventory_space, 5)
        self.assertFalse(bi.pickable())
        self.assertFalse(bi.overlappable())
        self.assertTrue(bi.restorable())

    def test_tile(self):
        bi = board_items.Tile()
        self.assertFalse(bi.pickable())
        data = bi.serialize()
        data["has_inventory"] = False
        self.assertEqual(bi.overlappable(), data["overlappable"])
        self.assertEqual(bi.pickable(), data["pickable"])
        bi2 = board_items.Tile.load(data)
        self.assertEqual(bi.overlappable(), bi2.overlappable())
        self.assertEqual(bi.pickable(), bi2.pickable())
        data = bi2.serialize()
        del data["null_sprixel"]
        bi3 = board_items.Tile.load(data)
        self.assertIsInstance(bi3.null_sprixel, gfx_core.Sprixel)
        self.assertIsInstance(board_items.ActionableTile(), board_items.Tile)
        self.assertIsInstance(board_items.ActionableTile(), board_items.Actionable)
        self.assertIsInstance(board_items.ActionableTile(), board_items.ActionableTile)

    def test_complex_version(self):
        ci = board_items.ComplexDoor()
        self.assertFalse(ci.pickable())
        self.assertTrue(ci.overlappable())
        data = ci.serialize()
        data["has_inventory"] = False
        self.assertEqual(ci.overlappable(), data["overlappable"])
        ci2 = board_items.ComplexDoor.load(data)
        self.assertEqual(ci.overlappable(), ci2.overlappable())
        data = ci2.serialize()
        del data["null_sprixel"]
        ci3 = board_items.ComplexDoor.load(data)
        self.assertIsInstance(ci3.null_sprixel, gfx_core.Sprixel)
        ci = board_items.ComplexWall()
        self.assertFalse(ci.pickable())
        self.assertFalse(ci.overlappable())
        data = ci.serialize()
        data["has_inventory"] = False
        self.assertEqual(ci.overlappable(), data["overlappable"])
        ci2 = board_items.ComplexWall.load(data)
        self.assertEqual(ci.overlappable(), ci2.overlappable())
        data = ci2.serialize()
        del data["null_sprixel"]
        ci3 = board_items.ComplexWall.load(data)
        self.assertIsInstance(ci3.null_sprixel, gfx_core.Sprixel)
        ci = board_items.ComplexTreasure()
        self.assertTrue(ci.pickable())
        self.assertFalse(ci.overlappable())
        data = ci.serialize()
        data["has_inventory"] = False
        self.assertEqual(ci.overlappable(), data["overlappable"])
        ci2 = board_items.ComplexTreasure.load(data)
        self.assertEqual(ci.overlappable(), ci2.overlappable())
        data = ci2.serialize()
        del data["null_sprixel"]
        ci3 = board_items.ComplexTreasure.load(data)
        self.assertIsInstance(ci3.null_sprixel, gfx_core.Sprixel)

    def test_camera(self):
        cam = board_items.Camera()
        cam = board_items.Camera(actuator=42)
        self.assertEqual(cam.actuator, 42)
        cam.row = 12
        cam.column = 34
        self.assertEqual(cam.row, 12)
        self.assertEqual(cam.column, 34)
        self.assertFalse(cam.has_inventory())


if __name__ == "__main__":
    unittest.main()
