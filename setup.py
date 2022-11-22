<<<<<<< HEAD
from setuptools import find_packages, setup

setup(
    name="Python Farm Game",
    version="0.6",
=======
from setuptools import setup

setup(
    name="Python Farm Game",
    version="0.5.2",
>>>>>>> 7eee31badfa52bf7eaad2d00ab227a27f9852364
    description="Python farm game ",
    author="orneo1212",
    author_email="orneo1212@gmail.com",
    packages=["farmlib", "pygameui"],  # same as name
    entry_points={
        "console_scripts": [
            "main=farmlib.main:main",
        ],
    },
<<<<<<< HEAD
    test_suite='tests',
=======
>>>>>>> 7eee31badfa52bf7eaad2d00ab227a27f9852364
)
