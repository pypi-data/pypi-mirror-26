"""Setup module for orderPy.
See: https://github.com/johannesber/orderPy"""

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="orderPy",
    version="0.1a3",
    description="A python script for windows that will order a disordered set of files by their date of creation or last modification.",
    long_description = long_description,
    url = "https://github.com/johannesber/orderPy",
    author = "Johannes Berger",
    author_email = "johannes.berger1709@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    keywords = "sorting data",
    py_modules = ["orderPy"],
    install_requires = ["Unipath"],
    python_requires = ">3.6",
    scripts = ["orderPy.py"],
    entry_points = {
        "console_scripts":[
            "orderPy = orderPy:main"
        ],
    },
 

)