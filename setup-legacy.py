import setuptools

with open("README-Legacy.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hac-game-lib",
    version="1.1.99",
    author="Arnaud Dupuis",
    author_email="8bitscoding@gmail.com",
    description="A small game development framework for teaching programming.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires="pygamelib",
    url="https://astro.hyrul.es",
    packages=[],
    scripts=[],
    keywords=["game", "development", "beginner", "console", "terminal"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 7 - Inactive",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Documentation": "https://hac-game-lib.readthedocs.io/en/latest/index.html",  # noqa: E501
        "Guides & Tutorials": "https://astro.hyrul.es/guides/hac-game-lib/",
        "Source": "https://github.com/arnauddupuis/hac-game-lib",
        "Tracker": "https://github.com/arnauddupuis/hac-game-lib/issues",
        "Release Notes": "https://8bitscoding.io/2020/08/30/pygamelib-v1-2-0-release-notes/",  # noqa: E501
    },
    python_requires=">=3.6",
)
