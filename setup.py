import setuptools
import pygamelib.constants as constants

try:
    from pipenv.project import Project
    from pipenv.utils.dependencies import convert_deps_to_pip
except ImportError:
    print("Please install pipenv first. See: https://github.com/pypa/pipenv")

with open("README.md", "r") as fh:
    long_description = fh.read()

# Compatibility layer between Pipenv and Pip requirements.txt
# See https://github.com/pypa/pipenv/issues/209
pipfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pipfile["packages"])

INSTALL_PACKAGES = list(requirements.values())


setuptools.setup(
    name="pygamelib",
    version=constants.PYGAMELIB_VERSION,
    author="Arnaud Dupuis",
    author_email="8bitscoding@gmail.com",
    description="A (not so) small library for terminal based game development.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=INSTALL_PACKAGES,
    url="https://www.pygamelib.org",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=["pgl-editor.py", "pgl-board-tester.py", "pgl-sprite-editor.py"],
    keywords=["game", "development", "beginner", "console", "terminal"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Terminals",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Documentation": "https://pygamelib.readthedocs.io/en/latest/index.html",  # noqa: E501
        "Source": "https://github.com/pygamelib/pygamelib",
        "Tracker": "https://github.com/pygamelib/pygamelib/issues",
        "Wiki": "https://github.com/pygamelib/pygamelib/wiki",
        "Tech blog": "https://8bitscoding.io/",
        # "Release Notes": "https://8bitscoding.io/2020/08/30/pygamelib-v1-2-0-release-notes/",  # noqa: E501
    },
    python_requires=">=3.6",
)
