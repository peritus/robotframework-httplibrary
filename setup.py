#!/usr/bin/env python

from distutils.core import setup

CLASSIFIERS = """
Programming Language :: Python
Programming Language :: Python 2.7
Programming Language :: Python 3.6
Topic :: Software Development :: Testing
"""[1:-1]

from os.path import join, dirname
long_description = open(join(dirname(__file__), 'README.rst',)).read()

setup(
    name='robotframework-httplibrary',
    version="1.0.2",
    description='Robot Framework keywords for HTTP requests',
    long_description=long_description,
    author='Filip Noetzel',
    author_email='filip+rfhttplibrary@j03.de',
    url='https://github.com/peritus/robotframework-httplibrary',
    license='Beerware',
    keywords='robotframework testing testautomation web http webtest',
    platforms='any',
    zip_safe=False,
    classifiers=CLASSIFIERS.splitlines(),
    package_dir={'': 'src'},
    install_requires=['robotframework', 'webtest>=2.0', 'jsonpatch',
                      'jsonpointer'],
    packages=['HttpLibrary']
)
