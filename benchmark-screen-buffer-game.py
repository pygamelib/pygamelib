from pygamelib import engine, constants, board_items, base
from pygamelib.gfx import core
import time

results = list()


def upd(g, k, dt):
    pass


sc = core.SpriteCollection.load_json_file("tests/panda.spr")
g = engine.Game(user_update=upd, mode=constants.MODE_TBT)
if g.screen.width < 155:
    print(
        base.Text.red_bright(
            "Your console/terminal needs to be at least 155 columns wide"
            " to run that benchmark."
        )
    )
    exit()
g.player = board_items.Player(sprixel=core.Sprixel("@@", None, core.Color(0, 255, 255)))
# g.load_board("hac-maps/test_editor.json", 1)
g.load_board("hac-maps/benchmark.json", 1)
g.change_level(1)
# g.display_board()
# time.sleep(1)
g.clear_screen()
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
    dt = 0.02
    frame_count = 0
    start = time.time()
    phase2 = 0

    g.screen.place(
        f"Game benchmark - console resolution: {g.terminal.width}x{g.terminal.height}",
        0,
        0,
    )
    g.screen.place(g.current_board(), 35, 55)
    g.start()
    while frame_count < 480:
        g.screen.place(f"Frame count: {frame_count}", 1, 0)
        if frame_count == 240:
            stop = time.time()
            results.append(
                f"Benchmark (buffer - phase 1) for :\n\tdt={dt}\n\tframes rendered="
                f"{frame_count} in "
                f"{stop - start} sec. or {(stop-start)/frame_count} sec. per frame\n\t"
                f"Actual rendering time per frame: "
                f"{((stop-start)/frame_count - dt)*1000} "
                f"msec.\n\tFPS: {1/((stop-start)/frame_count - dt)}"
            )
            g.screen.place(g.current_board(), 2, 0)
            phase2 = time.time()
        g.actuate_npcs(1)
        g.screen.update()
        g.terminal.inkey(timeout=dt)
        frame_count += 1
    stop = time.time()
    results.append(
        f"Benchmark (buffer - phase 2) for :\n\tdt={dt}\n\tframes rendered="
        f"{frame_count-240}"
        f" in {stop - phase2} sec. or {(stop-phase2)/(frame_count-240)} sec. "
        f"per frame\n\t"
        f"Actual rendering time per frame: "
        f"{((stop-phase2)/(frame_count-240) - dt)*1000} "
        f"msec.\n\tFPS: {1/((stop-phase2)/(frame_count-240) - dt)}"
    )
    results.append(
        f"Benchmark (buffer - overall) for :\n\tdt={dt}\n\tframes rendered="
        f"{frame_count}"
        f" in {stop - start} sec. or {(stop-start)/frame_count} sec. per frame\n\t"
        f"Actual rendering time per frame: {((stop-start)/frame_count - dt)*1000} "
        f"msec.\n\tFPS: {1/((stop-start)/frame_count - dt)}"
    )

print("\n=========== Benchmark results ===========")
for r in results:
    print(r)
