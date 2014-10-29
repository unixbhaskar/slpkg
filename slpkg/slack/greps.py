#!/usr/bin/python
# -*- coding: utf-8 -*-

# greps.py file is part of slpkg.

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

from slpkg.toolbar import status


def slack_data(PACKAGES_TXT, step):
    '''
    Grap data packages
    '''
    (name, location, size, unsize) = ([] for i in range(4))
    index, toolbar_width = 0, 700
    for line in PACKAGES_TXT.splitlines():
        index += 1
        toolbar_width = status(index, toolbar_width, step)
        if line.startswith("PACKAGE NAME"):
            name.append(line[15:].strip())
        if line.startswith("PACKAGE LOCATION"):
            location.append(line[21:].strip())
        if line.startswith("PACKAGE SIZE (compressed):  "):
            size.append(line[28:-2].strip())
        if line.startswith("PACKAGE SIZE (uncompressed):  "):
            unsize.append(line[30:-2].strip())
    return [name, location, size, unsize]
