#!/usr/bin/python
# -*- coding: utf-8 -*-

# messages.py file is part of slpkg.

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Utility for easy management packages in Slackware

# https://github.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
from colors import RED, CYAN, ENDC


def pkg_not_found(bol, pkg, message, eol):
    '''
    Print message when package not found
    '''
    print("{0}No such package {1}: {2}{3}".format(bol, pkg, message, eol))


def pkg_found(pkg, version):
    '''
    Print message when package found
    '''
    print("| Package {0}-{1} is already installed".format(pkg, version))


def pkg_installed(pkg):
    '''
    Print message when package installed
    '''
    print("| Package {0} installed".format(pkg))


def s_user(user):
    '''
    Check for root user
    '''
    if user != "root":
        print("\nslpkg: error: must have root privileges\n")
        sys.exit()


def build_FAILED(sbo_url, prgnam):
    '''
    Print error message if build failed
    '''
    template(78)
    print("| Build package {0} [ {1}FAILED{2} ]".format(prgnam, RED, ENDC))
    template(78)
    print("| See log file in {0}/var/log/slpkg/sbo/build_logs{1} directory or "
          "read README file:".format(CYAN, ENDC))
    print("| {0}{1}".format(sbo_url, "README"))
    template(78)
    print   # new line at end


def template(max_len):
    '''
    Print template
    '''
    print("+" + "=" * max_len)
