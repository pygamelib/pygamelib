# SUPAREX

![screenshot](https://raw.githubusercontent.com/arnauddupuis/hac-game-lib/master/images/suparex-title-screen.png "suparex")

## Pitch

Suparex is an infinite procedurally generated levels platform game.

This means that I was too lazy to code an end and I just put a bit of code into the game that generates levels as long as you don't die.

You can move with direction keys (arrows), jump with space and sprout trees in any direction with the z/q/s/d or w/a/s/d keys.

Your goal is to beat some famous women scientist to the hall of fame. Your main resource is time.

Good luck!

## Installation

Don't install, run it from here...

You need to install simpleaudio to benefit from the annoying 8-bit sounds! All sounds are generated with [SFXR Qt](https://github.com/agateau/sfxr-qt).

To install it you can do one of these:

```bash
pip3 install simpleaudio
```

or 

```bash
pipenv install
```

There is a Pipfile for your convenience.

## Future

Here is a list of ideas I have (no promise on delivery):
 * Package it on pypi.
 * Add background music.
 * Add more traps and why not enemies.
 * Add more variety in the level generation (colors, density of traps, verticality, etc.).
 * Set a hotkey/option to record the level generation process (very easy actually).
 * Add an online leaderboard (with anti-cheat measures...).