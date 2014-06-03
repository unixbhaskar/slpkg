.. image:: https://badge.fury.io/py/slpkg.png
    :target: http://badge.fury.io/py/slpkg
.. image:: https://pypip.in/d/slpkg/badge.png
    :target: https://pypi.python.org/pypi/slpkg
.. image:: https://pypip.in/license/slpkg/badge.png
    :target: https://pypi.python.org/pypi/slpkg


Slpkg is a terminal tool in order to easy use Slackware packages.


.. image:: https://raw.githubusercontent.com/dslackw/slpkg/master/logo/slpkg.png
    :scale: 60%
    :width: 30%
    :align: left


Features
--------
- Download package with all dependencies,
  build and install all in a command
- Automatic tool build and install packages
- List all installed packages
- Τracking dependencies
- Checking for updated packages
- Find and Download packages from SBo repositority
- View README file
- View SlackBuild file
- View Info file
- Auto Download and Build packages
- Install binary packages
- Install-upgrade packages with new
- Reinstall the same packages
- Remove packages
- Find installed packages
- Display the contents of the packages
- No dependencies

It's a quick and easy way to manage your packages in slackware
to a command.

[CHANGELOG] : https://github.com/dslackw/slpkg/blob/master/CHANGELOG


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

	usage: slpkg [-h] [-v] [-a script [source ...]] [-l all, sbo [all, sbo ...]]
        	     [-t] [-n] [-c] [-s] [-i  [...]] [-u  [...]] [-o  [...]]
             	     [-r  [...]] [-f  [...]] [-d  [...]]

	Utility to help package management in Slackware

	optional arguments:
	  -h, --help            show this help message and exit
	  -v, --verbose         print version and exit
	  -a script [source ...]
	                        auto build package
	  -l all, sbo [all, sbo ...]
	                        list of installed packages
	  -t                    tracking dependencies
	  -n                    find from SBo repositority
	  -c                    check if your package is up to date
	  -s                    download, build & install pkg from SBo
	  -i  [ ...]            install binary packages
	  -u  [ ...]            install-upgrade packages with new
	  -o  [ ...]            reinstall the same packages
	  -r  [ ...]            remove packages
	  -f  [ ...]            find if packages installed
	  -d  [ ...]            display the contents of the packages



Slpkg Examples
--------------

Find package from slackbuilds.org download, 
build and install with all dependencies :

.. code-block:: bash
	
	$ slpkg -s brasero
	Searching `brasero` from slackbuilds.org ...
	Searching `libunique` from slackbuilds.org .....
	Searching `gst1-plugins-bad` from slackbuilds.org ......
	Searching `gst1-plugins-base` from slackbuilds.org ........
	Searching `gstreamer1` from slackbuilds.org ....
	Searching `orc` from slackbuilds.org ....

	+==============================================================================
	| Installing new package /tmp/brasero-3.11.3-x86_64-1_SBo.tgz
	+==============================================================================

        Verifying package brasero-3.11.3-x86_64-1_SBo.tgz.
	Installing package brasero-3.11.3-x86_64-1_SBo.tgz:
	PACKAGE DESCRIPTION:
	# brasero (CD/DVD burning application)
	#
	# Brasero is a application to burn CD/DVD for the Gnome Desktop. It is
	# designed to be as simple as possible and has some unique features to
	# enable users to create their discs easily and quickly.
	#
	# Homepage: http://projects.gnome.org/brasero
	#
	Executing install script for brasero-3.11.3-x86_64-1_SBo.tgz.
	Package brasero-3.11.3-x86_64-1_SBo.tgz installed.

	

Tracking all dependencies of packages:

.. code-block:: bash

	$ slpkg -t brasero

	+=========================
	| brasero dependencies :
	+=========================
	 |
	 |
	 -- 1 orc
	 |
	 -- 1 gstreamer1
	 |
	 -- 1 gst1-plugins-base
	 |
	 -- 2 libunique gst1-plugins-bad



Check if your packages is up to date (www.slackbuilds.org):

.. code-block:: bash


	$ slpkg -c flashplayer-plugin
	Searching `flashplayer-plugin` from slackbuilds.org ...

	New version is available !!!
	+==================================================
	| flashplayer-plugin 11.2.202.356
	+==================================================


	$ slpkg -c ranger
	Searching `ranger` from slackbuilds.org ...

	Your package is up to date


	$ slpkg -c termcolor

	The package `termcolor` not found on your system


Find slackbuild from network (www.slackbuilds.org):

.. code-block:: bash


	$ slpkg -n bitfighter
	Searching `bitfighter` from slackbuilds.org ...

	+=======================================================================================
	| The `bitfighter` found in --> http://slackbuilds.org/repository/14.1/games/bitfighter/
	+=======================================================================================
	| Download SlackBuild : http://slackbuilds.org/slackbuilds/14.1/games/bitfighter.tar.gz
	| Source Downloads : http://bitfighter.org/files/bitfighter-019c.tar.gz 
	| Extra Downloads : https://bitfighter.googlecode.com/files/classic_level_pack.zip
	| Package requirements : OpenAL SDL2 speex libmodplug
	+=======================================================================================
         README               View the README file
	 SlackBuild           View the SlackBuild file
	 Info                 View the Info file
         Download             Download this package
	 Build                Download and build this package

        _


Auto build tool to build package:

.. code-block:: bash



	Two files termcolor.tar.gz and termcolor-1.1.0.tar.gz
	must be in the same directory.

	$ slpkg -a termcolor.tar.gz termcolor-1.1.0.tar.gz

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

	Use `slpkg -u` to install - upgrade this package
	

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

	The package `termcolor` removed


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
