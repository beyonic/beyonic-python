'''
Copyright (c) 2014 Nikhil Navadiya

MIT License

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


import os

from setuptools import setup

VERSION = "1.0"

def readme():
    """ Load the contents of the README file """
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_path, "r") as f:
        return f.read()

setup(
    name="beyonic",
    version=VERSION,
    description="The official Python client for Beyonic's API",
    author="Nikhil Navadiya, Luke Kyohere",
    author_email="nikhil.navadiya@gmail.com, luke@beyonic.com",
    long_description=readme(),
    packages=["beyonic", "beyonic.apis"],
    install_requires=["requests"],
    license="Apache",
    url="https://github.com/beyonic/beyonic-python",
    classifiers=[
        "Development Status :: 1 - Alpha",
        "License :: OSI Approved :: Apache Software License",
    ],
)