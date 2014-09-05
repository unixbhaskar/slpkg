.. image:: https://badge.fury.io/py/slpkg.png
    :target: http://badge.fury.io/py/slpkg
.. image:: https://pypip.in/d/slpkg/badge.png
    :target: https://pypi.python.org/pypi/slpkg
.. image:: https://pypip.in/license/slpkg/badge.png
    :target: https://pypi.python.org/pypi/slpkg
.. image:: https://raw.githubusercontent.com/dslackw/images/master/slpkg/logo.png
    :target: https://github.com/dslackw/slpkg 

slpkg 1.8.1
===========
 
`Slpkg <https://github.com/dslackw/slpkg>`_ is a terminal multitool in order to easy use `Slackware <http://www.slackware.com/>`_ 
packages.

The tool focuses on slpkg easy and understandable use.
Species are adapted to two repositories:

- SBo - `slackbuilds.org <http://slackbuilds.org/>`_
- Slack - `slackware.com <http://www.slackware.com/>`_

The slpkg cooperate in accordance with the standards of the organization slackbuilds.org 
to build a package,
are also used as the Slackware instructions for installing, upgrading or removing a 
package. 

What makes slpkg apart from other tools is the friendliness and the use of color for the 
enhancement packages
that are not installed on the system or is.

The big advantages is resolving dependencies packages from repository slackbuilds.org and
monitored for upgraded packages.

Of course you wonder how the slpkg is up to date at all times;
It's simple, every time there is a change in ChangeLog.txt before proceeding to any 
execution program looksat whether there is a change in file size and downloads and updates
the SLACKBUILDS.TXT file.

Also you can install official packages of your favorite distribution directly from the 
official repositories
of Slackware. Even you can check for the official updates and install them.

I should be grateful if you experience the slpkg and share your opinion with me.

And as we say Slackers, Keep it Simple Stupid!


.. image:: https://raw.githubusercontent.com/dslackw/images/master/slpkg/slpkg_package.png
    :target: https://github.com/dslackw/slpkg


Features
========

- Build third party packages from source with all dependencies
- Install packages through from official `Slackware <http://www.slackware.com/>`_ mirrors
- Find and Download packages from `slackbuilds.org <http://slackbuilds.org/>`_
- Grabs packages from slackbuilds.org in real time
- Automatic tool build and install packages
- Check if your distribution is up to date
- Remove packages with all dependencies
- Display the contents of the packages
- Install-upgrade Slackware packages
- Build and install all in a command
- Checking for updated packages
- List all installed packages
- Find installed package
- Read SlackBuilds files
- Τracking dependencies
- No dependencies

It's a quick and easy way to manage your packages in `Slackware <http://www.slackware.com/>`_
to a command.

`[CHANGELOG] <https://github.com/dslackw/slpkg/blob/master/CHANGELOG>`_

Video Tutorial
==============

.. image:: https://raw.githubusercontent.com/dslackw/images/master/slpkg/screenshot-1.png
    :target: https://asciinema.org/a/11755

Installation
------------

Untar the archive and run install.sh script:

.. code-block:: bash
    
    $ tar xvf slpkg-1.8.1.tar.gz
    $ cd slpkg-1.8.1
    $ ./install.sh

Using `pip <https://pip.pypa.io/en/latest/>`_ :

.. code-block:: bash

    $ pip install slpkg
    
    uninstall:

    $ pip uninstall slpkg

Using Slackware command:
    
Download `SBo package <http://slackbuilds.org/repository/14.1/system/slpkg/>`_

Download binary package from `SourceForge <https://sourceforge.net/projects/slpkg/>`_
    
Command Line Tool Usage
-----------------------

