import examples_includes  # noqa: F401
from pygamelib.gfx import particles, core
from pygamelib import engine, base, board_items, constants
from pygamelib.assets import graphics
from extra_lib import utilities

import random
import time
import copy


class State:
    current_state = 0
    intro_sprite = None
    night_bg = None
    intro_sprite_pos = None
    altar_sprite = None
    intro_fade_in_rate = 1.0
    particle_emitters = []
    black = core.Color(0, 0, 0)
    cyan = core.Color(0, 255, 255)
    dark_blue = core.Color(7, 2, 40)
    gravity = base.Vector2D(0.2, 0.0)
    wind_up = base.Vector2D(-0.2, 0.0)
    firework_colors = [
        core.Color(255, 0, 0),
        core.Color(0, 255, 0),
        core.Color(0, 0, 255),
        core.Color(255, 255, 0),
        core.Color(255, 0, 255),
        core.Color(0, 255, 255),
        core.Color(255, 255, 255),
    ]
    firework_sprixels = [
        core.Sprixel(graphics.GeometricShapes.BULLET),
        core.Sprixel(graphics.GeometricShapes.BLACK_CIRCLE),
    ]
    frwk_create = 0
    frwk_delta = 0
    frwk_spr_start_col = 0
    frwk_spr_stop_row = 0
    frwk_remaining = 50

    @staticmethod
    def next_state():
        State.current_state += 1


bench_state = State()
bench_timer = utilities.BenchmarkTimer()


def process_basic_keystroke(g: engine.Game, key):
    if key == "q":
        bench_timer.stop_timer(bench_state.current_state)
        g.stop()


def clear_screen(screen, color=bench_state.black):
    bsp = core.Sprixel(" ", color)
    for r in range(screen.height):
        for c in range(screen.width):
            screen.place(bsp, r, c)


def init_intro_screen(g: engine.Game):
    bench_timer.start_timer(bench_state.current_state)
    bench_timer.set_label(bench_state.current_state, "Intro scene initialization")
    screen = g.screen
    intro_asset = core.SpriteCollection.load_json_file("assets/pygamelib-logo.spr")
    sprite_collection = core.SpriteCollection.load_json_file("assets/1719775.spr")
    altar_collection = core.SpriteCollection.load_json_file("assets/altar.spr")
    bench_state.altar_sprite = altar_collection["altar"]
    bench_state.night_bg = sprite_collection["1719775"]
    resized_sprite = core.Sprite(size=[screen.width, screen.height])
    bench_state.frwk_spr_stop_row = (
        screen.height
        if screen.height <= bench_state.night_bg.height
        else bench_state.night_bg.height
    )
    bench_state.frwk_spr_start_col = bench_state.night_bg.width - screen.width
    for r in range(0, bench_state.frwk_spr_stop_row):
        cs = 0
        for c in range(bench_state.frwk_spr_start_col, bench_state.night_bg.width):
            # screen.place(copy.deepcopy(bench_state.night_bg.sprixel(r, c)), r, cs, 1)
            resized_sprite.set_sprixel(r, cs, bench_state.night_bg.sprixel(r, c))
            cs += 1
    bench_state.night_bg = resized_sprite
    clear_screen(screen)
    screen.place(
        intro_asset["pygamelib-logo"].tint(
            bench_state.black, bench_state.intro_fade_in_rate
        ),
        screen.vcenter - int(intro_asset["pygamelib-logo"].height / 2),
        screen.hcenter - round(intro_asset["pygamelib-logo"].width / 2),
    )
    bench_state.intro_sprite = intro_asset["pygamelib-logo"]
    bench_state.intro_sprite_pos = [
        screen.vcenter - int(intro_asset["pygamelib-logo"].height / 2),
        screen.hcenter - round(intro_asset["pygamelib-logo"].width / 2),
    ]
    bench_timer.count_frame(bench_state.current_state)

    # next_phase("Pygamelib logo fade in")
    bench_timer.stop_timer(bench_state.current_state)
    bench_state.next_state()
    bench_timer.start_timer(bench_state.current_state)
    bench_timer.set_label(
        bench_state.current_state,
        "Pygamelib logo fade in [Blending large sprite with mask]",
    )


