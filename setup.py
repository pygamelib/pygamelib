import setuptools
import gamelib.Constants as Constants

try:
    from pipenv.project import Project
    from pipenv.utils import convert_deps_to_pip
except ImportError:
    print("Please install pipenv first. See: https://github.com/pypa/pipenv")

with open("README.md", "r") as fh:
    long_description = fh.read()

# Compatibility layer between Pipenv and Pip requirements.txt
# See https://github.com/pypa/pipenv/issues/209
pipfile = Project(chdir=False).parsed_pipfile
requirements_path = convert_deps_to_pip(pipfile['packages'])

INSTALL_PACKAGES = open(requirements_path).read().splitlines()

setuptools.setup(
    name="hac-game-lib",
    version=Constants.HAC_GAME_LIB_VERSION,
    author="Arnaud Dupuis",
    author_email="hyrule.astronomy.club@gmail.com",
    description="A small game development framework for teaching \
        programming to young kids.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=INSTALL_PACKAGES,
    url="https://astro.hyrul.es",
    packages=setuptools.find_packages(),
    scripts=['hgl-base_game.py', 'hgl-editor.py', 'hgl-board-tester.py'],
    keywords=['game', 'development', 'beginner'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Documentation': 'https://hac-game-lib.readthedocs.io/en/latest/index.html',  # noqa: E501
        'Guides & Tutorials': 'https://astro.hyrul.es/guides/hac-game-lib/',
        'Source': 'https://github.com/arnauddupuis/hac-game-lib',
        'Tracker': 'https://github.com/arnauddupuis/hac-game-lib/issues',
        'Release Notes': 'https://astro.hyrul.es/news/hac-game-lib-v1.0.0-release-notes.html'
    },
    python_requires='>=3',
)
