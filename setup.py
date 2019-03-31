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
    url="https://github.com/arnauddupuis/hac-game-lib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)