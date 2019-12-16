"""
This module contains the base classes for both playable and non playable characters.
"""

from gamelib.Movable import Movable
from gamelib.Inventory import Inventory


class Character:
    """A base class for a character (playable or not)

    :param agility: Represent the agility of the character
    :type agility: int
    :param attack_power: Represent the attack power of the character.
    :type attack_power: int
    :param defense_power: Represent the defense_power of the character
    :type defense_power: int
    :param hp: Represent the hp (Health Point) of the character
    :type hp: int
    :param intelligence: Represent the intelligence of the character
    :type intelligence: int
    :param max_hp: Represent the max_hp of the character
    :type max_hp: int
    :param max_mp: Represent the max_mp of the character
    :type max_mp: int
    :param mp: Represent the mp (Mana/Magic Point) of the character
    :type mp: int
    :param remaining_lives: Represent the remaining_lives of the character. For a NPC
        it is generally a good idea to set that to 1. Unless the NPC is a multi phased
        boss.
    :type remaining_lives: int
    :param strength: Represent the strength of the character
    :type strength: int

    These characteristics are here to be used by the game logic but very few of them are
    actually used by the Game (`gamelib.Game`) engine.


    """

    def __init__(self, **kwargs):
        self.max_hp = None
        self.hp = None
        self.max_mp = None
        self.mp = None
        self.remaining_lives = None
        self.attack_power = None
        self.defense_power = None
        self.strength = None
        self.intelligence = None
        self.agility = None
        for a in [
            "max_hp",
            "hp",
            "max_mp",
            "mp",
            "remaining_lives",
            "attack_power",
            "defense_power",
            "strength",
            "intelligence",
            "agility",
        ]:
            if a in kwargs.keys():
                setattr(self, a, kwargs[a])


class Player(Movable, Character):
    """
    A class that represent a player controlled by a human.
    It accepts all the parameters from :class:`~gamelib.Characters.Character` and is a
    :class:`~gamelib.Movable.Movable`.

    .. note:: If no inventory is passed as parameter a default one is created.
    """

    def __init__(self, **kwargs):
        if "max_hp" not in kwargs.keys():
            kwargs["max_hp"] = 100
        if "hp" not in kwargs.keys():
            kwargs["hp"] = 100
        if "remaining_lives" not in kwargs.keys():
            kwargs["remaining_lives"] = 3
        if "attack_power" not in kwargs.keys():
            kwargs["attack_power"] = 10
        Movable.__init__(self, **kwargs)
        Character.__init__(self, **kwargs)
        if "inventory" in kwargs.keys():
            self.inventory = kwargs["inventory"]
        else:
            self.inventory = Inventory()

    def pickable(self):
        """This method returns False (a player is obviously not pickable).
        """
        return False

    def has_inventory(self):
        """This method returns True (a player has an inventory).
        """
        return True

    def overlappable(self):
        """This method returns false (a player cannot be overlapped).

        .. note:: If you wish your player to be overlappable, you need to inherit from
            that class and re-implement overlappable().
        """
        return False


class NPC(Movable, Character):
    """
    A class that represent a non playable character controlled by the computer.
    For the NPC to be successfully managed by the Game, you need to set an actuator.

    None of the parameters are mandatory, however it is advised to make good use of some
    of them (like type or name) for game design purpose.

    In addition to its own member variables, this class inherits all members from:
        * :class:`gamelib.Characters.Character`
        * :class:`gamelib.Movable.Movable`
        * :class:`gamelib.BoardItem.BoardItem`

    :param actuator: An actuator, it can be any class but it need to implement
        gamelibe.Actuator.Actuator.
    :type actuator: gamelib.Actuators.Actuator

    Example::

        mynpc = NPC(name='Idiot McStupid', type='dumb_ennemy')
        mynpc.step = 1
        mynpc.actuator = RandomActuator()
    """

    def __init__(self, **kwargs):
        if "max_hp" not in kwargs.keys():
            kwargs["max_hp"] = 10
        if "hp" not in kwargs.keys():
            kwargs["hp"] = 10
        if "remaining_lives" not in kwargs.keys():
            kwargs["remaining_lives"] = 1
        if "attack_power" not in kwargs.keys():
            kwargs["attack_power"] = 5
        Movable.__init__(self, **kwargs)
        Character.__init__(self, **kwargs)
        if "actuator" not in kwargs.keys():
            self.actuator = None
        else:
            self.actuator = kwargs["actuator"]

        if "step" not in kwargs.keys():
            self.step = 1
        else:
            self.step = kwargs["step"]

    def pickable(self):
        """Define if the NPC is pickable.

        Obviously this method always return False.

        :return: False
        :rtype: Boolean

        Example::

            if mynpc.pickable():
                Utils.warn("Something is fishy, that NPC is pickable"
                    "but is not a Pokemon...")
        """
        return False

    def overlappable(self):
        """Define if the NPC is overlappable.

        Obviously this method also always return False.

        :return: False
        :rtype: Boolean

        Example::

            if mynpc.overlappable():
                Utils.warn("Something is fishy, that NPC is overlappable but"
                    "is not a Ghost...")
        """
        return False

    def has_inventory(self):
        """Define if the NPC has an inventory.

        This method returns false because the game engine doesn't manage NPC inventory
        yet but it could be in the future. It's a good habit to check the value returned
        by this function.

        :return: False
        :rtype: Boolean

        Example::

            if mynpc.has_inventory():
                print("Cool: we can pickpocket that NPC!")
            else:
                print("No pickpocketing XP for us today :(")
        """
        return False
