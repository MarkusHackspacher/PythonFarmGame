from setuptools import find_packages, setup

setup(
    name="Python Farm Game",
    version="0.6",
    description="Python farm game ",
    author="orneo1212",
    author_email="orneo1212@gmail.com",
    packages=["farmlib", "pygameui"],  # same as name
    entry_points={
        "console_scripts": [
            "main=farmlib.main:main",
        ],
    },
    test_suite='tests',
)
