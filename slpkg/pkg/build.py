#!/usr/bin/python
# -*- coding: utf-8 -*-

# build.py

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
import shutil
import tarfile
import subprocess

from slpkg.messages import pkg_not_found, s_user

def build_package(script, source, extra, path):
    '''
    Build package from source
    '''
    pkg_name = script.replace(".tar.gz", "")
    try:
        tar = tarfile.open(script)
        tar.extractall()
        tar.close()
        shutil.copy2(source, pkg_name)
        for src in extra:
            shutil.copy2(src, pkg_name)
        os.chdir(path + pkg_name)
        subprocess.call("./{0}.SlackBuild".format(pkg_name), shell=True)
        os.chdir(path)
    except (OSError, IOError):
        message = "Wrong file"
        bol, eol, pkg = "\n", "\n", ""
        pkg_not_found(bol, pkg, message, eol)
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
