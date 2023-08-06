=============================
 Contributing To The Project
=============================
The best way to contribute changes to IMAPClient is to fork the
official repository on Github, make changes in a branch in your
personal fork and then submit a pull request.

Discussion on the mailing list before undertaking development is
highly encouraged for potentially major changes.

Although not essential, it will make the project maintainer a much
happier person if change submissions include appropriate updates to
unit tests and the live tests. Please ask if you're unsure how of how
the tests work.

Please read on if you plan on submitting changes to IMAPClient.

=============
 Source Code
=============
The official source code repository for IMAPClient can be found on
Github at: https://github.com/mjs/imapclient/

Any major feature work will also be found as branches of this
repository.

Branches
========
Development for the next major release happens on the ``master`` branch.

There is also a branch for each major release series (for example:
``1.x``). When appropriate and when there will be future releases for
a series, changes may be selectively merged between ``master`` and a
stable release branch.

Release Tags
============
Each released version is available in the IMAPClient repository
as a Git tag (e.g. "0.9.1").

============
 Unit Tests
============
There are comprehensive unit tests for the server response parser and
a number of other parts of the code. These tests use the unittest2
package which is also included as the standard unittest package in
Python 2.7 and 3.2 onwards.

Running Unit Tests
==================
To run the tests run::

     python setup.py test

from the root of the package source. This will install the Mock
package (locally) if it isn't already installed as it is required for
many of the tests.

Where unittest2 is included in the standard library (eg. Python 2.7
and 3.2+) you can also run all unit tests like this (from the root
directory of the IMAPClient source)::

     python -m unittest discover

Alternatively, if unittest2 is installed separately use the unit2
script (for Unix-like systems) or the unit2.py script::

     unit2 discover
     unit2.py discover

Running the Unit Tests Against Multiple Python Versions
=======================================================
It is possible to run the unit tests against all supported Python
versions at once using `tox`_. Once installed, the ``tox`` command
will use the tox.ini file in the root of the source directory and run
the unit tests against the Python versions officially supported by
IMAPClient (provided these versions of Python are installed!).

.. _`tox`: http://testrun.org/tox/

Writing Unit Tests
==================
Protocol level unit tests should not act against a real IMAP server
but should use canned data instead. The IMAPClientTest base class
should typically be used as the base class for any tests - it provides
a mock IMAPClient instance at `self.client`. See the tests in
imapclient/tests/test_imapclient.py for examples of how to write unit
tests using this approach.
