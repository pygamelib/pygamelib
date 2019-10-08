import setuptools
import gamelib.Constants as Constants

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hac-game-lib",
    version=Constants.HAC_GAME_LIB_VERSION,
    author="Arnaud Dupuis",
    author_email="hyrule.astronomy.club@gmail.com",
    description="A small game development framework for teaching programming to young kids.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'colorama >= 0.3.8'
    ],
    url="https://astro.hyrul.es",
    packages=setuptools.find_packages(),
    scripts=['hgl-base_game.py','hgl-editor.py','hgl-board-tester.py'],
    keywords=['game','development','beginner'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Documentation': 'https://hac-game-lib.readthedocs.io/en/latest/index.html',
        'Guides & Tutorials': 'https://astro.hyrul.es/guides/hac-game-lib/',
        'Source': 'https://github.com/arnauddupuis/hac-game-lib',
        'Tracker': 'https://github.com/arnauddupuis/hac-game-lib/issues',
        'Release Notes' : 'https://astro.hyrul.es/release-notes/2019.4a1/'
    },
    python_requires='>=3',
)