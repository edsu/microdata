from setuptools import setup
import sys

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(
    name = 'microdata',
    version = '0.7.0',
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
