from setuptools import setup
import sys

extra = {}

setup(
    name = 'microdata',
    version = '0.7.2',
    description = "html5lib extension for parsing microdata",
    author = "Ed Summers",
    author_email = "ehs@pobox.com",
    url = "http://github.com/edsu/microdata",
    py_modules = ['microdata'],
    scripts = ['microdata.py'],
    test_suite = 'test',
    install_requires = ['html5lib>=0.999999999'],
    **extra
)
