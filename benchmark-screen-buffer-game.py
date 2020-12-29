from pygamelib import engine, constants, board_items, base
from pygamelib.gfx import core
from pygamelib.assets import graphics
import time

results = list()


def upd(g, k, dt):
    pass


def draw_box(game, row, column, height, width, title=""):
    scr = game.screen
    scr.place(
        f"{graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_RIGHT}"
        f"{graphics.BoxDrawings.LIGHT_HORIZONTAL*round(width/2-1-len(title)/2)}"
        f"{title}"
        f"{graphics.BoxDrawings.LIGHT_HORIZONTAL*round(width/2-1-len(title)/2)}"
        f"{graphics.BoxDrawings.LIGHT_HORIZONTAL*(width-round(width/2-1-len(title)/2)*2-len(title)-2)}"  # noqa: E501
        f"{graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_LEFT}",
        row,
        column,
    )
    vert_sprix = core.Sprixel(graphics.BoxDrawings.LIGHT_VERTICAL)
    for r in range(1, height - 1):
        scr.place(vert_sprix, row + r, column)
        scr.place(
            vert_sprix, row + r, column + width - 1,
        )
        scr.place(
            f"{graphics.BoxDrawings.LIGHT_ARC_UP_AND_RIGHT}"
            f"{graphics.BoxDrawings.LIGHT_HORIZONTAL*(width-2)}"
            f"{graphics.BoxDrawings.LIGHT_ARC_UP_AND_LEFT}",
            row + height - 1,
            column,
        )


print("pygamelib benchmark\nLoading resources:", end="")
print("Sprites...", end="")
sc = core.SpriteCollection.load_json_file("tests/pgl-benchmark.spr")
panda = core.SpriteCollection.load_json_file("tests/panda.spr")["panda"]
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
    baseline_fps = round(200 / (spr_stop - spr_start))
    results.append(
        f"Sprite 200 updates in: {round(spr_stop-spr_start, 2)*1000}"
        f" msec. or {baseline_fps} FPS."
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
    draw_box(g, 35, 1, g.current_board().height, 40, "Benchmark")
    g.screen.place(panda, round((35 + g.current_board().height) - panda.height - 1), 2)
    panda.row = round((35 + g.current_board().height) - panda.height - 1)
    panda.column = 2
    g.screen.place("Progress: ", 38, 2)
    g.screen.place("FPS/Max. FPS: |", 39, 2)
    g.screen.place(core.Sprixel("|"), 39, 37)
    g.screen.place(
        base.Text("FPS graph:", style=constants.BOLD + constants.UNDERLINE), 40, 2
    )
    low_graph_row = round((35 + g.current_board().height) - panda.height - 2)
    g.start()
    max_fps = 0
    max_frames = 480
    panda_steps = int(max_frames / (37 - panda.width))
    last_col = 0
    while frame_count < max_frames:
        current_fps = round(frame_count / ((time.time() - start) - dt * frame_count))
        if current_fps > max_fps:
            max_fps = current_fps
            g.screen.place(
                core.Sprixel("|", None, core.Color(0, 0, 255)),
                39,
                16 + int(max_fps * 20 / (baseline_fps + 10)),
            )
        for i in range(16, 16 + int(max_fps * 20 / (baseline_fps + 10))):
            g.screen.delete(39, i)
        for i in range(16, 16 + int(current_fps * 20 / (baseline_fps + 10))):
            g.screen.place(
                core.Sprixel(" ", core.Color(0, 0, 255)), 39, i,
            )
        fps_str = f"FPS: {current_fps}"
        g.screen.place(f"Frame count: {frame_count}", 1, 0)
        g.screen.place(fps_str, 1, 20)
        g.screen.place(fps_str, 36, 2)
        g.screen.place(f"Frame #{frame_count}", 36, 20)
        g.screen.place(f"Maximum FPS: {max_fps}", 37, 2)
        for i in range(0, int((frame_count * 29) / max_frames)):
            g.screen.place(core.Sprixel.green_rect(), 38, 12 + i)
        current_col = 2 + int((frame_count * 38) / max_frames)
        if current_col > last_col:
            for i in range(
                low_graph_row
                - int(current_fps * (low_graph_row - 41) / (baseline_fps + 10)),
                low_graph_row,
            ):
                g.screen.place(
                    core.Sprixel(" ", core.Color(0, 0, 255)), i, current_col,
                )
            last_col = current_col
        if frame_count == int(max_frames / 2):
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
        if frame_count % panda_steps == 0:
            g.screen.delete(panda.row, panda.column)
            g.screen.place(panda, panda.row, panda.column + 1)
            panda.column += 1
        g.actuate_npcs(1)
        g.screen.update()
        g.terminal.inkey(timeout=dt)
        frame_count += 1
    stop = time.time()
    results.append(
        f"Benchmark (buffer - phase 2) for :\n\tdt={dt}\n\tframes rendered="
        f"{frame_count-int(max_frames/2)}"
        f" in {stop - phase2} sec. or {(stop-phase2)/(frame_count-int(max_frames/2))}"
        f" sec. per frame\n\t"
        f"Actual rendering time per frame: "
        f"{round(((stop-phase2)/(frame_count-int(max_frames/2)) - dt)*1000,2)} "
        f"msec.\n\tFPS: {round(1/((stop-phase2)/(frame_count-int(max_frames/2)) - dt))}"
    )
    results.append(
        f"Benchmark (buffer - overall) for :\n\tdt={dt}\n\tframes rendered="
        f"{frame_count}"
        f" in {stop - start} sec. or {(stop-start)/frame_count} sec. per frame\n\t"
        f"Actual rendering time per frame: "
        f"{round(((stop-start)/frame_count - dt)*1000,2)} "
        f"msec.\n\tFPS: {round(1/((stop-start)/frame_count - dt))}"
    )

print("\n=========== Benchmark results ===========")
for r in results:
    print(r)
