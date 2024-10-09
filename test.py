from pygamelib.gfx.ui import GridSelectorDialog, GridSelector, UiConfig
from pygamelib import engine


class Observer:
    def __init__(self):
        pass

    def handle_notification(self, attribute, value):
        print(attribute, value)


game = engine.Game.instance()
game.screen = engine.Screen(50, 50)


grid = GridSelectorDialog(
    ["a", "b", "1", "2", "4", "alph"],
    minimum_height=20,
    maximum_height=2,
    minimum_width=20,
    maximum_width=2,
)
grid_selector: GridSelector = grid.grid_selector


grid_selector.maximum_width = 3
grid_selector.maximum_height = 3
grid_selector.page_down()
print(grid_selector.current_page)
grid_selector.page_up()
print(grid_selector.current_page)

conf = UiConfig.instance(game=game)
gd = GridSelectorDialog(
    [
        "a",
        "b",
        "c",
        "##",
    ],
    maximum_height=3,
    maximum_width=3,
    title="test",
    config=conf,
)
gd.grid_selector.page_down()
assert gd.grid_selector.current_page == 1
gd.grid_selector.page_up()
assert gd.grid_selector.current_page == 0

grid_selector.attach(Observer)
grid_selector.width = "10"


screen = engine.Screen()

screen.place(gd, 1, 1)
screen.update()

gd.grid_selector.cursor_right()
screen.clear()
