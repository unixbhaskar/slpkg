.. image:: https://badge.fury.io/py/slpkg.png
    :target: http://badge.fury.io/py/slpkg
.. image:: https://pypip.in/d/slpkg/badge.png
    :target: https://pypi.python.org/pypi/slpkg
.. image:: https://pypip.in/license/slpkg/badge.png
    :target: https://pypi.python.org/pypi/slpkg


.. image:: https://raw.githubusercontent.com/dslackw/slpkg/master/logo/slpkg.png
    :scale: 60%
    :width: 30%
    :align: left

Slpkg is a terminal tool , written in Python that allows the
build, upgrade, remove, find and view Slackware packages contents.

It's a quick and easy way to manage your packages in slackware
to a command.

Note: The software is in progress...

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

	usage: slpkg [-h] [-v] [-s script source] [-l all, sbo [all, sbo ...]] [-n]
        	     [-c] [-i  [...]] [-u  [...]] [-a  [...]] [-r  [...]] [-f  [...]]
            	     [-d  [...]]

	Utility to help package management in Slackware

	optional arguments:
  	  -h, --help            show this help message and exit
	  -v, --verbose         print version and exit
	  -s script source, --slackbuild script source
	                        auto build package
	  -l all, sbo [all, sbo ...], --list all, sbo [all, sbo ...]
	                        list of installed packages
	  -n , --network        find from SBo repositority
	  -c , --check          check if your package is up to date
	  -i  [ ...], --install  [ ...]
	                        install binary packages
	  -u  [ ...], --upgrade  [ ...]
	                        install-upgrade package with new
	  -a  [ ...], --reinstall  [ ...]
	                        reinstall the same packages
	  -r  [ ...], --remove  [ ...]
	                        remove packages
	  -f  [ ...], --find  [ ...]
	                        find if packages installed
	  -d  [ ...], --display  [ ...]
	                        display the contents of the packages


Slpkg Examples
--------------

Check if your packages is up to date (www.slackbuilds.org):

.. code-block:: bash


	$ slpkg -c flashplayer-plugin
	Searching for `flashplayer-plugin` from www.slackbuilds.org Please wait ...

	New version is available !!!
	+==================================================
	| flashplayer-plugin 11.2.202.356
	+==================================================


	$ slpkg -c ranger
	Searching for `ranger` from www.slackbuilds.org Please wait ...

	Your package is up to date


	$ slpkg -c termcolor
	Searching for `termcolor` from www.slackbuilds.org Please wait ...

	The package `termcolor` not found on your system

	New version is available !!!
	+==================================================
	| termcolor 1.1.0
	+==================================================



Find slackbuild from network (www.slackbuilds.org):

.. code-block:: bash


	This find the slackbuild , source, extra downloads and package requirements !!!	

	$ slpkg -n brasero
	Searching for `brasero` from www.slackbuilds.org Please wait ...

	+=================================================================================
	| The `brasero` found in --> http://slackbuilds.org/repository/14.1/system/brasero/
	+=================================================================================

	Download SlackBuild : http://slackbuilds.org/slackbuilds/14.1/system/brasero.tar.gz
	Source Downloads : https://download.gnome.org/sources/brasero/3.11/brasero-3.11.3.tar.xz
	Extra Downloads : []
	Package requirements : libunique gst1-plugins-bad


And try again:


.. code-block:: bash

	$ slpkg -n bitfighter
	Searching for `bitfighter` from www.slackbuilds.org Please wait ...

	+======================================================================================
	| The `bitfighter` found in --> http://slackbuilds.org/repository/14.1/games/bitfighter/
	+======================================================================================

	Download SlackBuild : http://slackbuilds.org/slackbuilds/14.1/games/bitfighter.tar.gz
	Source Downloads : http://bitfighter.org/files/bitfighter-019c.tar.gz 
	Extra Downloads : [https://bitfighter.googlecode.com/files/classic_level_pack.zip]
	Package requirements : OpenAL SDL2 speex libmodplug
	

	$ slpkg -n termcolor
	Searching for `termcolor` from www.slackbuilds.org Please wait ...

	+======================================================================================
	| The `termcolor` found in --> http://slackbuilds.org/repository/14.1/python/termcolor/
	+======================================================================================

	Download SlackBuild : http://slackbuilds.org/slackbuilds/14.1/python/termcolor.tar.gz
	Source Downloads : https://pypi.python.org/packages/source/t/termcolor/termcolor-1.1.0.tar.gz
	Extra Downloads : []
	Package requirements :
	

Auto build tool to build package:

.. code-block:: bash



	Etc. download from www.slackbuilds.org the package termcolor
	http://slackbuilds.org/repository/14.1/python/termcolor/

	Two files termcolor.tar.gz and termcolor-1.1.0.tar.gz
	must be in the same directory.

	$ slpkg -s termcolor.tar.gz termcolor-1.1.0.tar.gz

	termcolor/
	termcolor/slack-desc
	termcolor/termcolor.info
	termcolor/README
	termcolor/termcolor.SlackBuild
	termcolor-1.1.0/
	termcolor-1.1.0/CHANGES.rst
	termcolor-1.1.0/COPYING.txt
	termcolor-1.1.0/README.rst
	termcolor-1.1.0/setup.py
	termcolor-1.1.0/termcolor.py
	termcolor-1.1.0/PKG-INFO
	running install
	running build
	running build_py
	creating build
	creating build/lib
	copying termcolor.py -> build/lib
	running install_lib
	creating /tmp/SBo/package-termcolor/usr
	creating /tmp/SBo/package-termcolor/usr/lib64
	creating /tmp/SBo/package-termcolor/usr/lib64/python2.7
	creating /tmp/SBo/package-termcolor/usr/lib64/python2.7/site-packages
	copying build/lib/termcolor.py -> /tmp/SBo/package-termcolor/usr/lib64/python2.7/site-packages
	byte-compiling /tmp/SBo/package-termcolor/usr/lib64/python2.7/site-packages/termcolor.py to termcolor.pyc
	running install_egg_info
	Writing /tmp/SBo/package-termcolor/usr/lib64/python2.7/site-packages/termcolor-1.1.0-py2.7.egg-info

	Slackware package maker, version 3.14159.

	Searching for symbolic links:

	No symbolic links were found, so we won't make an installation script.
	You can make your own later in ./install/doinst.sh and rebuild the
	package if you like.

	This next step is optional - you can set the directories in your package
	to some sane permissions. If any of the directories in your package have
	special permissions, then DO NOT reset them here!

	Would you like to reset all directory permissions to 755 (drwxr-xr-x) and
	directory ownerships to root.root ([y]es, [n]o)? n

	Creating Slackware package:  /tmp/termcolor-1.1.0-x86_64-1_SBo.tgz

	./
	usr/
	usr/lib64/
	usr/lib64/python2.7/
	usr/lib64/python2.7/site-packages/
	usr/lib64/python2.7/site-packages/termcolor.py
	usr/lib64/python2.7/site-packages/termcolor.pyc
	usr/lib64/python2.7/site-packages/termcolor-1.1.0-py2.7.egg-info
	usr/doc/
	usr/doc/termcolor-1.1.0/
	usr/doc/termcolor-1.1.0/termcolor.SlackBuild
	usr/doc/termcolor-1.1.0/README.rst
	usr/doc/termcolor-1.1.0/CHANGES.rst
	usr/doc/termcolor-1.1.0/PKG-INFO
	usr/doc/termcolor-1.1.0/COPYING.txt
	install/
	install/slack-desc

	Slackware package /tmp/termcolor-1.1.0-x86_64-1_SBo.tgz created.


Upgrade install package:

.. code-block:: bash

	$ slpkg -u /tmp/termcolor-1.1.0-x86_64-1_SBo.tgz

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


Of course you can install mass-packages:

.. code-block:: bash

	$ slpkg -u *.t?z
	
	or 

	$ slpkg -i *.t?z


Find if your packages installed:

.. code-block:: bash

	$ slpkg -f termcolor lua yetris you-get rar pip

	found --> termcolor-1.1.0-x86_64-1_SBo
	The package `lua` not found
	found --> yetris-2.0.1-x86_64-1_SBo
	The package `you-get` not found
	found --> rar-5.0.1-x86_64-1_SBo
	found --> pip-1.5.4-x86_64-1_SBo


Display the contents of the package:

.. code-block:: bash

	$ slpkg -d termcolor lua

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
	
	The package `lua` not found

Remove package:

.. code-block:: bash

	$ slpkg -r termcolor
	!!! WARNING !!!
	Are you sure to remove this package(s) [y/n] y

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
	Done ...


	$ slpkg -f termcolor lua rar

	The package `termcolor` not found
	The package `lua` not found
	found --> rar-5.0.1-x86_64-1_SBo


	$ slpkg -v
	Version: x.x.x
	Licence: GNU General Public License v3 (GPLv3)
	Email:   d.zlatanidis@gmail.com

Man page it is available for full support:

.. code-block:: bash

	$ man slpkg