def init_firework(screen: engine.Screen):
    clear_screen(screen)
    screen.place(bench_state.night_bg, 0, 0, 1)
    bench_state.frwk_create = time.time()
    bench_state.frwk_delta = random.uniform(0.05, 0.3)


def next_phase(label: str) -> None:
    bench_timer.stop_timer(bench_state.current_state)
    bench_state.next_state()
    bench_timer.start_timer(bench_state.current_state)
    bench_timer.set_label(bench_state.current_state, label)


def benchmark_intro_update(g: engine.Game, key, dt):
    global test
    # P
    # 16,46
    # 10,46
    # 10,53
    # 14,53
    # 15,52
    # 15,47
    screen = g.screen
    ph = bench_timer.phases[bench_state.current_state]
    screen.place(
        base.Text(
            f"Phase: {bench_state.current_state} FPS: {round(ph['frames']/(time.perf_counter()-ph['start']-g.input_lag*ph['frames']))}",
            bg_color=bench_state.black,
        ),
        0,
        0,
    )
    screen.place(
        base.Text(
            f"{ph['label']}",
            bg_color=bench_state.black,
            fg_color=bench_state.cyan,
        ),
        1,
        0,
    )
    process_basic_keystroke(g, key)

    if bench_state.intro_fade_in_rate > 0:
        screen.place(
            bench_state.intro_sprite.tint(
                bench_state.black, bench_state.intro_fade_in_rate
            ),
            bench_state.intro_sprite_pos[0],
            bench_state.intro_sprite_pos[1],
        )
        bench_state.intro_fade_in_rate -= 0.04
        # bench_timer.count_frame(bench_state.current_state)
        if bench_state.intro_fade_in_rate <= 0.0:
            screen.place(
                bench_state.intro_sprite,
                bench_state.intro_sprite_pos[0],
                bench_state.intro_sprite_pos[1],
            )
            # bench_timer.count_frame(bench_state.current_state)
            # next_phase("Pygamelib logo + particles [create particle emitters]")
            bench_timer.stop_timer(bench_state.current_state)
            bench_state.next_state()
            bench_timer.start_timer(bench_state.current_state)
            bench_timer.set_label(
                bench_state.current_state,
                f"Pygamelib logo + particles [create {len(utilities.logo_positions)} particle emitters]",
            )

    else:
        if bench_state.current_state == 2:
            expl_props = particles.EmitterProperties(
                variance=2.0,
                emit_number=20,
                emit_rate=0.01,
                lifespan=1,
                particle=particles.ColorParticle(
                    sprixel=core.Sprixel(graphics.GeometricShapes.BLACK_CIRCLE),
                    start_color=core.Color(0, 255, 255),
                    stop_color=core.Color(0, 0, 0),
                ),
                particle_lifespan=5,
                radius=1,
            )
            i = 0.1
            for p in utilities.logo_positions:
                expl_props.emit_rate = i
                emt = particles.CircleEmitter(expl_props)
                screen.place(
                    emt,
                    bench_state.intro_sprite_pos[0] + p[0],
                    bench_state.intro_sprite_pos[1] + p[1],
                    2,
                )
                i += 0.1
                bench_state.particle_emitters.append(emt)
            # bench_timer.count_frame(bench_state.current_state)
            # next_phase("Pygamelib logo + particles [run emitters until finished]")
            bench_timer.stop_timer(bench_state.current_state)
            bench_state.next_state()
            bench_timer.start_timer(bench_state.current_state)
            bench_timer.set_label(
                bench_state.current_state,
                "Pygamelib logo + particles [run emitters until finished]",
            )
        elif bench_state.current_state == 3:
            for emt in bench_state.particle_emitters:
                if not emt.finished():
                    emt.emit()
                    emt.update()
            for i in range(len(bench_state.particle_emitters) - 1, -1, -1):
                if bench_state.particle_emitters[i].finished():
                    del bench_state.particle_emitters[i]
            if len(bench_state.particle_emitters) == 0:
                # screen.delete(1, 0)
                screen.place(core.Sprixel(" ", bench_state.black), 1, 0)
                # next_phase("End for now")
                bench_timer.stop_timer(bench_state.current_state)
                bench_state.next_state()
                clear_screen(screen)
                bench_timer.start_timer(bench_state.current_state)
                bench_timer.set_label(
                    bench_state.current_state,
                    "Emitter with low number of particles [ParticleEmitter + "
                    "ColorParticle @ 50 particles per sec. for 150 emission cycles]",
                )
                emt_props = particles.EmitterProperties(
                    screen.vcenter,
                    screen.hcenter,
                    lifespan=100,
                    variance=2.5,
                    emit_number=5,
                    emit_rate=0.1,
                    particle=particles.ColorParticle(
                        sprixel=core.Sprixel(
                            graphics.GeometricShapes.BLACK_CIRCLE,
                            bg_color=core.Color(0, 0, 0),
                        ),
                        start_color=core.Color(0, 255, 255),
                        stop_color=core.Color(0, 0, 0),
                    ),
                    particle_lifespan=25,
                )
                bench_state.particle_emitters.append(
                    particles.ParticleEmitter(emt_props)
                )
                screen.place(
                    bench_state.particle_emitters[-1], screen.vcenter, screen.hcenter, 2
                )
                g.user_update = update_low_emitter

    bench_timer.count_frame(bench_state.current_state)
    screen.update()


