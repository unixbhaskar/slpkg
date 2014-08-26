#!/usr/bin/python
# -*- coding: utf-8 -*-

# search.py

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

import os
import re
import sys

from slpkg.functions import get_file
from slpkg.__metadata__ import lib_path

from slpkg.slack.slack_version import slack_ver

def sbo_search_pkg(name):
    '''
    Search for package path from SLACKBUILDS.TXT file
    '''
    try:
        sbo_url = ("http://slackbuilds.org/slackbuilds/{0}/".format(slack_ver()))
        for line in open(lib_path + "sbo_repo/SLACKBUILDS.TXT", "r"):
            if line.startswith("SLACKBUILD LOCATION"):
                if name == get_file(line[23:].strip(), "/").replace("\n", ""):
                    return sbo_url + line[23:].strip() + "/"
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
