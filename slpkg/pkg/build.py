#!/usr/bin/python
# -*- coding: utf-8 -*-

# build.py file is part of slpkg.

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

import os
import sys
import shutil
import tarfile
import subprocess

from slpkg.messages import pkg_not_found

def build_package(script, sources, path):
    '''
    Build package from source
    '''
    prgnam = script.replace(".tar.gz", "")
    try:
        tar = tarfile.open(script)
        tar.extractall()
        tar.close()
        for src in sources:
            shutil.copy2(src, prgnam)
        os.chdir(path + prgnam)
        subprocess.call("chmod +x {0}.SlackBuild".format(prgnam), shell=True)
        subprocess.call("./{0}.SlackBuild".format(prgnam), shell=True)
        os.chdir(path)
    except (OSError, IOError):
        message = "Wrong file"
        pkg_not_found("\n", prgnam, message, "\n")
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
