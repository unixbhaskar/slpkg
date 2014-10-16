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

from slack.slack_version import slack_ver


def split_package(package):
    '''
    Split package in name, version
    arch and build tag.
    '''
    split = package.split("-")
    sbo = "_SBo"
    slack = "_slack{0}".format(slack_ver())
    if sbo in package:
        build = split[-1][:-4]   # remove .t?z extension
    if slack in package:
        build = split[-1][:-len(slack)]
    else:
        build = split[-1]
    arch = split[-2]
    ver = split[-3]
    name = "-".join(split[:-3])
    return [name, ver, arch, build]
