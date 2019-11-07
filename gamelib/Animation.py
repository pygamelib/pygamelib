"""This module contains the animation relation classes (so far only Animation).
"""

from gamelib.Constants import PAUSED, RUNNING, STOPPED
from gamelib.HacExceptions import HacInvalidTypeException
from gamelib.BoardItem import BoardItem
import time


class Animation(object):
    """
    The Animation class is used to give the ability to have more than one model
    for a BoardItem. An BoardItem can have an animation and all of them that
    are available to the Game object can be animated through
    Game.animate_items(lvl_number).
    To benefit from that, BoardItem.animation must be set explicitely.
    An animation is controlled via the same state system than the Actuators.

    The frames are all stored in a list called frames, that you can access
    through Animation.frames.

    :param display_time: The time each frame is displayed
    :type display_time: float
    :param auto_replay: controls the auto replay of the animation, if false
        once the animation is played it stays on the last
        frame of the animation.
    :type auto_replay: bool
    :param frames: an array of "frames" (string)
    :type frames: array[str]
    :param animated_object: The object to animate.
    :type animated_object: :class:`~gamelib.BoardItem.BoardItem`
    :param refresh_screen: The callback function that controls the redrawing of
        the screen. This function reference should come from the main game.
    :type refresh_screen: function

    Example ::

        def redraw_screen(game_object):
            game_object.clear_screen()
            game_object.display_board()

        item = BoardItem(model=Sprite.ALIEN, name='Friendly Alien')
        # By default BoardItem does not have any animation, we have to
        # explicitely create one
        item.animation = Animation(display_time=0.1, animated_object=item,
                                   refresh_screen=redraw_screen)
    """
    def __init__(self, display_time=0.05, auto_replay=True, frames=None,
                 animated_object=None, refresh_screen=None):
        self.state = RUNNING
        self.display_time = display_time
        self.auto_replay = auto_replay
        if frames is None:
            frames = []
        self.frames = frames
        self._frame_index = 0
        self.animated_object = animated_object
        self.refresh_screen = refresh_screen

    def start(self):
        """Set the animation state to RUNNING.

        If the animation state is not RUNNING, animation's next_frame()
        function return the last frame returned.

        Example::

            item.animation.start()
        """
        self.state = RUNNING

    def pause(self):
        """Set the animation state to PAUSED.

        Example::

            item.animation.pause()
        """
        self.state = PAUSED

    def stop(self):
        """Set the animation state to STOPPED.

        Example::

            item.animation.stop()
        """
        self.state = STOPPED

    def add_frame(self, frame):
        """Add a frame to the animation.

        The frame has to be a string (that includes sprites from the Sprite
        module and squares from the Utils module).

        Raise an exception if frame is not a string.

        :param frame: The frame to add to the animation.
        :type frame: str
        :raise: :class:`gamelib.HacExceptions.HacInvalidTypeException`

        Example::

            item.animation.add_frame(Sprite.ALIEN)
            item.animation.add_frame(Sprite.ALIEN_MONSTER)
        """
        if type(frame) is not str:
            raise HacInvalidTypeException(
                'The "frame" parameter must be a string.'
                )
        self.frames.append(frame)

    def search_frame(self, frame):
        """Search a frame in the animation.

        That method is returning the index of the first occurrence of "frame".

        Raise an exception if frame is not a string.

        :param frame: The frame to find.
        :type frame: str
        :rtype: int
        :raise: :class:`gamelib.HacExceptions.HacInvalidTypeException`

        Example::

            item.animation.remove_frame(
                item.animation.search_frame(Sprite.ALIEN_MONSTER)
            )

        """
        if type(frame) is not str:
            raise HacInvalidTypeException(
                'The "frame" parameter must be a string.'
            )
        return self.frames.index(frame)

    def remove_frame(self, index):
        """Remove a frame from the animation.

        That method remove the frame at the specified index and return it
        if it exists.

        If the index is out of bound an exception is raised.
        If the index is not an int an exception is raised.

        :param index: The index of the frame to remove.
        :type index: int
        :rtype: str
        :raise: IndexError, HacInvalidTypeException

        Example::

            item.animation.remove_frame( item.animation.search_frame(
                Sprite.ALIEN_MONSTER)
            )

        """
        if type(index) is not int:
            raise HacInvalidTypeException(
                'The "index" parameter must be an int.'
            )
        if index <= self._frame_index and self._frame_index > 0:
            self._frame_index -= 1
        return self.frames.pop(index)

    def reset(self):
        """Reset the Animation to the first frame.

        Example::

            item.animation.reset()
        """
        self._frame_index = 0

    def current_frame(self):
        """Return the current frame.

        Example::

            item.model = item.animation.current_frame()
        """
        return self.frames[self._frame_index]

    def next_frame(self):
        """Update the animated_object.model with the next frame of the animation.

        That method takes care of automatically replaying the animation if the
        last frame is reached if the state is RUNNING.

        If the the state is PAUSED it still update the animated_object.model
        and returning the current frame. It does NOT actually go to next frame.

        If animated_object is not a sub class of
        :class:`~gamelib.BoardItem.BoardItem` an exception is raised.

        :raise: :class:`~gamelib.HacExceptions.HacInvalidTypeException`

        Example::

            item.animation.next_frame()
        """
        if not isinstance(self.animated_object, BoardItem):
            raise HacInvalidTypeException(
                'The animated_object needs to be a sub class of BoardItem.'
            )
        if self.state == RUNNING:
            self._frame_index += 1
            if self._frame_index >= len(self.frames):
                if self.auto_replay:
                    self.reset()
                else:
                    self._frame_index = len(self.frames) - 1
            self.animated_object.model = self.frames[self._frame_index]
            return self.frames[self._frame_index]
        elif self.state == PAUSED:
            self.animated_object.model = self.frames[self._frame_index]
            return self.frames[self._frame_index]
        # By default Python will return None for the STOPPED case.
        # This is debatable: why shouldn't we do the same thing
        # for STOPPED and PAUSED

    def play_all(self):
        """Play the entire animation once.

        That method plays the entire animation only once, there is no auto
        replay as it blocks the game (for the moment).

        If the the state is PAUSED or STOPPED, the animation does not play and
        the method return False.

        If animated_object is not a sub class of
        :class:`~gamelib.BoardItem.BoardItem` an exception is raised.

        If screen_refresh is not defined or is not a function an exception
        is raised.

        :raise: :class:`~gamelib.HacExceptions.HacInvalidTypeException`

        Example::

            item.animation.play_all()
        """
        if self.state == PAUSED or self.state == STOPPED:
            return False
        if self.refresh_screen is None or not callable(self.refresh_screen):
            raise HacInvalidTypeException(
                'The refresh_screen parameter needs to be a callback '
                'function reference.'
            )
        if not isinstance(self.animated_object, BoardItem):
            raise HacInvalidTypeException(
                'The animated_object needs to be a sub class of BoardItem.'
            )
        for f in self.frames:
            self.animated_object.model = f
            self.refresh_screen()
            time.sleep(self.display_time)
        return True
