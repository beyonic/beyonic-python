import os
from setuptools import setup
import os.path
import beyonic


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


if os.path.exists('README.md'):
    import shutil
    shutil.copyfile('README.md', 'README.txt')

VERSION = beyonic.__version__

setup(
    name="beyonic",
    version=VERSION,
    description="The official Python client for the Beyonic.com API",
    author="Beyonic",
    author_email="info@beyonic.com",
    long_description=read('README.txt'),
    packages=["beyonic", "beyonic.apis"],
    install_requires=["requests"],
    license="MIT",
    keywords=["api", "mobile payments", "mobile money", "beyonic", "mpesa"],
    url="http://beyonic.com",
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
