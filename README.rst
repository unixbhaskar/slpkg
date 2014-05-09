=====
Slpkg
=====

.. image:: http://badge.fury.io/py/slpkg.png
    :target: https://pypi.python.org/pypi/slpkg
.. image:: https://pypip.in/d/slpkg/badge.png
    :target: https://pypi.python.org/pypi/slpkg
.. image:: https://pypip.in/license/slpkg/badge.png
    :https://pypi.python.org/pypi/slpkg/


Slpkg is a terminal tool , written in Python that allows the
upgrade, remove, find and view Slackware packages contents.

It's a quick and easy way to manage your packages in slackware
to a command.

Note: the program is being developed.


Installation
------------

Using slackware command:

.. code-block:: bash
	
	Download from http://slackbuilds.org
	or
	using sbopkg tool http://www.sbopkg.org

Using pip:

.. code-block:: bash

	$ pip install slpkg
	
	uninstall:

	$ pip uninstall slpkg



Command Line Tool Usage
-----------------------

.. code-block:: bash

	usage: slpkg [-h] [-v] [-u UPGRADE] [-a REINSTALL] [-r REMOVE] [-l] [-f FIND]
        	     [-d DISPLAY]

	Slpkg is a Slackware tool to upgrade, remove, find and view packages contents

	optional arguments:
	  -h, --help            show this help message and exit
	  -v, --verbose         print version and exit
	  -u UPGRADE, --upgrade UPGRADE
        	                install-upgrade package with new
	  -a REINSTALL, --reinstall REINSTALL
        	                reinstall the same package
	  -r REMOVE, --remove REMOVE
        	                remove package
	  -l, --list            list of installed packages
	  -f FIND, --find FIND  find if package installed
	  -d DISPLAY, --display DISPLAY
        	                display the contents of the package

Slpkg Examples
--------------


Upgrade package:

.. code-block:: bash

	$ slpkg -u termcolor-1.1.0-x86_64-1_SBo.tgz

	+==============================================================================
	| Installing new package ./termcolor-1.1.0-x86_64-1_SBo.tgz
	+==============================================================================

	Verifying package termcolor-1.1.0-x86_64-1_SBo.tgz.
	Installing package termcolor-1.1.0-x86_64-1_SBo.tgz:
	PACKAGE DESCRIPTION:
	# termcolor (ANSII Color formatting for output in terminal)
	#
	# termcolor allows you to format your output in terminal.
	#
	# Project URL: https://pypi.python.org/pypi/termcolor
	#
	Package termcolor-1.1.0-x86_64-1_SBo.tgz installed.


Find if your package installed:

.. code-block:: bash

	$ slpkg -f termcolor
	The package is installed on your system


Display the contents of the package:

.. code-block:: bash

	$ slpkg -d termcolor
	PACKAGE NAME:     termcolor-1.1.0-x86_64-1_SBo
	COMPRESSED PACKAGE SIZE:     8.0K
	UNCOMPRESSED PACKAGE SIZE:     60K
	PACKAGE LOCATION: ./termcolor-1.1.0-x86_64-1_SBo.tgz
	PACKAGE DESCRIPTION:
	termcolor: termcolor (ANSII Color formatting for output in terminal)
	termcolor:
	termcolor: termcolor allows you to format your output in terminal.
	termcolor:
	termcolor:
	termcolor: Project URL: https://pypi.python.org/pypi/termcolor
	termcolor:
	termcolor:
	termcolor:
	termcolor:
	FILE LIST:
	./
	usr/
	usr/lib64/
	usr/lib64/python2.7/
	usr/lib64/python2.7/site-packages/
	usr/lib64/python2.7/site-packages/termcolor.py
	usr/lib64/python2.7/site-packages/termcolor.pyc
	usr/lib64/python2.7/site-packages/termcolor-1.1.0-py2.7.egg-info
	usr/lib64/python3.3/
	usr/lib64/python3.3/site-packages/
	usr/lib64/python3.3/site-packages/termcolor-1.1.0-py3.3.egg-info
	usr/lib64/python3.3/site-packages/__pycache__/
	usr/lib64/python3.3/site-packages/__pycache__/termcolor.cpython-33.pyc
	usr/lib64/python3.3/site-packages/termcolor.py
	usr/doc/
	usr/doc/termcolor-1.1.0/
	usr/doc/termcolor-1.1.0/termcolor.SlackBuild
	usr/doc/termcolor-1.1.0/README.rst
	usr/doc/termcolor-1.1.0/CHANGES.rst
	usr/doc/termcolor-1.1.0/PKG-INFO
	usr/doc/termcolor-1.1.0/COPYING.txt
	install/
	install/slack-desc


Remove package:

.. code-block:: bash

	$ slpkg -r termcolor
	!!! WARNING !!!
	Are you sure to remove this package [y/n] y

	Package: termcolor-1.1.0-x86_64-1_SBo
		Removing... 

	Removing package /var/log/packages/termcolor-1.1.0-x86_64-1_SBo...
	Removing files:
	  --> Deleting /usr/doc/termcolor-1.1.0/CHANGES.rst
	  --> Deleting /usr/doc/termcolor-1.1.0/COPYING.txt
	  --> Deleting /usr/doc/termcolor-1.1.0/PKG-INFO
	  --> Deleting /usr/doc/termcolor-1.1.0/README.rst
	  --> Deleting /usr/doc/termcolor-1.1.0/termcolor.SlackBuild
	  --> Deleting /usr/lib64/python2.7/site-packages/termcolor-1.1.0-py2.7.egg-info
	  --> Deleting /usr/lib64/python2.7/site-packages/termcolor.py
	  --> Deleting /usr/lib64/python2.7/site-packages/termcolor.pyc
	  --> Deleting /usr/lib64/python3.3/site-packages/__pycache__/termcolor.cpython-33.pyc
	  --> Deleting /usr/lib64/python3.3/site-packages/termcolor-1.1.0-py3.3.egg-info
	  --> Deleting /usr/lib64/python3.3/site-packages/termcolor.py
	  --> Deleting empty directory /usr/lib64/python3.3/site-packages/__pycache__/
	WARNING: Unique directory /usr/lib64/python3.3/site-packages/ contains new files
	WARNING: Unique directory /usr/lib64/python3.3/ contains new files
	  --> Deleting empty directory /usr/doc/termcolor-1.1.0/

	
	$ slpkg -f termcolor
	The package is not installed on your system

	$ slpkg -d termcolor
	The package is not found

	$ slpkg -v
	Version: x.x.x

