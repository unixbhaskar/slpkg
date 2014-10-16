#!/usr/bin/python
# -*- coding: utf-8 -*-

# read.py file is part of slpkg.

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

from slpkg.url_read import url_read


def read_readme(sbo_url, sbo_readme):
    '''
    Read SlackBuild README file
    '''
    return url_read(sbo_url + sbo_readme)


def read_info_slackbuild(sbo_url, name, sbo_file):
    '''
    Read info and SlackBuild file
    '''
    return url_read(sbo_url + name + sbo_file)