def update_low_emitter(g: engine.Game, key, dt):
    global test
    screen = g.screen
    ph = bench_timer.phases[bench_state.current_state]
    fps = round(
        ph["frames"] / (time.perf_counter() - ph["start"] - g.input_lag * ph["frames"])
    )
    screen.place(
        base.Text(
            f"Phase: {bench_state.current_state} FPS: {fps}",
            bg_color=bench_state.black,
        ),
        0,
        0,
    )
    screen.place(
        base.Text(
            f"{ph['label']}",
            bg_color=bench_state.black,
            fg_color=bench_state.cyan,
        ),
        1,
        0,
    )
    process_basic_keystroke(g, key)
    for emt in bench_state.particle_emitters:
        if not emt.finished():
            emt.emit()
            emt.update()
    for i in range(len(bench_state.particle_emitters) - 1, -1, -1):
        if bench_state.particle_emitters[i].finished():
            del bench_state.particle_emitters[i]
    if len(bench_state.particle_emitters) == 0:
        bench_timer.stop_timer(bench_state.current_state)
        bench_state.next_state()
        clear_screen(screen)
        bench_timer.start_timer(bench_state.current_state)
        bench_timer.set_label(
            bench_state.current_state,
            "Emitter with mid number of particles [ParticleEmitter + ColorParticle @ "
            "200 particles per sec. for 150 emission cycles]",
        )
        emt_props = particles.EmitterProperties(
            screen.vcenter,
            screen.hcenter,
            lifespan=150,
            variance=2.5,
            emit_number=20,
            emit_rate=0.1,
            particle=particles.ColorParticle(
                sprixel=core.Sprixel(
                    graphics.GeometricShapes.BLACK_CIRCLE,
                    bg_color=core.Color(0, 0, 0),
                ),
                start_color=core.Color(110, 5, 205),
                stop_color=core.Color(0, 0, 0),
            ),
            particle_lifespan=25,
        )
        bench_state.particle_emitters.append(particles.ParticleEmitter(emt_props))
        screen.place(
            bench_state.particle_emitters[-1], screen.vcenter, screen.hcenter, 2
        )
        g.user_update = update_mid_emitter

    bench_timer.count_frame(bench_state.current_state)
    screen.update()


