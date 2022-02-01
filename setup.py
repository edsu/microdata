from setuptools import setup

setup(
    name = 'microdata',
    version = '0.8.0',
    description = "html5lib extension for parsing microdata",
    author = "Ed Summers",
    author_email = "ehs@pobox.com",
    url = "http://github.com/edsu/microdata",
    python_requires=">=3.3",
    py_modules = ['microdata'],
    test_suite = 'test',
    install_requires = ['html5lib>=0.999999999'],
    entry_points = {
        "console_scripts": [
            "microdata = microdata:main"
        ]
    }
)
