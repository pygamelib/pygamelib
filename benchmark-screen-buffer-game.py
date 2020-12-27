from pygamelib import engine, constants, board_items, base, actuators
from pygamelib.gfx import core
from pygamelib.assets import graphics
import time

results = list()


def upd(g, k, dt):
    pass


def draw_box(game, row, column, height, width, selected=False, title=""):
    color = ""
    end_color = ""
    scr = game.screen
    if selected:
        color = base.Fore.GREEN + base.Style.BRIGHT
        end_color = base.Style.RESET_ALL
    scr.display_at(
        f"{color}{graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_RIGHT}"
        f"{graphics.BoxDrawings.LIGHT_HORIZONTAL*round(width/2-1-len(title)/2)}"
        f"{title}"
        f"{graphics.BoxDrawings.LIGHT_HORIZONTAL*round(width/2-1-len(title)/2)}"
        f"{graphics.BoxDrawings.LIGHT_HORIZONTAL*(width-round(width/2-1-len(title)/2)*2-len(title)-2)}"  # noqa: E501
        f"{graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_LEFT}{end_color}",
        row,
        column,
    )
    for r in range(1, height - 1):
        scr.display_at(
            f"{color}{graphics.BoxDrawings.LIGHT_VERTICAL}{end_color}", row + r, column
        )
        scr.display_at(
            f"{color}{graphics.BoxDrawings.LIGHT_VERTICAL}{end_color}",
            row + r,
            column + width - 1,
        )
        scr.display_at(
            f"{color}{graphics.BoxDrawings.LIGHT_ARC_UP_AND_RIGHT}"
            f"{graphics.BoxDrawings.LIGHT_HORIZONTAL*(width-2)}"
            f"{graphics.BoxDrawings.LIGHT_ARC_UP_AND_LEFT}{end_color}",
            row + height - 1,
            column,
        )


print("pygamelib benchmark\nLoading resources:", end="")
print("Sprites...", end="")
sc = core.SpriteCollection.load_json_file("tests/pgl-benchmark.spr")
print("done")
print("Game engine...", end="")
g = engine.Game(user_update=upd, mode=constants.MODE_TBT)
print("done")
if g.screen.width < 155:
    print(
        base.Text.red_bright(
            "Your console/terminal needs to be at least 155 columns wide"
            " to run that benchmark."
        )
    )
    exit()
if g.screen.height < 65:
    print(
        base.Text.red_bright(
            "Your console/terminal needs to be at least 65 columns high"
            " to run that benchmark."
        )
    )
    exit()
g.player = board_items.Player(sprixel=core.Sprixel("@@", None, core.Color(0, 255, 255)))
# g.load_board("hac-maps/test_editor.json", 1)
print("Test Board...", end="")
g.load_board("hac-maps/benchmark.json", 1)
print("done")
g.change_level(1)
# g.display_board()
# time.sleep(1)
g.clear_screen()
results.append(f"Benchmark runs at resolution: {g.screen.width}x{g.screen.height}")
# g.screen.place("+", int(g.screen.width / 2), int(g.screen.height / 2))


# g.screen.place(sc["panda"], 10, 10)
# g.screen.place("This is a text", g.screen.height - 1, 25)
# g.run()
# g.screen.place(g.player, 10, 10)
g.player.pos = [10, 10]
# path
# (5,19), (19,19), (24,32)
# bg color 33, 99, 247
for row in range(0, g.screen._display_buffer.shape[0]):
    for col in range(0, g.screen._display_buffer.shape[1]):
        g.screen.place(
            core.Sprixel(" ", core.Color(33, 99, 247)), row, col,
        )
spr_start = time.time()
g.screen.place(sc["pgl-benchmark"], int(g.screen.height / 2) - 14, 0)
g.screen.update()

g.player.actuator = actuators.PathFinder(game=g, parent=g.player)
test_times = [0.001, 0.01, 0.02, 0.05]
k = None
go = True

g.clear_screen()
with g.terminal.cbreak(), g.terminal.hidden_cursor(), g.terminal.fullscreen():
    spr_stop = time.time()
    results.append(
        f"Sprite (place, render and update screen), size ({sc['pgl-benchmark'].width}x"
        f"{sc['pgl-benchmark'].height}): {round(spr_stop-spr_start, 2)*1000}"
        f" msec. or {round(1/(spr_stop-spr_start))} FPS."
    )
    spr_start = time.time()
    for i in range(0, 200):
        g.screen.update()
        time.sleep(0.01)
    spr_stop = time.time()
    results.append(
        f"Sprite 200 updates in: {round(spr_stop-spr_start, 2)*1000}"
        f" msec. or {round(200/(spr_stop-spr_start))} FPS."
    )
    g.screen.clear_buffers()
    g.clear_screen()
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
        g.screen.place(
            f"FPS: {round(frame_count/((time.time()-start)-dt*frame_count))}", 1, 20
        )
        if frame_count == 240:
            stop = time.time()
            results.append(
                f"Benchmark (buffer - phase 1) for :\n\tdt={dt}\n\tframes rendered="
                f"{frame_count} in "
                f"{round(stop - start, 5)} sec. or {round((stop-start)/frame_count, 5)}"
                f" sec. per frame\n\tActual rendering time per frame: "
                f"{round(((stop-start)/frame_count - dt)*1000, 2)} "
                f"msec.\n\tFPS: {round(1/((stop-start)/frame_count - dt))}"
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
