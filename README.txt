rtsprofile
===============================================================================

rtsprofile is a Python library providing an interface to the RT System Profile
specification. This specification describes a complete RT system and can be
used to reconstruct that system at a later time. The library supports both XML
and YAML formatted files.

This software is developed at the National Institute of Advanced Industrial
Science and Technology. Approval number H22PRO-1141. The development was
financially supported by the New Energy and Industrial Technology Development
Organisation Project for Strategic Development of Advanced Robotics Elemental
Technologies.

This software is licensed under the GNU Lesser General Public License version 3
(LGPL3). See LICENSE.txt.


Requirements
------------

RTSProfile requires Python 2.7. It will not function with an earlier version of
Python. It has not been tested with Python 3.

Sphinx must be installed to build the documentation.


Installation
------------

There are several methods of installation available:

1. (Preferred method) Use pip to install the PyPi package.

 a. Install pip if it is not already installed.
    See https://pip.pypa.io/en/latest/installing/

 b. Execute the following command to install RTSProfile:

    $ pip install rtsprofile

2. Download the source from either the repository (see "Repository," below) or
   a source archive, extract it somewhere, and install it into your Python
   distribution:

 a. Extract the source, e.g. to a directory /home/blag/src/rtsprofile

 b. Run setup.py to install rtsprofile to your default Python installation::

    $ python setup.py install

3. On Windows, use the Windows installer.


Using the library
-----------------

The library has one main entry point: the RtsProfile class. Create an instance
of this class, giving the constructor just one data source. The library will
parse that source and give you a complete RT System Profile. You can then use
the properties (they're Python properties, not class methods) to access
information about the RT System. For further details, see the doxygen-generated
documentation.


Running the tests
----------------------

A pair of test specifications, one in each format, are included with the
library. You can execute the test on these files as below:

 $ python test/test.py ./test/rtsystem.xml
 $ python test/test.py ./test/rtsystem.yaml

Be aware that, depending on your Python paths, the tests may be executed
against an installed copy of rtsprofile rather than the copy in the current
working directory.

These tests are not yet complete coverage.


API naming conventions
----------------------

rtsprofile follows the standard Python naming conventions as laid out in PEP8
(http://www.python.org/dev/peps/pep-0008/).

Most importantly, the private, internal API functions begin with an underscore
(_). If a function begins with an underscore, it is not intended for use
outside the class and doing so could lead to undefined behaviour. Only use
those API functions that do not begin with an underscore and have a docstring
in your programs.


Further documentation and examples
----------------------------------

For further documentation, see the Doxygen-generated API documentation.

For examples of using the library, see the "rtresurrect" and "rtcryo" tools.


Future features
---------------

The following features are planned for future releases:

- Complete unit tests.


Repository
----------

The latest source is stored in a Git repository at github, available at
http://github.com/gbiggs/rtsprofile. You can download it as a zip file or
tarball by clicking the "Download Source" link in the top right of the page.
Alternatively, use Git to clone the repository. This is better if you wish to
contribute patches.

 $ git clone git://github.com/gbiggs/rtsprofile.git


Changelog
---------

4.1

- Switched setup script from distutils to setuptools
- Dropped support for Python 2.6

4.0:
- Use the correct namespace string when saving connection properties.

2.0:
- Fixed parsing of Message Sending nodes.
- PrecedingCondition timeout type is now integer.
- Added YAML support.
- Added tests.
- Changed the default string for Preceding conditions to "SYNC".
- Minor bug fixes