.. code-block:: bash

    usage: slpkg   [-h] [-v] [-a script [source ...]] 
                   [-l all, sbo, slack, noarch] [-c sbo, slack [<upgrade> ...]]
                   [-s sbo, slack [<package> ...]] [-t] [-n] [-i  [...]]
                   [-u  [...]] [-o  [...]] [-r  [...]] [-f  [...]] [-d  [...]]

    Utility for easy management packages in Slackware

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         print version and exit
      -a script [source ...]
                            auto build package
      -l all, sbo, slack, noarch
                            list of installed packages
      -c sbo, slack [<upgrade> ...]
                            check if your packages is up to date
      -s sbo, slack [<package> ...]
                            download, build & install packages
      -t                    packages tracking dependencies from SBo
      -n                    view packages from SBo repository
      -i  [ ...]            install binary packages
      -u  [ ...]            upgrade binary packages
      -o  [ ...]            reinstall binary packages
      -r  [ ...]            remove binary packages
      -f  [ ...]            view installed packages
      -d  [ ...]            display the contents of the packages


Slpkg Examples
--------------

Find package from slackbuilds.org download, 
build and install with all dependencies :

.. code-block:: bash
    
    $ slpkg -s sbo brasero
    Building dependency tree...... Done
    
    The following packages will be automatically installed or upgraded with new version:
    
    +==============================================================================
    | Package                                 Version         Arch       Repository
    +==============================================================================
    Installing:
      brasero                                 3.11.3          x86_64     SBo
    Installing for dependencies:
      orc                                     0.4.19          x86_64     SBo
      gstreamer1                              1.2.2           x86_64     SBo
      gst1-plugins-base                       1.2.2           x86_64     SBo
      gst1-plugins-bad                        1.2.2           x86_64     SBo
      libunique                               1.1.6           x86_64     SBo

    Installing summary
    ===============================================================================
    Total 6 packages.
    6 packages will be installed, 0 allready installed.

    Do you want to continue [Y/n]? y
    .
    .
    .
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
    
Find packages from `Slackware official mirrors <http://mirrors.slackware.com/>`_ 
download and install:

.. code-block:: bash

    $ slpkg -s slack mozilla

    Packages with name matching [ mozilla ]
    
    Reading package lists.............................. Done    

    +==============================================================================
    | Package                                   Arch     Build   Repos   Size
    +==============================================================================
    Installing:
      mozilla-firefox-24.1.0esr                 x86_64   1       Slack   23524  K
      mozilla-nss-3.15.2                        x86_64   2       Slack   1592  K
      mozilla-thunderbird-24.1.0                x86_64   1       Slack   24208  K

    Installing summary
    ===============================================================================

    Total 3 packages.
    3 packages will be installed, 0 allready installed.
    Need to get 6.02 Mb of archives.
    After this process, 15.72 Mb of additional disk space will be used.

    Would you like to install [Y/n]?

Tracking all dependencies of packages,
and also displays installed packages:

.. code-block:: bash

    $ slpkg -t brasero
    Reading package lists...... Done

    +=========================
    | brasero dependencies   :
    +=========================
    \ 
     +---[ Tree of dependencies ]
     |
     +--1 orc
     |
     +--2 gstreamer1
     |
     +--3 gst1-plugins-base
     |
     +--4 gst1-plugins-bad
     |
     +--5 libunique

Check if your packages is up to date from slackbuilds.org:

.. code-block:: bash

    $ slpkg -c sbo upgrade
    Reading package lists. Done

    These packages need upgrading:

    +==============================================================================
    | Package                             New version       Arch         Repository
    +==============================================================================
    Upgrading:
      six-1.7.1                           1.7.3             x86_64       SBo
      pysetuptools-3.4                    3.6               x86_64       SBo
      Jinja2-2.7.0                        2.7.2             x86_64       SBo
      pysed-0.3.0                         0.3.1             x86_64       SBo
      Pafy-0.3.56                         0.3.58            x86_64       SBo
      MarkupSafe-0.21                     0.23              x86_64       SBo
      pip-1.5.3                           1.5.6             x86_64       SBo
      colored-1.1.1                       1.1.4             x86_64       SBo
                
    Installing summary
    ===============================================================================
    Total 8 packages will be upgraded.
                
    Would you like to upgrade [Y/n]?

Check if your distribution is up to date from `Slackware official mirrors 
<http://mirrors.slackware.com/>`_

