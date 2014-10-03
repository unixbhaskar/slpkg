#!/usr/bin/python
# -*- coding: utf-8 -*-

# splitting.py file is part of slpkg.

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

from slpkg.__metadata__ import slack_archs

from slack_version import slack_ver

def split_package(package):
    '''
    Split package in name, version
    arch and build tag.
    '''
    for archs in slack_archs:
        if archs in package:
            arch = archs
        if "_slack" in package:
            slack = "_slack" + slack_ver()
        else:
            slack = ""
    pkg = package[:-(len(slack) + 4)]
    build = pkg.split("-")[-1] 
    pkg_ver = pkg[:-(len(arch) + len(build))]
    ver = pkg_ver.split("-")[-1]
    name = pkg_ver[:-(len(ver) + 1)]
    return [name, ver, arch[1:-1], build]