def update_mid_emitter(g: engine.Game, key, dt):
    global test
    screen = g.screen
    ph = bench_timer.phases[bench_state.current_state]
    screen.place(
        base.Text(
            f"Phase: {bench_state.current_state} FPS: {round(ph['frames']/(time.perf_counter()-ph['start']-g.input_lag*ph['frames']))}",
            bg_color=bench_state.black,
        ),
        0,
        0,
    )
    screen.place(
        base.Text(
            f"{ph['label']}",
            bg_color=bench_state.black,
            fg_color=bench_state.cyan,
        ),
        1,
        0,
    )
    process_basic_keystroke(g, key)
    for emt in bench_state.particle_emitters:
        if not emt.finished():
            emt.emit()
            emt.update()
    for i in range(len(bench_state.particle_emitters) - 1, -1, -1):
        if bench_state.particle_emitters[i].finished():
            del bench_state.particle_emitters[i]
    if len(bench_state.particle_emitters) == 0:
        bench_timer.stop_timer(bench_state.current_state)
        bench_state.next_state()
        clear_screen(screen)
        bench_timer.start_timer(bench_state.current_state)
        bench_timer.set_label(
            bench_state.current_state,
            "Emitter with high number of particles [ParticleEmitter + ColorParticle @ "
            "500 particles per sec. for 150 emission cycles]",
        )
        emt_props = particles.EmitterProperties(
            screen.vcenter,
            screen.hcenter,
            lifespan=150,
            variance=2.5,
            emit_number=50,
            emit_rate=0.1,
            particle=particles.ColorParticle(
                sprixel=core.Sprixel(
                    graphics.GeometricShapes.BLACK_CIRCLE,
                    bg_color=core.Color(0, 0, 0),
                ),
                start_color=core.Color(160, 0, 105),
                stop_color=core.Color(0, 0, 0),
            ),
            particle_lifespan=25,
        )
        bench_state.particle_emitters.append(particles.ParticleEmitter(emt_props))
        screen.place(
            bench_state.particle_emitters[-1], screen.vcenter, screen.hcenter, 2
        )
        g.user_update = update_high_emitter

    bench_timer.count_frame(bench_state.current_state)
    screen.update()


def update_high_emitter(g: engine.Game, key, dt):
    global test
    screen = g.screen
    ph = bench_timer.phases[bench_state.current_state]
    screen.place(
        base.Text(
            f"Phase: {bench_state.current_state} FPS: {round(ph['frames']/(time.perf_counter()-ph['start']-g.input_lag*ph['frames']))}",
            bg_color=bench_state.black,
        ),
        0,
        0,
    )
    screen.place(
        base.Text(
            f"{ph['label']}",
            bg_color=bench_state.black,
            fg_color=bench_state.cyan,
        ),
        1,
        0,
    )
    process_basic_keystroke(g, key)
    for emt in bench_state.particle_emitters:
        if not emt.finished():
            emt.emit()
            emt.update()
    for i in range(len(bench_state.particle_emitters) - 1, -1, -1):
        if bench_state.particle_emitters[i].finished():
            del bench_state.particle_emitters[i]
    if len(bench_state.particle_emitters) == 0:
        bench_timer.stop_timer(bench_state.current_state)
        bench_state.next_state()
        clear_screen(screen)
        bench_timer.start_timer(bench_state.current_state)
        bench_timer.set_label(
            bench_state.current_state,
            f"Firework - {bench_state.frwk_remaining} explosions [Particle and Circle "
            "emitter + RandomColor particle with large sprite in the background + "
            "gravity]",
        )
        init_firework(screen)
        g.user_update = firework_update

    bench_timer.count_frame(bench_state.current_state)
    screen.update()


