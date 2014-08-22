#!/usr/bin/python
# -*- coding: utf-8 -*-

# read.py

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

from slpkg.url_read import url_read
from slpkg.__metadata__ import slpkg_tmp

# create tmp directory if not exist
rdm_path = slpkg_tmp + "readme/"
if not os.path.exists(rdm_path):
    if not os.path.exists(slpkg_tmp):
        os.mkdir(slpkg_tmp)
        os.mkdir(rdm_path)

def read_readme(sbo_url, name, site):
    '''
    Read SlackBuild README file
    '''
    readme = url_read(sbo_url + site)
    f = open("{0}{1}.{2}".format(rdm_path, name, site), "w")
    f.write(readme)
    f.close()

def read_info_slackbuild(sbo_url, name, site):
    '''
    Read info SlackBuild file
    '''
    info = url_read(sbo_url + name + site)
    f = open("{0}{1}{2}".format(rdm_path, name, site), "w")
    f.write(info)
    f.close()
