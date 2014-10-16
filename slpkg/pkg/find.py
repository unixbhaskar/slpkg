#!/usr/bin/python
# -*- coding: utf-8 -*-

# find.py file is part of slpkg.

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

import os

from slpkg.blacklist import BlackList
from slpkg.splitting import split_package


def find_package(find_pkg, directory):
    '''
    Find packages
    '''
    pkgs = []
    blacklist = BlackList().packages()
    for pkg in sorted(os.listdir(directory)):
        if pkg.startswith(find_pkg) and split_package(pkg)[0] not in blacklist:
            pkgs.append(pkg)
    return pkgs
