#!/usr/bin/python
# -*- coding: utf-8 -*-

# check.py file is part of slpkg.

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

from slpkg.pkg.find import find_package
from slpkg.pkg.build import build_package
from slpkg.pkg.manager import pkg_upgrade

from slpkg.colors import *
from slpkg.downloader import download 
from slpkg.messages import template, build_FAILED
from slpkg.__metadata__ import tmp, pkg_path, build_path, sp

from init import initialization
from search import sbo_search_pkg
from download import sbo_slackbuild_dwn
from dependency import sbo_dependencies_pkg
from greps import sbo_source_dwn, sbo_version_pkg

def sbo_check():
    '''
    Upgrade all slackbuilds packages from slackbuilds.org
    repository.
    NOTE: This functions check packages by version not by build
    tag because build tag not reported the SLACKBUILDS.TXT file,
    but install the package with maximum build tag if find the 
    some version in /tmp directory.
    '''
    try:
        done = "{0}Done{1}\n".format(GREY, ENDC)
        reading_lists = "{0}Reading package lists ...{1}".format(GREY, ENDC)
        sys.stdout.write(reading_lists)
        sys.stdout.flush()
        initialization()
        arches = ["-x86_64-", "-i486-", "-arm-", "-noarch-"]
        index, toolbar_width = int(), 3
        dependencies,  dependencies_list, \
        requires, upgrade, installed, sbo_list, \
        upg_name, pkg_for_upg, upg_ver, upg_arch = ([] for i in range(10))
        for pkg in os.listdir(pkg_path):
            if pkg.endswith("_SBo"):
                sbo_list.append(pkg)
        if sbo_list: 
            for pkg in sbo_list:
                index += 1
                if index == toolbar_width:
                    sys.stdout.write("{0}.{1}".format(GREY, ENDC))
                    sys.stdout.flush()
                    toolbar_width += 4
                for _arch in arches:
                    if _arch in pkg:
                        arch = _arch[1:-1]
                    else:
                        arch = os.uname()[4]
                        if arch.startswith("i") and arch.endswith("86"):
                            arch = "i486"
                package = pkg[:-(len(arch) + len("_SBo") + 3)]
                pkg_version = package.split("-")[-1] 
                name = package[:-(len(pkg_version) + 1)]
                if sbo_search_pkg(name):
                    # search packages if exists in the repository
                    # and it gets to avoidable modified packages
                    # from the user with the tag _SBo
                    sbo_package = ("{0}-{1}".format(name, sbo_version_pkg(name)))
                    if sbo_package > package:
                        upg_name.append(name)
            sys.stdout.write(done)
            if upg_name:
                sys.stdout.write("{0}Resolving dependencies ...{1}".format(
                                 GREY, ENDC))
                sys.stdout.flush()
                # Of the packages found to need upgrading,
                # stored in a series such as reading from the 
                # file .info.
                for upg in upg_name:
                    dependencies = sbo_dependencies_pkg(upg)
                # Because there are dependencies that depend on other 
                # dependencies are created lists into other lists. 
                # Thus creating this loop create one-dimensional list.
                for dep in dependencies:
                    requires += dep
                requires.reverse() # Inverting the list brings the
                                   # dependencies in order to be installed.
                # Many packages use the same dependencies, in this loop 
                # creates a new list by removing duplicate dependencies but 
                # without spoiling the line must be installed.
                for duplicate in requires:
                    if duplicate not in dependencies_list:
                        dependencies_list.append(duplicate)
                # Last and after the list is created with the correct number 
                # of dependencies that must be installed, and add the particular 
                # packages that need to be upgraded if they are not already on 
                # the list in end to list.
                for upg in upg_name:
                    if upg not in dependencies_list:
                        dependencies_list.append(upg)
                # In the end lest a check of the packages that are on the list
                # are already installed.
                for pkg in dependencies_list:
                    ver = sbo_version_pkg(pkg)
                    prgnam = ("{0}-{1}".format(pkg, ver))
                    pkg_version = ver # if package not installed 
                                      # take version from repository
                    arch = os.uname()[4]
                    if arch.startswith("i") and arch.endswith("86"):
                        arch = "i486"
                    if find_package(prgnam, pkg_path) == []:
                        for sbo in os.listdir(pkg_path):
                            if sbo.startswith(pkg + sp) and sbo.endswith("_SBo"):
                                # search if packages installed
                                # if yes grab package name,
                                # version and arch
                                for _arch in arches:
                                    if _arch in sbo:
                                        arch = _arch[1:-1]
                                name = sbo[:-(len(arch) + len("_SBo") + 3)]
                                pkg_version = name.split("-")[-1]
                        upgrade.append(pkg)
                        pkg_for_upg.append("{0}-{1}".format(pkg, pkg_version))
                        upg_ver.append(ver)
                        upg_arch.append(arch)
                sys.stdout.write(done)
            if pkg_for_upg:
                print("\nThese packages need upgrading:\n")
                template(78)
                print("{0}{1}{2}{3}{4}{5}{6}".format("| Package", " " * 30, "New version", \
                      " " * 6 , "Arch", " " * 9, "Repository"))
                template(78)
                print("Upgrading:")
                count_upgraded = count_installed = int()
                for upg, ver, arch in zip(pkg_for_upg, upg_ver, upg_arch):
                    if find_package(upg[:-len(ver)], pkg_path):
                        COLOR = YELLOW
                        count_upgraded += 1
                    else:
                        COLOR = RED
                        count_installed += 1
                    print(" {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(COLOR, upg, ENDC, \
                          " " * (38-len(upg)), GREEN, ver, ENDC, \
                          " " * (17-len(ver)), arch, " " * (13-len(arch)), "SBo"))
                msg_upg = "package"
                msg_ins = msg_upg
                if count_upgraded > 1:
                    msg_upg = msg_upg + "s"
                if count_installed > 1:
                    msg_ins = msg_ins + "s"
                print("\nInstalling summary")
                print("=" * 79)
                print("{0}Total {1} {2} will be upgraded and {3} {4} will be installed.{5}\n".format(
                      GREY, count_upgraded, msg_upg, count_installed, msg_ins, ENDC))
                read = raw_input("Would you like to upgrade [Y/n]? ")
                if read == "Y" or read == "y":
                    if not os.path.exists(build_path):
                        os.mkdir(build_path)
                    os.chdir(build_path)
                    for name, version in zip(upgrade, upg_ver):
                        prgnam = ("{0}-{1}".format(name, version))
                        sbo_url = sbo_search_pkg(name)
                        sbo_dwn = sbo_slackbuild_dwn(sbo_url)
                        src_dwn = sbo_source_dwn(name).split()
                        script = sbo_dwn.split("/")[-1] # keep file from script link
                        download(build_path, sbo_dwn)
                        sources = []
                        for src in src_dwn:
                            download(build_path, src)
                            sources.append(src.split("/")[-1]) # keep file from source link
                        build_package(script, sources, build_path)
                        # Searches the package name and version in /tmp to install.
                        # If find two or more packages e.g. to build tag 
                        # 2 or 3 will fit most.
                        binary_list = []
                        for search in find_package(prgnam, tmp):
                            if "_SBo" in search:
                                binary_list.append(search)
                        try:
                            binary = (tmp + max(binary_list)).split()
                        except ValueError:
                            build_FAILED(sbo_url, prgnam)
                            sys.exit()
                        if find_package(name + sp, pkg_path):
                            print("{0}[ Upgrading ] --> {1}{2}".format(GREEN, ENDC, name))
                        else:
                            print("{0}[ Installing ] --> {1}{2}".format(GREEN, ENDC, name))
                            # Use this list to pick out what 
                            # packages will be installed
                            installed.append(name)
                        pkg_upgrade(binary)
                    if len(pkg_for_upg) > 1:
                        template(78)
                        print("| Total {0} {1} upgraded and {2} {3} installed".format(
                              count_upgraded, msg_upg, count_installed, msg_ins))
                        template(78)
                        for pkg, upg, ver in zip(pkg_for_upg, upgrade, upg_ver):
                            upgraded = ("{0}-{1}".format(upg, ver))
                            if find_package(upgraded, pkg_path):
                                if upg in installed:
                                    print("| Package {0} installed".format(pkg))
                                else: 
                                    print("| Package {0} upgraded with new package {1}-{2}".format(
                                          pkg, upg, ver))
                        template(78)
            else:
                print("\nTotal {0} SBo packages are up to date\n".format(len(sbo_list)))
        else:
            sys.stdout.write(done)
            print("\nNo SBo packages found\n")
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
