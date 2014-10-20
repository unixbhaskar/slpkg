#!/usr/bin/python
# -*- coding: utf-8 -*-

# tracking.py file is part of slpkg.

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

from slpkg.messages import template
from slpkg.init import initialization
from slpkg.__metadata__ import pkg_path, sp
from slpkg.colors import RED, GREEN, GREY, YELLOW, CYAN, ENDC

from slpkg.pkg.find import find_package

from dependency import sbo_dependencies_pkg


def track_dep(name):
    '''
    View tree of dependencies and also
    highlight packages with color green
    if allready installed and color red
    if not installed.
    '''
    done = "{0}Done{1}\n".format(GREY, ENDC)
    reading_lists = "{0}Reading package lists ...{1}".format(GREY, ENDC)
    sys.stdout.write(reading_lists)
    sys.stdout.flush()
    initialization()
    dependencies_list = sbo_dependencies_pkg(name)
    sys.stdout.write(done)
    if dependencies_list:
        requires, dependencies = [], []
        # Create one list for all packages
        for pkg in dependencies_list:
            requires += pkg
        requires.reverse()
        # Remove double dependencies
        for duplicate in requires:
            if duplicate not in dependencies:
                dependencies.append(duplicate)
        if dependencies == []:
            dependencies = ["No dependencies"]
        pkg_len = len(name) + 24
        print    # new line at start
        template(pkg_len)
        print("| Package {0}{1}{2} dependencies :".format(CYAN, name, ENDC))
        template(pkg_len)
        print("\\")
        print(" +---{0}[ Tree of dependencies ]{1}".format(YELLOW, ENDC))
        index = int()
        for pkg in dependencies:
            index += 1
            if find_package(pkg + sp, pkg_path):
                print(" |")
                print(" {0}{1}: {2}{3}{4}".format("+--", index, GREEN, pkg,
                                                  ENDC))
            else:
                print(" |")
                print(" {0}{1}: {2}{3}{4}".format("+--", index, RED, pkg, ENDC))
        print    # new line at end
    else:
        print("\nNo package was found to match\n")
