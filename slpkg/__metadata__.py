#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

__prog__ = "slpkg"
__author__ = "dslackw"
__version_info__ = (1, 6, 2)
__version__ = "{0}.{1}.{2}".format(*__version_info__)
__license__ = "GNU General Public License v3 (GPLv3)"
__email__ = "d.zlatanidis@gmail.com"

''' file spacer '''
sp = "-"

''' temponary path '''
tmp = "/tmp/"
slpkg_path = tmp + "slpkg/"

''' packages log files path '''
pkg_path = "/var/log/packages/"

''' computer architecture '''
uname = os.uname()
arch = (uname[4])

''' slackbuild fietype binary packages '''
sbo_arch = "*"
sbo_tag = "?_SBo"
sbo_filetype = ".tgz"
