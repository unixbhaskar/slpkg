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
import re
import sys
import time
import shutil
import tarfile
import subprocess

from slpkg.checksum import md5sum
from slpkg.__metadata__ import log_path
from slpkg.colors import RED, GREEN, ENDC
from slpkg.messages import pkg_not_found, template

from slpkg.sbo.greps import SBoGrep


def build_package(script, sources, path):
    '''
    Build package from source and create log
    file in path /var/log/slpkg/sbo/build_logs/.
    Also check md5sum calculates.
    '''
    prgnam = script[:-7]    # remove .tar.gz
    log_file = ("build_{0}_log".format(prgnam))
    sbo_logs = log_path + "sbo/"
    build_logs = sbo_logs + "build_logs/"
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    if not os.path.exists(sbo_logs):
        os.mkdir(sbo_logs)
    if not os.path.exists(build_logs):
        os.mkdir(build_logs)
    log_date = time.strftime("%d/%m/%Y")
    start_log_time = time.strftime("%H:%M:%S")
    start_time = time.time()
    log_line = ("#" * 79 + "\n\n")
    try:
        if os.path.isfile(build_logs + log_file):
            os.remove(build_logs + log_file)
        tar = tarfile.open(script)
        tar.extractall()
        tar.close()
        sbo_md5_list = SBoGrep(prgnam).checksum()
        for src, sbo_md5 in zip(sources, sbo_md5_list):
            # fix build sources with spaces
            src = src.replace("%20", " ")
            md5 = md5sum(src)
            if sbo_md5 != md5:
                template(78)
                print("| MD5SUM check for {0} [ {1}FAILED{2} ]".format(
                      src, RED, ENDC))
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
                print("| MD5SUM check for {0} [ {1}PASSED{2} ]".format(
                      src, GREEN, ENDC))
                template(78)
                print   # new line after pass checksum
            shutil.copy2(src, prgnam)
        os.chdir(path + prgnam)
        subprocess.call("chmod +x {0}.SlackBuild".format(prgnam), shell=True)
        # write headers to log file
        with open(build_logs + log_file, "w") as log:
            log.write(log_line)
            log.write("File : " + log_file + "\n")
            log.write("Path : " + build_logs + "\n")
            log.write("Date : " + log_date + "\n")
            log.write("Time : " + start_log_time + "\n\n")
            log.write(log_line)
            log.close()
            subprocess.Popen("./{0}.SlackBuild 2>&1 | tee -a {1}{2}".format(
                prgnam, build_logs, log_file),
                shell=True, stdout=sys.stdout).communicate()
        end_log_time = time.strftime("%H:%M:%S")
        end_time = time.time()
        diff_time = round(end_time - start_time, 2)
        # calculate build time per package
        if diff_time <= 59.99:
            sum_time = str(diff_time) + " Sec"
        elif diff_time > 59.99 and diff_time <= 3599.99:
            sum_time = round(diff_time / 60, 2)
            sum_time_list = re.findall(r"\d+", str(sum_time))
            sum_time = ("{0} Min {1} Sec".format(sum_time_list[0],
                                                 sum_time_list[1]))
        elif diff_time > 3599.99:
            sum_time = round(diff_time / 3600, 2)
            sum_time_list = re.findall(r"\d+", str(sum_time))
            sum_time = ("{0} Hours {1} Min".format(sum_time_list[0],
                                                   sum_time_list[1]))
        # append END tag to a log file
        with open(build_logs + log_file, "a") as log:
            log.seek(2)
            log.write(log_line)
            log.write("Time : " + end_log_time + "\n")
            log.write("Total build time : {0}\n".format(sum_time))
            log.write(" " * 38 + "E N D\n\n")
            log.write(log_line)
            log.close()
            os.chdir(path)
        print("Total build time for package {0} : {1}\n".format(prgnam,
                                                                sum_time))
    except (OSError, IOError):
        message = "Wrong file"
        pkg_not_found("\n", prgnam, message, "\n")
    except KeyboardInterrupt:
        print   # new line at exit
        sys.exit()
