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
    url="https://astro.hyrul.es",
    packages=setuptools.find_packages(),
    keywords='game development beginner',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Documentation': 'https://hac-game-lib.readthedocs.io/en/latest/index.html',
        'Source': 'https://github.com/arnauddupuis/hac-game-lib',
        'Tracker': 'https://github.com/arnauddupuis/hac-game-lib/issues',
        'Release Notes' : 'https://astro.hyrul.es/release-notes/2019.4a1/'
    },
    python_requires='>=3',
)