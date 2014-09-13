#!/usr/bin/python
# -*- coding: utf-8 -*-

# views.py file is part of slpkg.

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
import subprocess

from colors import colors
from functions import get_file
from __metadata__ import tmp, build_path, pkg_path, slpkg_tmp, sp
from messages import pkg_not_found, pkg_found, view_sbo, template, build_FAILED

from pkg.build import build_package
from pkg.find import find_package
from pkg.manager import pkg_upgrade

from read import *
from greps import *
from init import initialization
from search import sbo_search_pkg
from download import sbo_slackbuild_dwn

def sbo_network(name):
    '''
    View SlackBuild package, read or install them 
    from slackbuilds.org
    '''
    rdm_path = slpkg_tmp + "readme/"
    sys.stdout.write("{0}Reading package lists ...{1}".format(
                     colors.GREY, colors.ENDC))
    sys.stdout.flush()
    initialization()
    sbo_url = sbo_search_pkg(name)
    if sbo_url:
        sbo_req = sbo_requires_pkg(sbo_url, name)
        sbo_dwn = sbo_slackbuild_dwn(sbo_url)
        source_dwn = sbo_source_dwn(name).split()
        sys.stdout.write ("{0}Done{1}\n".format(colors.GREY, colors.ENDC))
        view_sbo(name, sbo_url, get_file(sbo_dwn, "/"), \
                 ", ".join([get_file(src, "/") for src in source_dwn]), \
                 sbo_req)
        '''
        Check if package supported by arch
        before proceed to install
        '''
        FAULT = ""
        UNST = ["UNSUPPORTED", "UNTESTED"]
        for item in UNST:
            for un in source_dwn:
                if item == un:
                    FAULT = item
        while True:
            try:
                read = raw_input("_ ")
            except KeyboardInterrupt:
                print # new line at exit
                break
            if read == "D" or read == "d":
                print("\n{0}Start --> {1}{2}\n".format(colors.GREEN, colors.ENDC, name))
                subprocess.call("wget -N {0}".format(sbo_dwn), shell=True)
                for src in source_dwn:
                    subprocess.call("wget -N {0}".format(src), shell=True)
                print("Complete!\n")
                break
            elif read == "R" or read == "r":
                site = "README"
                read_readme(sbo_url, name, site)
                subprocess.call("less {0}{1}.{2}".format(rdm_path, name, site), shell=True)
                os.remove("{0}{1}.{2}".format(rdm_path, name, site))
            elif read == "F" or read == "f":
                site = ".info"
                read_info_slackbuild(sbo_url, name, site)
                subprocess.call("less {0}{1}{2}".format(rdm_path, name, site), shell=True)
                os.remove("{0}{1}{2}".format(rdm_path, name, site))
            elif read == "S" or read == "s":
                site = ".SlackBuild"
                read_info_slackbuild(sbo_url, name, site)
                subprocess.call("less {0}{1}{2}".format(rdm_path, name, site), shell=True)
                os.remove("{0}{1}{2}".format(rdm_path, name, site))
            elif read == "B" or read == "b":
                if FAULT:
                    print("\n{0}The package {1}{2}\n".format(colors.RED, FAULT, colors.ENDC))
                    sys.exit()
                if not os.path.exists(build_path):
                    os.mkdir(build_path)
                sources = []
                os.chdir(build_path)
                script = get_file(sbo_dwn, "/")
                print("\n{0}Start -->{0} {1}\n".format(colors.GREEN, colors.ENDC, name))
                subprocess.call("wget -N {0}".format(sbo_dwn), shell=True)
                for src in source_dwn:
                    subprocess.call("wget -N {0}".format(src), shell=True)
                    sources.append(get_file(src, "/"))
                build_package(script, sources, build_path)
                print("Complete!\n")
                break
            elif read == "I" or read == "i":
                if FAULT:
                    print("\n{0}The package {1}{2}\n".format(colors.RED, FAULT, colors.ENDC))
                    sys.exit()
                if not os.path.exists(build_path):
                    os.mkdir(build_path)
                sbo_version = sbo_version_pkg(name)
                prgnam = ("{0}-{1}".format(name, sbo_version))
                if find_package(prgnam + sp, pkg_path) == []:
                    sources = []
                    os.chdir(build_path)
                    print("\n{0}Start -->{0} {1}\n".format(colors.GREEN, colors.ENDC, name))
                    subprocess.call("wget -N {0}".format(sbo_dwn), shell=True)
                    script = get_file(sbo_dwn, "/")
                    for src in source_dwn:
                            subprocess.call("wget -N {0}".format(src), shell=True)
                            sources.append(get_file(src, "/"))
                    build_package(script, sources, build_path)
                    '''
                    Searches the package name and version in /tmp to install.
                    If find two or more packages e.g. to build tag 
                    2 or 3 will fit most.
                    '''
                    binary_list = []
                    for search in find_package(prgnam, tmp):
                        if "_SBo" in search:
                            binary_list.append(search)
                    try:
                        binary = (tmp + max(binary_list)).split()
                    except ValueError:
                        build_FAILED(sbo_url, prgnam)
                        sys.exit()
                    print("{0}[ Installing ] --> {1}{2}".format(colors.GREEN, colors.ENDC, name))
                    pkg_upgrade(binary)
                    print("Complete!\n")
                    break
                else:
                    template(78)
                    pkg_found(name, sbo_version)
                    template(78)
                    break
            else:
                break
    else:
        sys.stdout.write ("{0}Done{1}\n".format(colors.GREY, colors.ENDC))
        message = "From slackbuilds.org"
        pkg_not_found("\n", name, message, "\n")