def firework_update(g: engine.Game, key, dt):
    global test
    screen = g.screen
    ph = bench_timer.phases[bench_state.current_state]
    sprix = screen.get(0, 0).sprixel(0, 0)
    fps = round(
        ph["frames"] / (time.perf_counter() - ph["start"] - g.input_lag * ph["frames"])
    )
    text = base.Text(
        f"Phase: {bench_state.current_state} FPS: {fps} ",
        bg_color=sprix.bg_color,
    )
    screen.place(text, 0, 1, 2)
    screen.place(
        base.Text(
            f"{ph['label']}",
            bg_color=sprix.bg_color,
            fg_color=bench_state.cyan,
        ),
        0,
        text.length + 2,
        2,
    )
    process_basic_keystroke(g, key)

    # Firework

    if time.time() - bench_state.frwk_create >= bench_state.frwk_delta:
        row = random.randrange(5, screen.height - 5)
        col = random.randrange(10, screen.width - 10)
        c = copy.copy(random.choice(bench_state.firework_colors))
        cur_emt = None
        props = particles.EmitterProperties(
            row,
            col,
            variance=random.uniform(0.0, 3.0),
            emit_number=random.randint(20, 50),
            emit_rate=0.1,
            lifespan=1,
            particle=particles.ColorParticle(
                sprixel=random.choice(bench_state.firework_sprixels),
                start_color=c,
                # stop_color=core.Color(0, 0, 0),
            ),
            particle_lifespan=random.uniform(8.0, 10.0),
            radius=random.uniform(2.0, 4.0),
        )
        cur_emt = particles.CircleEmitter(props)
        # g.session_log(f"[FIREWORK::Run] Placing new emitter at {row},{col}")
        screen.place(cur_emt, row, col, 2)
        bench_state.particle_emitters.append(cur_emt)
        bench_state.frwk_create = time.time()
        bench_state.frwk_delta = random.uniform(0.1, 1.0)
        bench_state.frwk_remaining -= 1

    for emt in bench_state.particle_emitters:
        if not emt.finished():
            emt.emit()
            emt.apply_force(bench_state.gravity)
            emt.update()

    for i in range(len(bench_state.particle_emitters) - 1, -1, -1):
        if bench_state.particle_emitters[i].finished():
            # g.session_log(
            #     f"[FIREWORK::Run] emitter at {bench_state.particle_emitters[i].row},{bench_state.particle_emitters[i].column} is finished => Removing"
            # )
            screen.delete(
                bench_state.particle_emitters[i].row,
                bench_state.particle_emitters[i].column,
            )
            del bench_state.particle_emitters[i]

    # bench_state.frwk_remaining -= 1
    if bench_state.frwk_remaining <= 0:
        bench_timer.stop_timer(bench_state.current_state)
        init_temple_scene(screen)
        bench_state.next_state()
        bench_timer.start_timer(bench_state.current_state)
        bench_timer.set_label(
            bench_state.current_state,
            "Altar with fire torch (CircleEmitter + ColorPartitionParticle)",
        )
        g.user_update = temple_scene_update
        # g.stop()

    bench_timer.count_frame(bench_state.current_state)
    screen.update()


def init_temple_scene(screen):
    # CircleEmitter + ColorPartitionParticle
    # Variance: 0.3
    # Radius: 0.4
    # bg color 7, 2, 40
    # emitters: 19,24 19,34 19,122 19,132
    # fire color : 45,151,227
    clear_screen(screen, core.Color(7, 2, 40))
    screen.place(
        bench_state.altar_sprite,
        screen.vcenter - int(bench_state.altar_sprite.height / 2),
        0,
    )
    emt_props = particles.EmitterProperties(
        screen.vcenter,
        screen.hcenter,
        lifespan=150,
        variance=0.3,
        emit_number=10,
        emit_rate=0.1,
        particle=particles.ColorPartitionParticle(
            start_color=core.Color(45, 151, 227),
            stop_color=core.Color(7, 2, 40),
        ),
        particle_lifespan=5,
        radius=0.4,
    )
    for c in [[20, 24], [20, 35], [20, 122], [20, 133]]:
        bench_state.particle_emitters.append(particles.CircleEmitter(emt_props))
        screen.place(
            bench_state.particle_emitters[-1],
            screen.vcenter - int(bench_state.altar_sprite.height / 2) + c[0],
            c[1],
            2,
        )


