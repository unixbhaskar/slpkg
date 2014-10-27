#!/usr/bin/python
# -*- coding: utf-8 -*-

# remove.py file is part of slpkg.

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


def delete(path, packages):
    '''
    Remove downloaded packages
    '''
    read = raw_input("Removal downloaded packages [Y/n]? ")
    if read == "Y" or read == "y":
        for pkg in packages:
            os.remove(path + pkg)
            os.remove(path + pkg + ".asc")
        is_empty(path)
    else:
        is_empty(path)


def is_empty(path):
    if not os.listdir(path):
        print("Packages removed")
    else:
        print("\nThere are packages in direcrory {0}\n".format(path))
