import examples_includes  # noqa: F401
from pygamelib import engine, board_items, constants, base
from pygamelib.gfx import core
from pygamelib.assets import graphics

# This simplistic example shows the basic of player movement.
# It also shows how to change the level on key press.

# The game will run in fullscreen mode and will restore the state of the terminal
# when the game is stopped.


def update_game(game: engine.Game, key, elapsed_time):
    # The update function is called every frame and always receive 3 arguments:
    # game: the game object
    # key: the key pressed by the user (if any) or None
    # delta_time: the time passed since the last frame (in seconds)

    # First, we process the direction keys. We react to direction keys, wasd and zqsd
    # for directions.
    if key == "w" or key == "z" or key == engine.key.UP:
        game.move_player(constants.UP, 1)
    elif key == "s" or key == engine.key.DOWN:
        game.move_player(constants.DOWN, 1)
    elif key == "a" or key == "q" or key == engine.key.LEFT:
        game.move_player(constants.LEFT, 1)
    elif key == "d" or key == engine.key.RIGHT:
        game.move_player(constants.RIGHT, 1)
    elif key == "X" or key == engine.key.ESC:
        # If the user press ESC or Shift+x, we stop the game.
        game.stop()
    elif key == "b":
        # If the user press b, we change the level.
        if game.current_level == 1:
            game.change_level(2)
        else:
            game.change_level(1)

        # We don't forget to place the current board and its name in the top left corner
        # of the screen.
        mygame.screen.place(mygame.current_board().name, 0, 0)
        mygame.screen.place(mygame.current_board(), 1, 0)

    # And finally we update the screen.
    game.screen.update()


if __name__ == "__main__":

    # Create a new game instance.
    # The game has a name (here it is "Demo game"), it is up to you to use or not that
    # name.
    # We set the game to run in real time (default is to run turn by turn). MODE_RT is
    # for real time, MODE_TBT is for turn based.
    # We also give the game engine a reference to the update_game function. This
    # function for every frame.
    # Please refer to the documentation for more information about the Game class:
    # https://pygamelib.readthedocs.io/en/latest/pygamelib.engine.Game.html
    mygame = engine.Game(
        name="Demo game", user_update=update_game, mode=constants.MODE_RT
    )
    # Then we create 2 basic boards. Please have a look at the wiki for a complete
    # tutorial on Boards:
    # https://github.com/pygamelib/pygamelib/wiki/Getting-started-Board
    # And the documentation for the Board class:
    # https://pygamelib.readthedocs.io/en/latest/pygamelib.engine.Board.html
    board1 = engine.Board(
        name="Level 1",
        ui_board_void_cell_sprixel=core.Sprixel.blue_square(),  # blue background
        player_starting_position=[0, 0],  # The player starts at the top left corner
    )
    board2 = engine.Board(
        name="Level 2",
        ui_board_void_cell_sprixel=core.Sprixel.black_square(),  # black background
        player_starting_position=[4, 4],  # The player starts at position [4, 4]
    )

    # Then we create a player that will be represented by a Unicorn emoji.
    # We explicitly set the background to be transparent, so the player will take the
    # background color of the board.
    # For more information on board items, please refer to the documentation:
    # https://pygamelib.readthedocs.io/en/latest/board_items.html
    mygame.player = board_items.Player(
        name="DaPlay3r",
        sprixel=core.Sprixel(graphics.Models.UNICORN, is_bg_transparent=True),
    )

    # We add the boards to the game.
    mygame.add_board(1, board1)
    mygame.add_board(2, board2)

    # We change the level to the first one.
    mygame.change_level(1)
    # We place the current board and its name in the top left corner of the screen.
    mygame.screen.place(mygame.current_board().name, 0, 0)
    mygame.screen.place(mygame.current_board(), 1, 0)

    # Now let's put a message bellow the board to help about the controls.
    mygame.screen.place(
        base.Text.cyan_bright("Press WASD or ZQSD to move the player"),
        mygame.current_board().height + 2,  # the message will be placed below the board
        0,
    )
    mygame.screen.place(
        base.Text.green_bright("Press b to change the level"),
        mygame.current_board().height + 3,  # And this one on the next line
        0,
    )
    mygame.screen.place(
        base.Text.red_bright("Press ESC or Shift+x to quit"),
        mygame.current_board().height + 4,  # And this one on the next line
        0,
    )

    # And we start the game. Everything will now be handled by the user_update function.
    mygame.run()

    # This is going to be displayed when the player quit.
    # The Text class can ease a lot the display of fancy text in the terminal.
    # Please refer to the documentation for more information about the Text class:
    # https://pygamelib.readthedocs.io/en/latest/pygamelib.base.Text.html
    print(base.Text.yellow_bright("Good bye and thank you for playing!"))
