#!/usr/bin/env python
import os

from setuptools import setup, find_packages

HERE = os.path.dirname(__file__)

setup(
    name="sneakers",
    version="0.0.1",
    description="Ruby shoes flavored tkinter.",
    author="James Draper",
    author_email="james.draper@duke.edu",
    license="MIT",
    url="https://github.com/draperjames/sneakers",
    packages=find_packages(),
    platforms=["POSIX", "Windows"],
    provides=["sneakers"],
    keywords="gui, shoes, tkinter",
    long_description=open(os.path.join(HERE, "README.md"), "r").read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Systems Administration",
    ],
)
