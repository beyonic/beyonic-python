import os
from setuptools import setup
import os.path
import beyonic


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


VERSION = beyonic.__version__

from os import path
from io import open
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="beyonic",
    version=VERSION,
    description="The official Python client for the Beyonic.com API",
    author="Beyonic",
    author_email="info@beyonic.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["beyonic", "beyonic.apis"],
    install_requires=["requests"],
    license="MIT",
    keywords=["api", "mobile payments", "mobile money", "beyonic", "mpesa"],
    url="https://beyonic.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
