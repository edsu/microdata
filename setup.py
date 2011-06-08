from setuptools import setup

setup(
    name = 'html5lib-microdata',
    version = '0.1',
    description = "html5lib extension for parsing microdata",
    author = "Ed Summers",
    author_email = "ehs@pobox.com",
    url = "http://github.com/edsu/html5lib-microdata",
    py_modules = ['html5lib_microdata'],
    test_suite = 'test',
    install_requires = ['html5lib'],
)
