![Tested OS: Linux](https://img.shields.io/badge/Tested%20OS-Linux-green.svg "Tested OS: Linux")
![Untested OS: Windows, Mac OS](https://img.shields.io/badge/Untested%20OS-Windows,Mac%20OS-important.svg "Untested OS: Windows, Mac OS")
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)


# hac-game-lib
Hyrule Astronomy Club - Kids coding class - base library for a game development

## Introduction

This library is used as a base to teach coding to kids from 6 to 12.
It aims at giving an envireonment to kids that let them focus on the algorithm instead of the lousy display or precise management.

This is **obviously** extremely simple and does not aim at being anythting serious for game developpers.

If this library is useful for other teachers, I'll make tutorials.

![base_game.py screenshot](images/base_game_lvl1.jpg?raw=true "base_game.py")

## Requirements

Run PIP to install the requirements (only colorama):

```bash
pip3 install -r requirements.txt
```

## Limitations

There is tons of limitations but for the most important ones: 
* Only one player is supported.
* There is little protections against messing up with the internal. This is *on purpose*, I want the kids to learn to use the API not mess up with the internals of every single class.
