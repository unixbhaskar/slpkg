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

from colors import colors
from checksum import md5sum
from __metadata__ import log_path
from messages import pkg_not_found, template

from sbo.greps import sbo_checksum_pkg

def build_package(script, sources, path):
    '''
    Build package from source and
    create log file in path /var/log/slpkg/logs/
    '''
    prgnam = script.replace(".tar.gz", "")
    log_file = ("build_{0}_log".format(prgnam))
    logs = log_path + "logs/"
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    if not os.path.exists(logs):
        os.mkdir(logs)
    log_date = time.strftime("%c")
    log_line = ("#" * 79 + "\n\n")
    try:
        if os.path.isfile(logs + log_file):
            os.remove(logs + log_file)
        tar = tarfile.open(script)
        tar.extractall()
        tar.close()
        for src in sources:
            sbo_md5 = sbo_checksum_pkg(prgnam)
            md5 = md5sum(src)
            if sbo_md5 != md5:
                template(78)
                print("| MD5SUM check for {0} [ {1}FAILED{2} ]".format(
                      src, colors.RED, colors.ENDC))
                template(78)
                print("| Expected: {0}".format(md5))
                print("| Found: {0}".format(sbo_md5))
                template(78)
                read = raw_input("\nDo you want to continue [Y/n]? ")
                if read == "Y" or read == "y":
                    pass
                else:
                    sys.exit()
            else:
                template(78)
                print("| MD5SUM check for {0} [ {1}PASS{2} ]".format(
                      src, colors.GREEN, colors.ENDC))
                template(78)
                print # new line after pass checksum
            shutil.copy2(src, prgnam)
        os.chdir(path + prgnam)
        subprocess.call("chmod +x {0}.SlackBuild".format(prgnam), shell=True)
        with open(logs + log_file, "w") as log: # write headers to log file
            log.write(log_line)
            log.write("File : " + log_file + "\n")
            log.write("Path : " + logs + "\n")
            log.write("Date : " + log_date + "\n\n")
            log.write(log_line)
            log.close()
        with open(logs + log_file, "a") as log: # append END tag to a log file
            log.write(log_line)
            log.write(" " * 38 + "E N D\n\n")
            log.write(log_line)
            subprocess.Popen("./{0}.SlackBuild 2>&1 | tee -a {1}{2}".format(
                             prgnam, logs, log_file), shell=True, stdout=sys.stdout).communicate()
            log.close()
            os.chdir(path)
    except (OSError, IOError):
        message = "Wrong file"
        pkg_not_found("\n", prgnam, message, "\n")
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
