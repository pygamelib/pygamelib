"""This module contains the base classes for simple and advanced actuators.
These classes are the base contract for actuators.
If you wish to create your own one, you need to inheritate from one of these base class.
"""

from gamelib.Constants import PAUSED, RUNNING, STOPPED


class Actuator():
    """
    Actuator is the base class for all Actuators. It is mainly a contract class with
    some utility methods.

    By default, all actuators are considered movement actuators. So the base class only
    require next_move() to be implemented.
    """
    def __init__(self):
        """
        The constructor does not take any parameters.

        .. important:: The default state of ALL actuators is RUNNING. If you want your
            actuator to be in a different state (PAUSED for example), you have to do it
            yourself.
        """
        self.type = None
        self.state = RUNNING

    def start(self):
        """Set the actuator state to RUNNING.

        If the actuator state is not RUNNING, actuators' next_move() function
        (and all derivatives) should not return anything.

        Example::

            mygame.start()
        """
        self.state = RUNNING

    def pause(self):
        """Set the actuator state to PAUSED.

        Example::

            mygame.pause()
        """
        self.state = PAUSED

    def stop(self):
        """Set the actuator state to STOPPED.

        Example::

            mygame.stop()
        """
        self.state = STOPPED

    def next_move(self):
        """
        That method needs to be implemented by all actuators or a NotImplementedError
        exception will be raised.

        :raises: NotImplementedError
        """
        raise NotImplementedError()


class Behavioral(Actuator):
    """
    The behavioral actuator is inheriting from Actuator and is adding a next_action()
    method.
    The actual actions are left to the actuator that implements Behavioral.
    """
    def __init__(self):
        """
        The constructor simply construct an Actuator.
        """
        Actuator.__init__(self)

    def next_action(self):
        """
        That method needs to be implemented by all behavioral actuators or a
        NotImplementedError exception will be raised.

        :raises: NotImplementedError
        """
        raise NotImplementedError()
