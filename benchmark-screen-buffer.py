from pygamelib import engine, constants, board_items
from pygamelib.gfx import core
import time


def upd(g, k, dt):
    if k == "q":
        g.state = constants.STOPPED
    elif k == "0":
        g.screen.place("+", 0, 0)
    elif k == "1":
        g.screen.place("*", 1, 1)
    elif k == "2":
        g.screen.place("#", 2, 2)
    g.screen.update()


sc = core.SpriteCollection.load_json_file("tests/panda.spr")
g = engine.Game(user_update=upd, mode=constants.MODE_TBT)
g.player = board_items.Player(sprixel=core.Sprixel("@", None, core.Color(0, 255, 255)))
g.add_board(1, engine.Board())
g.change_level(1)
# g.screen.place("+", int(g.screen.width / 2), int(g.screen.height / 2))
for row in range(0, g.screen._display_buffer.shape[0]):
    for col in range(0, g.screen._display_buffer.shape[1]):
        g.screen.place(
            core.Sprixel(" ", core.Color(row * 4, col, int((row + col) / 2))), row, col
        )
# g.screen.place(sc["panda"], 10, 10)
# g.screen.place("This is a text", g.screen.height - 1, 25)
# g.run()
g.screen.place(g.player, 10, 10)
g.player.pos = [10, 10]
k = None
go = True
result = list(f"Benchmark runs at resolution: {g.screen.width}x{g.screen.height}")
with g.terminal.cbreak(), g.terminal.hidden_cursor(), g.terminal.fullscreen():
    for dt in [0.01, 0.02, 0.05]:
        frames = 120
        start = time.time()
        frame_count = 0
        while frame_count != frames and g.state != constants.STOPPED:
            g.screen.place(f"Benchmark: {dt} {frame_count}/{frames}", 0, 0)
            if k == "q":
                g.state = constants.STOPPED

            if g.player.column == g.screen.width - 1:
                go = False
            elif g.player.column == 0:
                go = True
            g.screen.place(core.Sprixel(" "), g.player.row, g.player.column)
            if go:
                g.player.pos[1] += 1
            else:
                g.player.pos[1] -= 1
            g.screen.place(g.player, g.player.row, g.player.column)
            g.screen.update()
            k = g.terminal.inkey(timeout=dt)
            frame_count += 1
        stop = time.time()
        result.append(
            f"Benchmark for dt={dt} frames rendered={frame_count} in {stop - start} sec. or {(stop-start)/frame_count} sec. per frame\nActual rendering time per frame: {(stop-start)/frame_count - dt}"
        )
    for r in result:
        print(r)
    input("Press a key to quit")
