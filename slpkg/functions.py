#!/usr/bin/python
# -*- coding: utf-8 -*-

# functions.py

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

def get_file(link, char):
    '''
    Get filename from links
    '''
    i = 0
    results = []
    for file in range(len(link)):
        i -= 1
        results.append(link[i])
        if link[i] == char:
            break
    return "".join(results[::-1]).replace("/", "").strip(" ")
