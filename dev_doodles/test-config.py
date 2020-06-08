from gamelib.Game import Game


g = Game()
c = g.load_config("test-config.json", "test")

print(f"Version: {g.config('test')['config_file_version']}")
g.config("test")["directories"].append("test_boards")
g.save_config("test", "config-test.json")
print(g.config("blorp"))