.. code-block:: bash

    $ slpkg -c slack upgrade
    Reading package lists....... Done

    These packages need upgrading:

    +==============================================================================
    | Package                                   Arch     Build   Repos   Size
    +==============================================================================
    Upgrading:
      dhcpcd-6.0.5                              x86_64   3       Slack   92  K
      samba-4.1.11                              x86_64   1       Slack   9928 K
      xscreensaver-5.29                         x86_64   1       Slack   3896 K

    Installing summary
    ===============================================================================
    Total 3 package will be upgrading.
    Need to get 1.70 Mb of archives.
    After this process, 9.51 Mb of additional disk space will be used.
    
    Would you like to upgrade [Y/n]?

Find packages from slackbuilds.org:

.. code-block:: bash

    $ slpkg -n bitfighter
    Reading package lists. Done
    
    +===============================================================================
    | Package bitfighter --> http://slackbuilds.org/repository/14.1/games/bitfighter/
    +===============================================================================
    | SlackBuild : bitfighter.tar.gz
    | Sources : bitfighter-019c.tar.gz 
    | Requirements : OpenAL, SDL2, speex, libmodplug
    +===============================================================================
     README               View the README file
     SlackBuild           View the SlackBuild file
     Info                 View the Info file
     Download             Download this package
     Build                Download and build this package
     Install              Download/Build/Install
     Quit                 Quit
    _

Auto tool to build package:

.. code-block:: bash

    Two files termcolor.tar.gz and termcolor-1.1.0.tar.gz
    must be in the same directory.
    (slackbuild script & source code or extra sources if needed)

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
    copying build/lib/termcolor.py -> 
    /tmp/SBo/package-termcolor/usr/lib64/python2.7/site-packages
    byte-compiling /tmp/SBo/package-termcolor/usr/lib64/python2.7/site-packages/termcolor.py 
    to termcolor.pyc
    running install_egg_info
    Writing 
    /tmp/SBo/package-termcolor/usr/lib64/python2.7/site-packages/termcolor-1.1.0-py2.7.egg-info

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

Upgrade, install package:

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

Install mass-packages:

.. code-block:: bash

    $ slpkg -u *.t?z
    
    or 

    $ slpkg -i *.t?z

Find installed packages:

.. code-block:: bash

    $ slpkg -f termcolor lua yetris you-get rar pip
    
    Packages with name matching [ termcolor, lua, yetris, you-get, rar, pip ]

    [ installed ] - termcolor-1.1.0-x86_64-1_SBo
    No such package lua: Cant find
    [ installed ] - yetris-2.0.1-x86_64-1_SBo
    No such package you-get: Cant find
    [ installed ] - rar-5.0.1-x86_64-1_SBo
    [ installed ] - pip-1.5.4-x86_64-1_SBo

Display the contents of the packages:

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
    
    No such package lua: Cant find

Remove packages:

.. code-block:: bash

    $ slpkg -r termcolor
    
    Packages with name matching [ termcolor ]
    
    [ delete ] --> termcolor-1.1.0-x86_64-1_SBo

    Are you sure to remove 1 package(s) [Y/n]? y

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

    +==============================================================================
    | Package: termcolor removed
    +==============================================================================

    $ slpkg -f termcolor lua rar

    Packages with name matching [ termcolor, lua, rar ] 
    
    No such package termcolor: Cant find
    No such package lua: Cant find
    [ installed ] - rar-5.0.1-x86_64-1_SBo

Remove packages with all dependencies:
(presupposes facility with the option 'slpkg -s sbo <package>)

.. code-block:: bash

    $ slpkg -r Flask

    Packages with name matching [ Flask ]

    [ delete ] --> Flask-0.10.1-x86_64-1_SBo

    Are you sure to remove 1 package [Y/n]? y

    +==============================================================================
    | Found dependencies for package Flask:
    +==============================================================================
    | pysetuptools
    | MarkupSafe
    | itsdangerous
    | Jinja2
    | werkzeug
    +==============================================================================

    Remove dependencies (maybe used by other packages) [Y/n]? y
    .
    .
    .
    +==============================================================================
    | Package Flask removed
    | Package pysetuptools removed
    | Package MarkupSafe removed
    | Package itsdangerous removed
    | Package Jinja2 removed
    | Package werkzeug removed
    +==============================================================================

Man page it is available for full support:

.. code-block:: bash

    $ man slpkg
