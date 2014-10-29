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

from slpkg.url_read import URL


class Read(object):

    def __init__(self, sbo_url):
        self.sbo_url = sbo_url

    def readme(self, sbo_readme):
        '''
        Read SlackBuild README file
        '''
        return URL(self.sbo_url + sbo_readme).reading()

    def info(self, name, sbo_file):
        '''
        Read info file
        '''
        return URL(self.sbo_url + name + sbo_file).reading()

    def slackbuild(self, name, sbo_file):
        '''
        Read SlackBuild file
        '''
        return URL(self.sbo_url + name + sbo_file).reading()