def temple_scene_update(g: engine.Game, key, dt):
    global test
    screen = g.screen
    ph = bench_timer.phases[bench_state.current_state]
    fps = round(
        ph["frames"] / (time.perf_counter() - ph["start"] - g.input_lag * ph["frames"])
    )
    text = base.Text(
        f"Phase: {bench_state.current_state} FPS: {fps} ",
        bg_color=bench_state.dark_blue,
    )
    screen.place(text, 0, 1, 2)
    screen.place(
        base.Text(
            f"{ph['label']}",
            bg_color=bench_state.dark_blue,
            fg_color=bench_state.cyan,
        ),
        0,
        text.length + 2,
        2,
    )
    process_basic_keystroke(g, key)

    for emt in bench_state.particle_emitters:
        if not emt.finished():
            emt.emit()
            emt.apply_force(bench_state.wind_up)
            emt.update()

    for i in range(len(bench_state.particle_emitters) - 1, -1, -1):
        if bench_state.particle_emitters[i].finished():
            screen.delete(
                bench_state.particle_emitters[i].row,
                bench_state.particle_emitters[i].column,
            )
            del bench_state.particle_emitters[i]

    if len(bench_state.particle_emitters) <= 0:
        bench_timer.stop_timer(bench_state.current_state)
        g.stop()
    elif bench_state.particle_emitters[0].lifespan % 10 == 0:
        bench_state.wind_up.column = random.uniform(-0.2, 0.2)

    bench_timer.count_frame(bench_state.current_state)
    screen.update()


if __name__ == "__main__":
    # Min rez 65*159
    g = engine.Game.instance(
        player=board_items.Player(
            sprixel=core.Sprixel(
                "@",
                fg_color=core.Color(0, 255, 255),
            ),
            movement_speed=0.01,
        ),
        user_update=benchmark_intro_update,
        mode=constants.MODE_RT,
        input_lag=0.1,
    )
    if g.screen.width >= 159 and g.screen.height >= 65:
        g.DEBUG = True
        b = engine.Board(
            size=[1, 1],
            ui_board_void_cell_sprixel=core.Sprixel(" ", core.Color(180, 180, 180)),
        )
        g.add_board(1, b)
        g.change_level(1)
        init_intro_screen(g)
        g.run()
        # Display benchmark results.
        print(
            base.Text(
                "pygamelib particle engine benchmark",
                fg_color=core.Color(0, 255, 255),
                style=constants.UNDERLINE + constants.BOLD,
            )
        )
        total_time = 0
        total_frames = 0
        for pk in bench_timer.phases.keys():
            ph = bench_timer.phases[pk]
            print(
                f"{base.Text(ph['label'],core.Color(0,255,0))}: {ph['frames']} frames in "
                f"{round(ph['stop']-ph['start']-g.input_lag*ph['frames'],2)} sec. or "
                f"{round(ph['frames']/(ph['stop']-ph['start']-g.input_lag*ph['frames']))} "
                f"FPS"
            )
            total_frames += ph["frames"]
            total_time += ph["stop"] - ph["start"] - g.input_lag * ph["frames"]
        print(
            base.Text(
                f"\nAverage FPS: {round(total_frames/total_time)}",
                fg_color=core.Color(200, 255, 0),
                style=constants.BOLD,
            )
        )
    else:
        print(
            base.Text(
                "The console dimensions need to be at least 159 columns by 65 rows, "
                f"yours is {g.screen.width} by {g.screen.height}",
                core.Color(255, 0, 0),
            )
        )


for l in g.session_logs():
    print(l)
