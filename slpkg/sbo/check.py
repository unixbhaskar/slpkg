#!/usr/bin/python
# -*- coding: utf-8 -*-

# check.py

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
import getpass
import subprocess

from slpkg.pkg.build import *
from slpkg.pkg.find import find_package
from slpkg.pkg.manager import pkg_upgrade

from slpkg.colors import colors
from slpkg.functions import get_file
from slpkg.messages import pkg_not_found, s_user, template
from slpkg.__metadata__ import tmp, pkg_path, uname, arch, sp
from slpkg.__metadata__ import sbo_arch, sbo_tag, sbo_filetype, build_path

from search import sbo_search_pkg
from download import sbo_slackbuild_dwn
from greps import sbo_source_dwn, sbo_extra_dwn, sbo_version_pkg

def sbo_check(name):
    '''
    Check for new package updates
    '''
    sys.stdout.write("Reading package lists ...")
    sbo_file = "".join(find_package(name + sp, pkg_path))
    if sbo_file == "":
        sys.stdout.write("Done\n")
        message = "Not installed"
        bol, eol = "\n", "\n"
        pkg_not_found(bol, name, message, eol)
    else:
        sys.stdout.flush()
        sbo_url = sbo_search_pkg(name)
        if sbo_url is None:
            sys.stdout.write("Done\n")
            message = "From slackbuilds.org"
            bol, eol = "\n", "\n"
            pkg_not_found(bol, name, message, eol)
        else:
            sys.stdout.write("Done\n")
            sbo_version = sbo_version_pkg(sbo_url, name)
            sbo_dwn = sbo_slackbuild_dwn(sbo_url, name)
            source_dwn = sbo_source_dwn(sbo_url, name)
            extra_dwn = sbo_extra_dwn(sbo_url, name)
            sbo_file_version = sbo_file[len(name) + 1:-len(arch) - 7]
            if sbo_version > sbo_file_version:
                print("\n{0}New version is available:{1}".format(
                        colors.YELLOW, colors.ENDC))
                template(78)
                print("| Package {0} {1} --> {2} {3}".format(
                        name, sbo_file_version,  name, sbo_version))
                template(78)
                print # new line at start
                try:
                    read = raw_input("Would you like to install [Y/n]? ")
                except KeyboardInterrupt:
                    print # new line at exit
                    sys.exit()
                if read == "Y" or read == "y":
                    s_user(getpass.getuser())
                    if not os.path.exists(build_path):
                        os.mkdir(build_path)
                    os.chdir(build_path)
                    pkg_for_install = ("{0}-{1}".format(name, sbo_version))
                    script = get_file(sbo_dwn, "/")
                    source = get_file(source_dwn, "/")
                    print("\n{0}Start -->{1}\n".format(colors.GREEN, colors.ENDC))
                    subprocess.call("wget -N {0} {1}".format(sbo_dwn, source_dwn), shell=True)
                    extra = []
                    if extra_dwn:
                        for src in extra_dwn.split():
                            subprocess.call("wget -N {0}".format(src), shell=True)
                            extra.append(get_file(src, "/"))
                    build_package(script, source, extra, build_path)
                    binary = ("{0}{1}{2}{3}{4}".format(
                               tmp, pkg_for_install, sbo_arch, sbo_tag, sbo_filetype).split())
                    pkg_upgrade(binary)                     
            else:
                print("\nPackage {0}-{1} is up to date\n".format(name, sbo_file_version))
