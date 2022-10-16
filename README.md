![Linux: Ok](https://img.shields.io/badge/Linux-Ok-green.svg "Linux: Ok")
![Windows: Ok](https://img.shields.io/badge/Windows-Ok-green.svg "Windows: Ok")
![Mac OS: Ok](https://img.shields.io/badge/Mac%20OS-Ok-green.svg "Mac OS: Ok")
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.txt)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Documentation Status](https://readthedocs.org/projects/pygamelib/badge/?version=latest)](https://pygamelib.readthedocs.io/en/latest/?badge=latest)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/2849/badge)](https://bestpractices.coreinfrastructure.org/projects/2849)
[![CircleCI](https://circleci.com/gh/arnauddupuis/pygamelib.svg?style=svg)](https://circleci.com/gh/arnauddupuis/pygamelib)
[![codecov](https://codecov.io/gh/arnauddupuis/pygamelib/branch/master/graph/badge.svg)](https://codecov.io/gh/arnauddupuis/pygamelib)

<p align="center">
  <img src="https://raw.githubusercontent.com/pygamelib/pygamelib/master/images/pygamelib-logo.png">
</p>

# pygamelib
A (not so) small library for terminal based game development.

## Preemptive warning

Version updates always bare the possibility of bringing some breaking changes together with new features and improvements. We try to limit these but when they do occur they are documented [on the wiki]([/wiki#migration-notes](https://github.com/pygamelib/pygamelib/wiki#migration-notes)).

## Introduction

Historically, this library is used as a base to teach coding to kids from 6 to 15.
It aims at giving an environment to new and learning developers (including kids) that let them focus on the algorithm instead of the lousy display or precise management.

It started as a very simple library with very little capabilities, but over time it became something more. To the point that it is now possible to make very decent games with it.
So this is **obviously** still extremely simple compared to other game framework and it still does not aim at being anything serious for real game developers.
However, it can now be used by aspiring game developers for an introduction to 2D games development.

There is a [Youtube channel](https://www.youtube.com/channel/UCT_SxIlKaD6MM7JlQKelpgw) that (will) contains tutorials.

Here is a quick view of what can currently be achieved with that library:

[![Watch the video](https://img.youtube.com/vi/9l18dhJ-kJE/hqdefault.jpg)](https://youtu.be/9l18dhJ-kJE)

Have a look at the [examples/](examples/suparex/) directory to see how most of these games have been done!

If you want a quick peak at the new features in the most recent version, have a look at this:

[![Watch the video](https://img.youtube.com/vi/AyzSMH5msU4/hqdefault.jpg)](https://youtu.be/AyzSMH5msU4)

## Strong points

Hopefully you'll find the pygamelib to have a lot of strong points:
 * It is **simple**. It requires very limited Python knowledge to start coding games.
 * Yet **powerful** offering more advanced programmers a *lot* of possibilities.
 * The possibilities **scale up with the students** offering basic feature and default values "good enough" for beginners and lots of tunning opportunities for the advanced coders.
 * Lots of stuff are available **by default**. Any idea how long it would take a beginner to display only a part of a board? 1 second with the pygamelib, probably slightly more if they had to do it by hand ;)
 * It is **Terminal based**. This means no graphics card dependencies, cross platform, and a framework that stimulate imagination and creativity.

## Installation (recommended)

The easiest way to install a stable version is to use [pypi](https://pypi.org/project/pygamelib/):

```bash
pip3 install pygamelib
```

It will pull all dependencies 

## Installation from sources and requirements

### Python

The pygamelib only supports Python 3.6+. It will **not** run with Python 2.
We use [pipenv](https://github.com/pypa/pipenv) to manage dependencies.

Run Pipenv to install the requirements:

```bash
pip3 install pipenv
pipenv install
```

If you want the development dependencies you need to run:
```bash
pip3 install pipenv
pipenv install --dev
```

Or you can just run ```make devenv``` if make is available on your system.

### Runing tests 

To run the unit tests use the following command:

```bash
python -m unittest discover -s tests
```

### Terminal color and emojis

It is not really a hard requirement but colored emojis are really bringing the games created to life.  
We then recommend to have a color emojis font installed like Noto Color Emojis (on most Linux distributions you can install it from the package manager, search for "noto-color-emoji").

If your terminal application is not displaying color emojis, please have a look at this [file](https://gist.github.com/IgnoredAmbience/7c99b6cf9a8b73c9312a71d1209d9bbb) and follow the instructions.

### Running examples

To run the examples using [pipenv](https://github.com/pypa/pipenv):

```bash
pipenv shell
(pygamelib) cd examples/suparex
(pygamelib) python3 suparex.py
```

## Limitations

There is tons of limitations but for the most important ones: 
* Only one player is supported.
* There is little protections against messing up with the internal. This is *on purpose*, I want the kids to learn to use the API not mess up with the internals of every single class.
* It's pure Python (it's slow).
