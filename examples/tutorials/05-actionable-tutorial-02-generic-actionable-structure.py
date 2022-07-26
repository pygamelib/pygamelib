import examples_includes  # noqa: F401

from pygamelib import engine, constants, board_items
from pygamelib.gfx import core


# Here is our callback
def destroy_callback(action_parameters):
    # The first action parameter is the actionable object.
    act = action_parameters[0]
    # We set the game object as the second action parameter, so let's get it back
    game = action_parameters[1]

    # Then let's increase the score with the actionable's value.
    game.score += act.value

    # And we remove the actionable from the board.
    game.current_board().remove_item(act)

    # And update the score
    game.screen.place(f"Score: {game.score}", 0, game.current_board().width + 1)


def projectile_hit(projectile, targets, extra):
    # If the projectile hits a target, we trigger the actionable callback.
    if isinstance(targets[0], board_items.Actionable):
        targets[0].activate()


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
    elif input_key == " ":
        # If the player hits the space bar, we fire a projectile.
        p = board_items.Projectile(
            direction=constants.UP,
            range=10,
            sprixel=core.Sprixel("|", fg_color=core.Color(255, 0, 0)),
            hit_callback=projectile_hit,
        )
        # And place the projectile just above the player.
        game.add_projectile(1, p, game.player.row - 1, game.player.column)

    # And we need to update the screen at each frame.
    # update() will only redraw the screen if something changed, whereas force_update()
    # will redraw the screen regardless of its state.
    game.screen.update()


if __name__ == "__main__":
    # Now let's create a game object.
    game = engine.Game(
        # MODE_RT tells the game to run in real time.
        mode=constants.MODE_RT,
        # The player will be a cyan "@"
        player=board_items.Player(
            sprixel=core.Sprixel("^", fg_color=core.Color(255, 0, 0))
        ),
        # Finally we set the update function. It will be called every frame.
        user_update=main_game_update,
    )
    # Let's add an extra variable to the game object to hold the score.
    setattr(game, "score", 0)

    # Now let's create our board.
    board = engine.Board(
        # We set the size of the board to be 20 columns by 10 rows.
        size=[20, 10],
        # This controls the background color of the board. This one will be blue-ish
        ui_board_void_cell_sprixel=core.Sprixel(" ", bg_color=core.Color(0, 0, 0)),
        # The player will be at the bottom center of the board.
        player_starting_position=[9, 10],
    )

    # Now we add the board to the game.
    game.add_board(1, board)

    # Change level to level 1
    game.change_level(1)

    # Place the score counter on the screen next to the board.
    game.screen.place(f"Score: {game.score}", 0, board.width + 1)

    # Let's put lines of GenericActionableStructure as destructible walls.
    for c in range(board.width):
        a1 = board_items.GenericActionableStructure(
            # The actionable will be a green "#"
            sprixel=core.Sprixel("#", fg_color=core.Color(0, 255, 0)),
            # The callback action will be the destroy_callback function
            action=destroy_callback,
            # Set the permission so movable objects can use the Actionable
            perm=constants.ALL_MOVABLE_AUTHORIZED,
            value=100,
        )
        # We want the callback to know about ourselves.
        a1.action_parameters = [a1, game]
        # We add the actionable to the board
        board.place_item(a1, 0, c)
    # And another line of less valuable items.
    for c in range(board.width):
        a1 = board_items.GenericActionableStructure(
            # The actionable will be a orange "#"
            sprixel=core.Sprixel("#", fg_color=core.Color(255, 155, 0)),
            # The callback action will be the destroy_callback function
            action=destroy_callback,
            # Set the permission so movable objects can use the Actionable
            perm=constants.ALL_MOVABLE_AUTHORIZED,
            value=50,
        )
        # We want the callback to know about ourselves.
        a1.action_parameters = [a1, game]
        # We add the actionable to the board
        board.place_item(a1, 1, c)

    # Place the board on screen (the Game object automatically creates a screen of the
    # size of the terminal). You can create your own screen if you want.
    game.screen.place(board, 0, 0)  # Top left corner

    # And finally run the game
    game.run()
