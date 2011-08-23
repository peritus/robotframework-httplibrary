robotframework-httplibrary
--------------------------

**robotframework-httplibrary** is a `Robot Framework
<http://code.google.com/p/robotframework/>`_ test library for all your HTTP
needs. It uses `livetest <http://pypi.python.org/pypi/livetest>`_ (which, in
turn uses the famous `webtest <http://webtest.pythonpaste.org/>`_ library
underneath.)

Installation
------------

**Note**: Due to a problem in livetest's package metadata (reported here:
(`https://github.com/storborg/livetest/pull/6
<https://github.com/storborg/livetest/pull/6>`_) you need to install webtest
first:

``pip install webtest``

Then, install robotframework-httplibrary

``pip install --upgrade robotframework-httplibrary``

Usage
-----
API documentation can be found at
`http://peritus.github.com/robotframework-httplibrary/
<http://peritus.github.com/robotframework-httplibrary/>`_, here is an example
on how to use it:

============  ================
  Setting          Value      
============  ================
Library       HttpLibrary.HTTP
============  ================

\

============  =================================  ===================================
 Test Case    Action                             Argument
============  =================================  ===================================
Example       [Documentation]                    Follows A Redirect
\             Connect                            `httpstat.us <http://httpstat.us>`_
\             GET                                /302
\             Follow Response
\             Response Status Code Should Equal  200
============  =================================  ===================================

Compatibility
-------------
This library is only tested on CPython. It might work on Jython, not sure.

Development
-----------
If you want to hack on this library itself, this should get you started::

  # bootstrap development environment
  git clone https://github.com/peritus/robotframework-httplibrary.git
  cd robotframework-httplibrary/
  python bootstrap.py
  ./bin/buildout
  
  # run tests
  ./bin/robotframework tests/

I'm very happy about patches, pull-requests and API-discussions (as this is
mostly a wrapper supposed to have a nice API)!

License
-------
`Beerware <http://en.wikipedia.org/wiki/Beerware>`_: If we meet some day, and
you think this stuff is worth it (or need a more serious license), you can buy
me a beer in return.

