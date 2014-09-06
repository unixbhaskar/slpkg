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
import time
import shutil
import tarfile
import subprocess

from messages import pkg_not_found

def build_package(script, sources, path):
    '''
    Build package from source
    '''
    prgnam = script.replace(".tar.gz", "")
    log_file = ("build_{0}_log".format(prgnam))
    log_path = ("{0}{1}/".format(path, prgnam))
    log_date = time.strftime("%c")
    template = ("#" * 78 + "\n\n")
    try:
        if os.path.isfile(log_path + log_file):
            os.remove(log_path + log_file)
        tar = tarfile.open(script)
        tar.extractall()
        tar.close()
        for src in sources:
            shutil.copy2(src, prgnam)
        os.chdir(path + prgnam)
        subprocess.call("chmod +x {0}.SlackBuild".format(prgnam), shell=True)
        p = subprocess.Popen("./{0}.SlackBuild".format(prgnam), shell=True, stdout=subprocess.PIPE)
        log = open(log_file, "a")
        log.write(template)
        log.write("File : " + log_file + "\n")
        log.write("Path : " + log_path + "\n")
        log.write("Date : " + log_date + "\n\n")
        log.write(template)
        for build in p.communicate():
            if build:
                print build,
                log.write(str(build,))
        log.close()
        os.chdir(path)
    except (OSError, IOError):
        message = "Wrong file"
        pkg_not_found("\n", prgnam, message, "\n")
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
