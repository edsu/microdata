from setuptools import setup

setup(
    name = 'microdata',
    version = '0.1',
    description = "html5lib extension for parsing microdata",
    author = "Ed Summers",
    author_email = "ehs@pobox.com",
    url = "http://github.com/edsu/microdata",
    py_modules = ['microdata'],
    test_suite = 'test',
    install_requires = ['html5lib'],
)
