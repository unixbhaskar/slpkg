#!/usr/bin/python
# -*- coding: utf-8 -*

# file_size.py

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
import sys
import urllib2

def server_file_size(url):
    '''
    Returns the size of remote files
    '''
    try:
        tar = urllib2.urlopen(url)
        meta = tar.info()
        return meta.getheaders("Content-Length")
    except urllib2.URLError:
        print("\nError: connection refused\n")
        sys.exit()
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()

def local_file_size(registry):
    '''
    Returns the size of local files
    '''
    return os.path.getsize(registry)
