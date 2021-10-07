
__author__ = "B. Marchand, L. Lacourt"
__version__ = "0.1"
contact = "basile.marchand@gmail.com"
name = "pymas"

import pathlib as pl 
from setuptools import setup, find_packages

with pl.Path("README.md").open("r") as fid:
    long_description = fid.read()

setup(
    name=name,
    version=__version__,
    author_email=contact,
    description="PYthon MAil Sender",
    long_description=long_description,
    license="",
    url="",
    classifiers=[
        'Development Status :: 1 - Beta',
    ],
    install_requires=["pyyaml"],
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['pymas=pymas:entry_point'],
    }
)