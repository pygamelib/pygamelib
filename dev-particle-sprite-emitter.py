from pygamelib.gfx.core import Sprite, Sprixel, Color
from pygamelib.engine import Game
from pygamelib.board_items import Player
from pygamelib import constants
from pygamelib.assets import graphics
from pygamelib.gfx.particles import (
    ParticleEmitter,
    ParticleSprixel,
    Particle,
    EmitterProperties,
    SpriteEmitter,
)
import logging, time

expl_props = EmitterProperties(
    variance=2.0,
    emit_number=20,
    emit_rate=0.01,
    lifespan=1,
    particle=Particle(
        sprixel=ParticleSprixel(graphics.GeometricShapes.BULLET),
    ),
    particle_lifespan=25,
    radius=1,
)

particle_emitters = []


def create_sprite(h: int, w: int) -> Sprite:
    new_sprite = Sprite(size=[w, h])
    for r in range(0, h):
        for c in range(0, w):
            new_sprite.set_sprixel(r, c, ParticleSprixel(" ", Color.random()))
    return new_sprite


def update_screen(g: Game, k, dt) -> None:
    if k == "q":
        g.stop()
    elif k == "S":
        g.screen.place(
            create_sprite(5, 10), g.player.screen_row, g.player.screen_column + 1
        )
    elif k == "w":
        g.screen.delete(g.player.screen_row, g.player.screen_column)
        g.screen.place(g.player, g.player.screen_row - 1, g.player.screen_column)
    elif k == "s":
        g.screen.delete(g.player.screen_row, g.player.screen_column)
        g.screen.place(g.player, g.player.screen_row + 1, g.player.screen_column)
    elif k == "a":
        g.screen.delete(g.player.screen_row, g.player.screen_column)
        g.screen.place(g.player, g.player.screen_row, g.player.screen_column - 1)
    elif k == "d":
        g.screen.delete(g.player.screen_row, g.player.screen_column)
        g.screen.place(g.player, g.player.screen_row, g.player.screen_column + 1)
    elif k == "e":
        est = time.perf_counter()
        # Proposed end user API for the sprite emitter.
        spcst = time.perf_counter()
        sp = create_sprite(5, 10)
        logging.debug(
            f"update_screen: sprite creation time: {time.perf_counter() - spcst}"
        )
        g.screen.place(sp, 1, 0)
        expl_props.row = g.player.screen_row + 1
        expl_props.column = g.player.screen_column
        sest = time.perf_counter()
        sprite_emitter = SpriteEmitter(sprite=sp, emitter_properties=expl_props)
        logging.debug(
            f"update_screen: sprite emitter creation time: {time.perf_counter() - sest}"
        )
        g.screen.place(sprite_emitter, g.player.screen_row, g.player.screen_column + 1)
        particle_emitters.append(sprite_emitter)
        logging.debug(f"update_screen: total 'e' time: {time.perf_counter() - est}")

    g.screen.place(
        f"Number of emitters: {len(particle_emitters)} cursor position {g.player.screen_row},{g.player.screen_column}",
        0,
        0,
    )
    # Update the particle emitters
    for _ in range(len(particle_emitters) - 1, -1, -1):
        emt = particle_emitters.pop()
        if emt.finished():
            continue
        emt.emit()
        emt.update()
        # emt.render_to_buffer(
        #     buffer,
        #     emt.row,
        #     emt.column,
        #     buffer_height,
        #     buffer_width,
        # )
        particle_emitters.append(emt)
    g.screen.update()


if __name__ == "__main__":
    logging.basicConfig(filename="dev-sprite-emitter.log", level=logging.DEBUG)
    g = Game(
        player=Player(
            sprixel=Sprixel(
                graphics.BoxDrawings.HEAVY_VERTICAL_AND_HORIZONTAL,
                fg_color=Color(0, 255, 0),
            )
        ),
        user_update=update_screen,
        mode=constants.EngineMode.MODE_REAL_TIME,
    )
    g.ENABLE_SESSION_LOGS = True
    g.screen.place(g.player, g.screen.vcenter - 2, g.screen.hcenter - 5)

    g.run()
