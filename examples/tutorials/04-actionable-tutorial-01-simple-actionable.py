import examples_includes  # noqa: F401

from pygamelib import engine, constants, board_items, actuators
from pygamelib.gfx import core


# Here is our callback
def change_level_callback(action_parameters):
    # We set the game object as the first action_parameters, so let's get it back
    game = action_parameters[0]
    # Let's remember where the player was before changing level
    game.current_board().player_starting_position = game.player.pos
    # Now we just oscillate between two levels
    if game.current_level == 1:
        game.change_level(2)
    else:
        game.change_level(1)

    # Once, the level is changed, we need to update the screen
    game.screen.delete(0, 0)
    game.screen.place(game.current_board(), 0, 0)


# This is the update function that will be called every frame.
# The parameters are: a reference to the game object, the last input (can be None) and
# the elapsed time since the last frame.
def main_game_update(game: engine.Game, input_key, elapsed_time: float):

    # Here we just handle the inputs (Q for quit and arrows to move)
    if input_key == "Q":
        game.stop()
    elif input_key.name == "KEY_RIGHT":
        game.move_player(constants.RIGHT)
    elif input_key.name == "KEY_LEFT":
        game.move_player(constants.LEFT)
    elif input_key.name == "KEY_DOWN":
        game.move_player(constants.DOWN)
    elif input_key.name == "KEY_UP":
        game.move_player(constants.UP)

    # And we need to update the screen at each frame.
    # update() will only redraw the screen if something changed, whereas force_update()
    # will redraw the screen regardless of its state.
    game.screen.update()


if __name__ == "__main__":
    # Now let's create a game object.
    game = engine.Game(
        # MODE_RT tells the game to run in real time.
        mode=constants.MODE_RT,
        # The player will be a red "@"
        player=board_items.Player(
            sprixel=core.Sprixel("@", fg_color=core.Color(255, 0, 0))
        ),
        # Finally we set the update function. It will be called every frame.
        user_update=main_game_update,
    )
    # Now let's create our 2 boards.
    b1 = engine.Board(
        # We set the size of the board to be 20 columns by 10 rows.
        size=[20, 10],
        # This controls the background color of the board. This one will be blue-ish
        ui_board_void_cell_sprixel=core.Sprixel(
            " ", bg_color=core.Color(125, 125, 200)
        ),
    )
    b2 = engine.Board(
        # We set the size of the board to be 20 columns by 10 rows.
        size=[20, 10],
        # This controls the background color of the board. This one will be green-ish
        ui_board_void_cell_sprixel=core.Sprixel(
            " ", bg_color=core.Color(125, 200, 125)
        ),
    )

    # Now we add the boards to the game.
    game.add_board(1, b1)
    game.add_board(2, b2)

    # Change level to level 1
    game.change_level(1)

    # The only thing remaining is to set up the Actionable objects.
    a1 = board_items.Actionable(
        # The actionable will be a black "A"
        sprixel=core.Sprixel("A", fg_color=core.Color(0, 0, 0)),
        # The callback action will be the change_level_callback function
        action=change_level_callback,
        # The action_parameters will be the game object
        action_parameters=[game],
        # Set the permission so the Player and NPC can use the Actionable
        perm=constants.ALL_CHARACTERS_AUTHORIZED,
    )
    # We add the actionable to the board at row 2 and column 10
    b1.place_item(a1, 2, 10)

    # And the second one
    a2 = board_items.Actionable(
        # The actionable will be a white "A"
        sprixel=core.Sprixel("A", fg_color=core.Color(255, 255, 255)),
        # The callback action will be the change_level_callback function
        action=change_level_callback,
        # The action_parameters will be the game object
        action_parameters=[game],
    )
    # We add the actionable to the board at row 9 and column 2
    b2.place_item(a2, 9, 2)

    # Let's add an NPC represented by a yellow "N"
    npc = board_items.NPC(sprixel=core.Sprixel("N", fg_color=core.Color(255, 255, 0)))
    # We will place the NPC on the right and it will move to the left.
    npc.actuator = actuators.UnidirectionalActuator(direction=constants.LEFT)
    game.add_npc(1, npc, 2, 19)

    # Place the board on screen (the Game object automatically creates a screen of the
    # size of the terminal). You can create your own screen if you want.
    game.screen.place(b1, 0, 0)  # Top left corner

    # And finally run the game
    game.run()
