#!/usr/bin/env python

from distutils.core import setup

CLASSIFIERS = """
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

setup(
  name             = 'robotframework-httplibrary',
  version          = "0.0.1",
  description      = 'Robot Framework wrapper for livetest',
  long_description = "Robot Framework wrapper for livetest",
  author           = 'Filip Noetzel',
  author_email     = 'filip+rfhttplibrary@j03.de',
  url              = 'http://code.google.com/p/robotframework-seleniumlibrary',
  license          = 'Beerware',
  keywords         = 'robotframework testing testautomation web http livetest webtest',
  platforms        = 'any',
  classifiers      = CLASSIFIERS.splitlines(),
  package_dir      = {'' : 'src'},
  install_requires = ['robotframework', 'livetest'],
  packages         = ['HttpLibrary']
)
