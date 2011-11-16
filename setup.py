#!/usr/bin/env python

from distutils.core import setup

CLASSIFIERS = """
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

setup(
  name             = 'robotframework-httplibrary',
  version          = "0.1.1",
  description      = 'Robot Framework wrapper for livetest',
  long_description = "Robot Framework wrapper for livetest",
  author           = 'Filip Noetzel',
  author_email     = 'filip+rfhttplibrary@j03.de',
  url              = 'https://github.com/peritus/robotframework-httplibrary',
  license          = 'Beerware',
  keywords         = 'robotframework testing testautomation web http livetest webtest',
  platforms        = 'any',
  zip_safe         = False,
  classifiers      = CLASSIFIERS.splitlines(),
  package_dir      = {'' : 'src'},
  install_requires = ['robotframework', 'livetest', 'jsonpointer'],
  packages         = ['HttpLibrary']
)
