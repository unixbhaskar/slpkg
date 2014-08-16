#!/usr/bin/python
# -*- coding: utf-8 -*-

# mirrors.py

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

from slpkg.__metadata__ import arch
from slack_version import slack_ver

def mirrors(name, location):
    '''
    Select Slackware mirror packages
    based architecture
    '''
    if arch == "x86_64":
        http = "http://mirrors.slackware.com/slackware/slackware64-{0}/{1}{2}".format(
                slack_ver(), location, name)
    else:
        http = "http://mirrors.slackware.com/slackware/slackware-{0}/{1}{3}".format(
                slack_ver(), location, name)
    return http
