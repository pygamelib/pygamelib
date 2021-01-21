from pygamelib import engine, constants, board_items, base
from pygamelib.gfx import core
from pygamelib.assets import graphics
import time

results = list()


def upd(g, k, dt):
    pass


def draw_box(game, row, column, height, width, title=""):
    scr = game.screen
    scr.display_at(
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
        scr.display_at(vert_sprix, row + r, column)
        scr.display_at(
            vert_sprix,
            row + r,
            column + width - 1,
        )
    scr.display_at(
        f"{graphics.BoxDrawings.LIGHT_ARC_UP_AND_RIGHT}"
        f"{graphics.BoxDrawings.LIGHT_HORIZONTAL*(width-2)}"
        f"{graphics.BoxDrawings.LIGHT_ARC_UP_AND_LEFT}",
        row + height - 1,
        column,
    )


print("pygamelib Direct Display benchmark\n")
print("Loading game engine...", end="", flush=True)
g_start = time.time()
g = engine.Game(user_update=upd, mode=constants.MODE_TBT)
g_stop = time.time()
print("done")
if g.screen.width < 155:
    print(
        base.Text.red_bright(
            "Your console/terminal needs to be at least 155 columns wide"
            f" to run that benchmark (current width is {g.screen.width})."
        )
    )
    exit()
if g.screen.height < 65:
    print(
        base.Text.red_bright(
            "Your console/terminal needs to be at least 65 columns high"
            f" to run that benchmark (current height is {g.screen.height})."
        )
    )
    exit()
g.player = board_items.Player(sprixel=core.Sprixel("@@", None, core.Color(0, 255, 255)))
print("Loading resources: ", end="", flush=True)
load_start = time.time()
sprites = core.SpriteCollection.load_json_file("tests/pgl-benchmark.spr")
panda = sprites["panda"]
polus = sprites["Polus_Map"]
load_stop = time.time()
print("done")
print("Generating Boards: ", end="", flush=True)
gen_start = time.time()
print("Benchmark Board ", end="", flush=True)
g.load_board("hac-maps/benchmark.json", 1)
print("[ok] ", end="", flush=True)
g.change_level(1)
print("High Definition Board ", end="", flush=True)
polus_cam = board_items.Camera()
polus_map = engine.Board(
    size=polus.size,
    ui_borders="",
    enable_partial_display=True,
    partial_display_viewport=[
        int(g.current_board().height / 2),
        g.current_board().width,  # Tricky: The other board uses double characters.
    ],
    partial_display_focus=polus_cam,
    DISPLAY_SIZE_WARNINGS=False,
)
polus_cam.row = 120
polus_cam.column = 0
polus_map.place_item(board_items.Tile(sprite=polus), 0, 0)
gen_stop = time.time()
print("[ok]...done")

g.clear_screen()
results.append(f"Benchmark runs at resolution: {g.screen.width}x{g.screen.height}")
results.append(f"Resources loading time: {round(load_stop - load_start, 2)} secondes.")
results.append(f"Game engine loading time: {round(g_stop - g_start,2)} secondes.")
results.append(
    f"Test board loading/generation time: {round(gen_stop - gen_start,2)} secondes."
)

g.player.pos = [10, 10]

k = None
go = True

with g.terminal.cbreak(), g.terminal.hidden_cursor(), g.terminal.fullscreen():
    # Here it would be faster to use the clear screen trick, but we need to compare
    # what's comparable.
    spr_start = time.time()
    for row in range(0, g.terminal.height):
        for col in range(0, g.terminal.width):
            g.screen.display_at(
                core.Sprixel(" ", core.Color(33, 99, 247)),
                row,
                col,
            )
    g.screen.display_sprite_at(
        sprites["pgl-benchmark"],
        int(g.terminal.height / 2) - 14,
        int(g.terminal.width / 2 - sprites["pgl-benchmark"].width / 2),
    )
    g.start()
    # On my test computer the screen turn back black and I don't know why
    spr_stop = time.time()
    results.append(
        f"Sprite (place, render and update screen), size "
        f"({sprites['pgl-benchmark'].width}x"
        f"{sprites['pgl-benchmark'].height}): {round(spr_stop-spr_start, 2)*1000}"
        f" msec. or {round(1/(spr_stop-spr_start))} FPS."
    )
    spr_start = time.time()
    for i in range(0, 200):
        g.screen.display_sprite_at(
            sprites["pgl-benchmark"],
            int(g.terminal.height / 2) - 14,
            int(g.terminal.width / 2 - sprites["pgl-benchmark"].width / 2),
        )
        time.sleep(0.01)
    spr_stop = time.time()
    baseline_fps = round(200 / (spr_stop - spr_start))
    results.append(
        f"Sprite 200 updates in: {round(spr_stop-spr_start, 2)*1000}"
        f" msec. or {baseline_fps} FPS."
    )
    g.clear_screen()
    # **BENCHMARK**
    dt = 0.02
    frame_count = 0
    start = time.time()
    phase2 = 0

    # # g.start()
    max_fps = 0
    max_frames = 480
    max_frames = 1000
    panda_steps = int(max_frames / (37 - panda.width))
    last_col = 0
    fps_history = []
    bench_status = base.Text(
        "One board, multiple sprites, NPC movement computed",
        core.Color(0, 128, 255),
        style=constants.BOLD,
    )
    text_phase = base.Text("Phase 1", core.Color(255, 128, 0))
    offset = g.current_board().width * 2 + 7
    panda.row = round((2 + g.current_board().height) - panda.height - 1)
    panda.column = offset
    while frame_count < max_frames:
        print(g.screen.terminal.home, end="")
        g.screen.display_line(
            f"Game benchmark - console resolution: {g.terminal.width}x"
            f"{g.terminal.height}"
        )
        g.screen.display_line("Frame count: 0")
        g.display_board()
        g.screen.display_line("  ")
        if frame_count > int(max_frames / 2):
            polus_map.display_around(
                polus_cam,
                polus_map.partial_display_viewport[0],
                polus_map.partial_display_viewport[1],
            )
        draw_box(
            g,
            2,
            g.current_board().width * 2 + 5,
            g.current_board().height,
            46,
            "Benchmarks",
        )
        bm_box_offset = 35
        draw_box(
            g,
            bm_box_offset,
            polus_map.partial_display_viewport[1] * 2 + 2,
            polus_map.partial_display_viewport[0] * 2,
            g.screen.width - polus_map.partial_display_viewport[1] * 2 - 2,
            "More info",
        )
        g.screen.display_at(
            "Currently running benchmark:",
            bm_box_offset + 3,
            polus_map.partial_display_viewport[1] * 2 + 3,
        )
        g.screen.display_at(
            text_phase,
            bm_box_offset + 3,
            polus_map.partial_display_viewport[1] * 2 + 33,
        )
        g.screen.display_at(
            bench_status,
            bm_box_offset + 4,
            polus_map.partial_display_viewport[1] * 2 + 5,
        )
        g.screen.display_at(
            f"Baseline FPS (calc. in splashscreen): {baseline_fps}",
            bm_box_offset + 6,
            polus_map.partial_display_viewport[1] * 2 + 3,
        )
        g.screen.display_at(
            "Remaining frames to render:",
            bm_box_offset + 8,
            polus_map.partial_display_viewport[1] * 2 + 3,
        )
        bench_rem_frames = base.Text(
            str(max_frames - frame_count), core.Color(0, 255, 128)
        )
        g.screen.display_at(
            bench_rem_frames,
            bm_box_offset + 8,
            polus_map.partial_display_viewport[1] * 2 + 31,
        )
        g.screen.display_at("Progress: ", 5, offset)
        g.screen.display_at("FPS/Max. FPS: |", 6, offset)
        g.screen.display_at(core.Sprixel("|"), 6, offset + 35)
        g.screen.display_at(
            base.Text("FPS graph:", style=constants.BOLD + constants.UNDERLINE),
            7,
            offset,
        )
        low_graph_row = round((2 + g.current_board().height) - panda.height - 2)
        current_fps = round(frame_count / ((time.time() - start) - dt * frame_count))
        if current_fps > max_fps:
            max_fps = current_fps
            if max_fps > baseline_fps:
                baseline_fps = max_fps
            g.screen.display_at(
                core.Sprixel("|", None, core.Color(0, 0, 255)),
                6,
                offset + 15 + int(max_fps * 20 / (baseline_fps + 10)),
            )

        for i in range(
            offset + 15, offset + 16 + int(max_fps * 20 / (baseline_fps + 10))
        ):
            g.screen.display_at(" ", 6, i)
        for i in range(
            offset + 15, offset + 15 + int(current_fps * 20 / (baseline_fps + 10))
        ):
            g.screen.display_at(
                core.Sprixel(" ", core.Color(0, 0, 255)),
                6,
                i,
            )
        fps_str = f"FPS: {current_fps}"
        g.screen.display_at(f"Frame count: {frame_count}", 1, 0)
        g.screen.display_at(fps_str, 1, 20)
        g.screen.display_at(fps_str, 3, offset)
        g.screen.display_at(f"Frame #{frame_count}", 3, offset + 20)
        g.screen.display_at(f"Maximum FPS: {max_fps}", 4, offset)
        for i in range(0, int((frame_count * 32) / max_frames)):
            g.screen.display_at(core.Sprixel.green_rect(), 5, offset + 10 + i)
        current_col = offset + int((frame_count * 38) / max_frames)
        if current_col > last_col:
            fps_history.append(current_fps)
            last_col = current_col
        for c in range(offset, current_col + 1):
            g.screen.display_at(
                core.Sprixel(" ", core.Color(0, 0, 255)),
                low_graph_row,
                c,
            )
            for i in range(
                low_graph_row
                - int(
                    fps_history[c - offset] * (low_graph_row - 8) / (baseline_fps + 10)
                ),
                low_graph_row,
            ):
                g.screen.display_at(
                    core.Sprixel(" ", core.Color(0, 0, 255)),
                    i,
                    c,
                )

        if frame_count == int(max_frames / 2):
            stop = time.time()
            results.append(
                f"Benchmark (direct display - phase 1):\n\tdt={dt}\n\tframes "
                f"rendered={frame_count} in "
                f"{round(stop - start, 5)} sec. or {round((stop-start)/frame_count, 5)}"
                f" sec. per frame\n\tActual rendering time per frame: "
                f"{round(((stop-start)/frame_count - dt)*1000, 2)} "
                f"msec.\n\tFPS: {round(1/((stop-start)/frame_count - dt))}"
            )
            #     g.screen.place(polus_map, 2, 0)
            phase2 = time.time()
            bench_status.text = "Phase 1 + high definition board + camera movement"
        g.screen.display_sprite_at(panda, panda.row, panda.column + 1)
        if frame_count % panda_steps == 0:
            #     g.screen.delete(panda.row, panda.column)
            panda.column += 1
        if frame_count > max_frames / 2:
            text_phase.text = "Phase 2"
            if (
                polus_cam.column
                < polus_map.width - polus_map.partial_display_viewport[1]
            ):
                polus_cam.column += 2
            else:
                polus_cam.row += 1
        g.actuate_npcs(1)
        g.terminal.inkey(timeout=dt)
        frame_count += 1
    stop = time.time()
    results.append(
        f"Benchmark (direct display - phase 2):\n\tdt={dt}\n\tframes rendered="
        f"{frame_count-int(max_frames/2)}"
        f" in {stop - phase2} sec. or {(stop-phase2)/(frame_count-int(max_frames/2))}"
        f" sec. per frame\n\t"
        f"Actual rendering time per frame: "
        f"{round(((stop-phase2)/(frame_count-int(max_frames/2)) - dt)*1000,2)} "
        f"msec.\n\tFPS: {round(1/((stop-phase2)/(frame_count-int(max_frames/2)) - dt))}"
    )
    results.append(
        f"Benchmark (direct display - overall):\n\tdt={dt}\n\tframes rendered="
        f"{frame_count}"
        f" in {stop - start} sec. or {(stop-start)/frame_count} sec. per frame\n\t"
        f"Actual rendering time per frame: "
        f"{round(((stop-start)/frame_count - dt)*1000,2)} "
        f"msec.\n\tFPS: {round(1/((stop-start)/frame_count - dt))}"
    )

print("\n=========== Direct Display Benchmark results ===========")
for r in results:
    print(r)
