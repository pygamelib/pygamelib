from pygamelib import engine, constants, board_items
from pygamelib.gfx import core
import time

results = list()


def upd(g, k, dt):
    pass


sc = core.SpriteCollection.load_json_file("tests/panda.spr")
g = engine.Game(user_update=upd, mode=constants.MODE_TBT)
g.player = board_items.Player(sprixel=core.Sprixel("@", None, core.Color(0, 255, 255)))
g.load_board("hac-maps/test_editor.json", 1)
g.change_level(1)
# g.screen.place("+", int(g.screen.width / 2), int(g.screen.height / 2))


# g.screen.place(sc["panda"], 10, 10)
# g.screen.place("This is a text", g.screen.height - 1, 25)
# g.run()
# g.screen.place(g.player, 10, 10)
g.player.pos = [10, 10]
test_times = [0.001, 0.01, 0.02, 0.05]
k = None
go = True
results.append(f"Benchmark runs at resolution: {g.screen.width}x{g.screen.height}")

with g.terminal.cbreak(), g.terminal.hidden_cursor(), g.terminal.fullscreen():

    # **BUFFER BENCHMARK**
    for row in range(0, g.screen._display_buffer.shape[0]):
        for col in range(0, g.screen._display_buffer.shape[1]):
            g.screen.place(
                core.Sprixel(" ", core.Color(row * 4, col, int((row + col) / 2))),
                row,
                col,
            )
    count = 0
    start = time.time()
    while count < 50:
        g.screen.update()
        count += 1
        time.sleep(0.02)
    stop = time.time()
    results.append(
        f"Benchmark (buffer): screen full redraw (50 times with 0.02  sec pause):"
        f"\n\tTotal execution time: {stop-start} sec.\n\tTime per frame: "
        f"{((stop-start-50*0.02)/50)*1000} msec.\n\tFPS: {1/((stop-start-50*0.02)/50)}"
    )
    pr = pc = 20
    g.screen.place(sc["panda"], pr, pc)
    for dt in test_times:
        frames = 120
        start = time.time()
        frame_count = 0
        while frame_count != frames and g.state != constants.STOPPED:
            g.screen.place(
                f"Benchmark (buffer): {dt} {frame_count}/{frames}", 0, 0,
            )
            if k == "q":
                g.state = constants.STOPPED

            if g.player.column == g.screen.width - 1:
                go = False
            elif g.player.column == 0:
                go = True
            g.screen.place(
                core.Sprixel(
                    " ",
                    core.Color(
                        g.player.row * 4,
                        g.player.column,
                        int((g.player.row + g.player.column) / 2),
                    ),
                ),
                g.player.row,
                g.player.column,
            )
            if go:
                g.player.pos[1] += 1
            else:
                g.player.pos[1] -= 1
            g.player.sprixel.bg_color = core.Color(
                g.player.row * 4,
                g.player.column,
                int((g.player.row + g.player.column) / 2),
            )
            g.screen.place(g.player, g.player.row, g.player.column)
            # Test moving a Sprite
            g.screen.place(
                core.Sprixel(" ", core.Color(pr * 4, pc, int((pr + pc) / 2),),), pr, pc
            )
            if (pr + sc["panda"].height) < (g.screen.height - 1):
                pr += 1
            if (pc + sc["panda"].width) < (g.screen.width - 1):
                pc += 1
            g.screen.place(sc["panda"], pr, pc)
            # Update screen (this will trigger Screen.render())
            g.screen.update()
            k = g.terminal.inkey(timeout=dt)
            frame_count += 1
        stop = time.time()
        results.append(
            f"Benchmark (buffer) for :\n\tdt={dt}\n\tframes rendered={frame_count} in "
            f"{stop - start} sec. or {(stop-start)/frame_count} sec. per frame\n\t"
            f"Actual rendering time per frame: {((stop-start)/frame_count - dt)*1000} "
            f"msec.\n\tFPS: {1/((stop-start)/frame_count - dt)}"
        )

    # **DISPLAY/BLESSED BENCHMARK**
    g.clear_screen()
    # print(g.terminal.home, end="")
    count = 0
    start = time.time()
    while count < 50:
        for row in range(0, g.terminal.height):
            for col in range(0, g.terminal.width):
                g.screen.display_at(
                    core.Sprixel(" ", core.Color(row * 4, col, int((row + col) / 2))),
                    row,
                    col,
                    end="",
                )
        count += 1
        time.sleep(0.02)
    stop = time.time()
    results.append(
        f"Benchmark (blessed): screen full redraw (50 times with 0.02  sec pause):\n\t"
        f"Total execution time: {stop-start} sec.\n\tTime per frame: "
        f"{((stop-start-50*0.02)/50)*1000} msec.\n\tFPS: {1/((stop-start-50*0.02)/50)}"
    )

    for dt in test_times:
        frames = 120
        start = time.time()
        frame_count = 0
        while frame_count != frames and g.state != constants.STOPPED:
            g.screen.display_at(
                f"{g.terminal.home}Benchmark (blessed): {dt} {frame_count}/{frames}",
                0,
                0,
                end="",
            )
            if k == "q":
                g.state = constants.STOPPED

            if g.player.column == g.screen.width - 1:
                go = False
            elif g.player.column == 0:
                go = True
            row = g.player.row
            col = g.player.column
            g.screen.display_at(
                core.Sprixel(" ", core.Color(row * 4, col, int((row + col) / 2))),
                row,
                col,
                end="",
            )
            if go:
                g.player.pos[1] += 1
            else:
                g.player.pos[1] -= 1
            col = g.player.column
            g.screen.display_at(
                core.Sprixel(
                    g.player.sprixel.model,
                    core.Color(row * 4, col, int((row + col) / 2)),
                    g.player.sprixel.fg_color,
                ),
                row,
                col,
                end="",
            )
            k = g.terminal.inkey(timeout=dt)
            frame_count += 1
        stop = time.time()
        results.append(
            f"Benchmark (blessed) for :\n\tdt={dt}\n\tframes rendered={frame_count} in "
            f"{stop - start} sec. or {(stop-start)/frame_count} sec. per frame\n\t"
            f"Actual rendering time per frame: {((stop-start)/frame_count - dt)*1000} "
            f"msec.\n\tFPS: {1/((stop-start)/frame_count - dt)}"
        )

print("\n=========== Benchmark results ===========")
for r in results:
    print(r)
