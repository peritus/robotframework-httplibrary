
.. image:: https://secure.travis-ci.org/peritus/robotframework-httplibrary.png?branch=master
  :target: http://travis-ci.org/peritus/robotframework-httplibrary

robotframework-httplibrary
--------------------------

**robotframework-httplibrary** is a `Robot Framework
<http://code.google.com/p/robotframework/>`_ test library for all your HTTP
needs. It uses `livetest <http://pypi.python.org/pypi/livetest>`_ (which, in
turn uses the famous `webtest <http://webtest.pythonpaste.org/>`_ library
underneath).

Installation
------------

You can install robotframework-httplibrary via `pip
<http://www.pip-installer.org/>`_::

  pip install --upgrade robotframework-httplibrary

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
Example
\             [Documentation]                    Follows a Redirect
\             Create HTTP Context                `httpstat.us <http://httpstat.us>`_
\             GET                                /302
\             Response Status Code Should Equal  302
\             Follow Response
\             Response Body Should Contain       generating different HTTP codes
============  =================================  ===================================

You can view a `report <http://peritus.github.com/robotframework-httplibrary/report.html>`_ and a `log <http://peritus.github.com/robotframework-httplibrary/log.html>`_ of this test executed that looks like this:

.. image:: http://peritus.github.com/robotframework-httplibrary/rfhttplib_example_test_execution.png
  :target: http://peritus.github.com/robotframework-httplibrary/log.html

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

Changelog
---------

**v0.4.2**

- Don't enforce ASCII when converting to JSON (so chinese characters are
  printed as such and not escaped like \uXXXX). Thanks Terry Yin!

**v0.4.1**

- Tested with Robot Framework 2.8rc1
- Uses jsonpointer 1.0, jsonpatch 1.0

**v0.4.0**

- Compatible with Webtest > 2.0
- hard-deprecate 'Set HTTP Host', will be removed soon.

**v0.3.4**

- Add support for python-json-pointer >= 0.6 (if you experienced
  "``AttributeError: 'module' object has no attribute 'set_pointer'``", you
  should upgrade to this version).

**v0.3.3**

- add HTTPS support
- add 'Stringify JSON' keyword
- implicitly set correct 'Host' header

License
-------
`Beerware <http://en.wikipedia.org/wiki/Beerware>`_: If we meet some day, and
you think this stuff is worth it (or need a more serious license), you can buy
me a beer in return.

