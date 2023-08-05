""" Package information of docstrings based argparse.
"""
from setuptools import setup
import dsargparse

setup(
    name="dsargparse",
    version="0.3.1",
    author="Junpei Kawamoto",
    author_email="kawamoto.junpei@gmail.com",
    description=dsargparse.__doc__,
    py_modules=["dsargparse"],
    test_suite="tests.suite",
    license="MIT",
    keywords="cli helper argparse",
    url="https://github.com/jkawamoto/dsargparse",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Utilities"
    ]
)
