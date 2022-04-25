from pygamelib.gfx import particles, core
from pygamelib import engine, base, board_items, constants
from pygamelib.assets import graphics

global_emitters = []

proj_props = particles.EmitterProperties(
    variance=0.0,
    emit_number=2,
    emit_rate=0.2,
    lifespan=29,
    particle=particles.ColorParticle(
        sprixel=core.Sprixel(
            # graphics.GeometricShapes.BULLET, fg_color=core.Color(255, 100, 50)
            graphics.GeometricShapes.BLACK_SMALL_SQUARE,
            fg_color=core.Color(255, 100, 50),
        ),
        start_color=core.Color(255, 0, 0),
        stop_color=core.Color(180, 180, 180),
    ),
    # particle_velocity=base.Vector2D(0.0, -0.5),
    particle_lifespan=5,
    particle_acceleration=base.Vector2D(0.0, -0.5),
)

expl_props = particles.EmitterProperties(
    variance=2.0,
    emit_number=20,
    emit_rate=0.01,
    lifespan=1,
    particle=particles.ColorParticle(
        sprixel=core.Sprixel(graphics.GeometricShapes.BULLET),
        start_color=core.Color(255, 0, 0),
        stop_color=core.Color(180, 180, 180),
    ),
    particle_lifespan=5,
    radius=1,
)


def hit_callback(proj, coliding_objects, args):
    g = args[0]
    emt = particles.CircleEmitter(expl_props)
    emt.row = g.current_board().screen_row + proj.row
    emt.column = g.current_board().screen_column + proj.column
    global_emitters.append(emt)
    g.screen.place(emt, emt.row, emt.column, 2)


def update(g: engine.Game, key, dt):
    screen = g.screen
    # Clean logs
    for r in range(1, g.screen.height - b.height - 2):
        screen.delete(r, 0)

    # Remove dead emitters
    for i in range(len(global_emitters) - 1, 0, -1):
        if global_emitters[i].finished():
            del global_emitters[i]

    if key == "q":
        g.stop()
    elif key == "a":
        g.move_player(constants.LEFT)
    elif key == "d":
        g.move_player(constants.RIGHT)
    elif key == "w":
        g.move_player(constants.UP)
    elif key == "s":
        g.move_player(constants.DOWN)
    elif key.name == "KEY_SPACE" or key == " ":
        direction = base.Vector2D(0, 1)
        p = board_items.Projectile(
            direction=direction,
            range=30,
            movement_speed=0.05,
            # model=graphics.GeometricShapes.BLACK_CIRCLE,
            sprixel=core.Sprixel(
                graphics.GeometricShapes.BLACK_CIRCLE, fg_color=core.Color(255, 0, 0)
            ),
            hit_model="*",
            hit_callback=hit_callback,
            callback_parameters=[g],
        )
        p.particle_emitter = particles.ParticleEmitter(proj_props)
        g.add_projectile(
            g.current_level,
            p,
            g.player.row + direction.row,
            g.player.column + direction.column,
        )
    screen.place(f"proj_props.lifespan={proj_props.lifespan}", 0, 0)
    row = 1
    for emt in g.current_board()._particle_emitters:
        screen.place(
            f"Emitter #{row}: lifespan={emt.lifespan} row={emt.row} column={emt.column}"
            f" active={not emt.finished()}",
            row,
            0,
        )
        row += 1
    for emt in global_emitters:
        screen.place(
            f"Global Emitter: lifespan={emt.lifespan} row={emt.row} column={emt.column}"
            f" active={not emt.finished()}",
            row,
            0,
        )
        row += 1
        emt.emit()
        emt.update()
    if len(g.session_logs()) < (g.screen.height - b.height - 2) - row:
        for log in g.session_logs():
            screen.place(log, row, 0)
            row += 1
    else:
        stop = len(g.session_logs())
        start = stop - ((g.screen.height - b.height - 2) - row)
        for i in range(start, stop):
            screen.place(g.session_logs()[i], row, 0)
            row += 1

    screen.update()


if __name__ == "__main__":
    g = engine.Game.instance(
        player=board_items.Player(
            sprixel=core.Sprixel(
                "@",
                fg_color=core.Color(0, 255, 255),
            ),
            movement_speed=0.01,
        ),
        user_update=update,
        mode=constants.MODE_RT,
        input_lag=0.1,
    )
    g.DEBUG = True
    b = engine.Board(
        size=[g.screen.width, int(g.screen.height / 2)],
        ui_board_void_cell_sprixel=core.Sprixel(" ", core.Color(180, 180, 180)),
    )
    g.add_board(1, b)
    g.change_level(1)
    b.place_item(
        board_items.Wall(sprixel=core.Sprixel(" ", core.Color(255, 255, 0))), 10, 10
    )
    g.screen.place(b, g.screen.height - b.height - 1, 0)

    g.run()
