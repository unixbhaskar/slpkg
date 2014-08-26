#!/usr/bin/python
# -*- coding: utf-8 -*-

# dependency.py

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Utility for easy management packages in Slackware

# https://github.com/dslackw/slpkg

# This program is free software: you can redistribute it and/or modify
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

from slpkg.colors import colors
from slpkg.__metadata__ import pkg_path, sp
from slpkg.messages import pkg_not_found, template

from slpkg.pkg.find import find_package

from init import initialization
from search import sbo_search_pkg
from greps import sbo_requires_pkg
from download import sbo_slackbuild_dwn

dep_results = []

def sbo_dependencies_pkg(name):
    '''
    Build tree of dependencies
    '''
    try:
        if name is not "%README%":
            sbo_url = sbo_search_pkg(name)
            if sbo_url is None:
                sys.stdout.write("Done\n")
                message = "From slackbuilds.org"
                bol, eol = "\n", "\n"
                pkg_not_found(bol, name, message, eol)
            else:
                dependencies = sbo_requires_pkg(sbo_url, name)
                if dependencies:
                    dep_results.append(dependencies)
                for dep in dependencies:
                        sys.stdout.write(".")
                        sys.stdout.flush()
                        sbo_dependencies_pkg(dep)
                return dep_results
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()

def pkg_tracking(name):
    '''
    Print tree of dependencies
    '''
    sys.stdout.write("Reading package lists ...")
    initialization()
    dependencies_list = sbo_dependencies_pkg(name)
    if dependencies_list is None:
        pass
    elif dependencies_list == []:
        sys.stdout.write("Done\n")
        print("\nPackage {0} no dependencies\n".format(name))
    else:
        sys.stdout.write("Done\n")
        print # new line at start
        requires, dependencies = [], []
        for pkg in dependencies_list:
            requires += pkg
        requires.reverse()
        for duplicate in requires:
            if duplicate not in dependencies:
                dependencies.append(duplicate)
        pkg_len = len(name) + 24
        template(pkg_len)
        print("| Package {0}{1}{2} dependencies :".format(colors.CYAN, name,
                                                           colors.ENDC))
        template(pkg_len)
        print("\\")
        print(" +---{0}[ Tree of dependencies ]{1}".format(colors.YELLOW, colors.ENDC))
        index = 0
        for pkg in dependencies:
            index += 1
            if find_package(pkg + sp, pkg_path):
                print(" |")
                print(" {0}{1}: {2}{3}{4}".format("+--", index, colors.GREEN, pkg, colors.ENDC))
            else:
                print(" |")
                print(" {0}{1}: {2}{3}{4}".format("+--", index, colors.RED, pkg, colors.ENDC))
        print # new line at end
