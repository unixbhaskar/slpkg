#!/usr/bin/python
# -*- coding: utf-8 -*-

# downloader.py file is part of slpkg.

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

import sys
import subprocess

from colors import GREEN, ENDC


class Download(object):

    def __init__(self, path, url):
        self.path = path
        self.url = url
        self.file_name = self.url.split("/")[-1]

    def start(self):
        '''
        Download files usign wget.
        Check if file already download the skip or continue
        download if before stoped.
        '''
        print("\n{0}[ Download ] -->{1} {2}\n".format(GREEN, ENDC,
                                                      self.file_name))
        try:
            subprocess.call("wget -c -N --directory-prefix={0} {1}".format(
                            self.path, self.url), shell=True)
        except KeyboardInterrupt:
            print   # new line at cancel
            sys.exit()
