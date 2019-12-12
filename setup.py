#!/usr/bin/env python

from distutils.core import setup

CLASSIFIERS = """
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

from os.path import join, dirname
long_description = open(join(dirname(__file__), 'README.rst',)).read()

setup(
    name='robotframework-httplibrary',
    version="0.4.7",
    description='Robot Framework keywords for HTTP requests',
    long_description=long_description,
    author='Vadym Vikulin',
    author_email='vadym.vikulin@gmail.com',
    url='https://github.com/vikulin/robotframework-httplibrary',
    license='Beerware',
    keywords='robotframework testing test automation web http webtest',
    platforms='any',
    zip_safe=False,
    classifiers=CLASSIFIERS.splitlines(),
    package_dir={'': 'src'},
    install_requires=['robotframework', 'webtest>=2.0', 'jsonpatch', 'jsonpointer'],
    packages=['HttpLibrary']
)
