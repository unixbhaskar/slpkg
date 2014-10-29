#!/usr/bin/python
# -*- coding: utf-8 -*-

# sizes.py file is part of slpkg.

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


def units(comp_sum, uncomp_sum):
    '''
    Calculate package size
    '''
    compressed = round((sum(map(float, comp_sum)) / 1024), 2)
    uncompressed = round((sum(map(float, uncomp_sum)) / 1024), 2)
    comp_unit = uncomp_unit = "Mb"
    if compressed > 1024:
        compressed = round((compressed / 1024), 2)
        comp_unit = "Gb"
    if uncompressed > 1024:
        uncompressed = round((uncompressed / 1024), 2)
        uncomp_unit = "Gb"
    if compressed < 1:
        compressed = sum(map(int, comp_sum))
        comp_unit = "Kb"
    if uncompressed < 1:
        uncompressed = sum(map(int, uncomp_sum))
        uncomp_unit = "Kb"
    return [comp_unit, uncomp_unit], [compressed, uncompressed]
