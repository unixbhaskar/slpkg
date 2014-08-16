#!/usr/bin/python
# -*- coding: utf-8 -*-

# patches.py

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
import time
import subprocess

from slpkg.colors import colors
from slpkg.messages import s_user
from slpkg.url_read import url_read
from slpkg.__metadata__ import pkg_path, slpkg_tmp, arch

from slpkg.pkg.find import find_package
from slpkg.pkg.manager import pkg_upgrade

from mirrors import mirrors
from slack_version import slack_ver

def patches():
    '''
    Install new patches from official Slackware mirrors
    '''
    try:
        dwn_list, dwn_patches = [], []
        upgrade_all, package_name, package_location = [], [], []
        pch_path = slpkg_tmp + "patches/"
        if not os.path.exists(pch_path):
            if not os.path.exists(slpkg_tmp):
                os.mkdir(slpkg_tmp)
                os.mkdir(pch_path)
        sys.stdout.write ("Reading package lists ...")
        sys.stdout.flush()
        PACKAGE_TXT = url_read(mirrors(name="PACKAGES.TXT", location="patches/"))
        index, toolbar_width = 0, 100
        for line in PACKAGE_TXT.splitlines():
            index += 1
            if index == toolbar_width:
                sys.stdout.write(".")
                sys.stdout.flush()
                toolbar_width += 100
                time.sleep(0.05)
            if line.startswith("PACKAGE NAME"):
                package_name.append(line.replace("PACKAGE NAME:  ", ""))
            if line.startswith("PACKAGE LOCATION"):
                package_location.append(line.replace("PACKAGE LOCATION:  ./", ""))
        for loc, name in zip(package_location, package_name):
            dwn_list.append("{0}{1}/{2}".format(mirrors("",""), loc, name))
        for pkg in package_name:
            installed_pkg = "".join(find_package(pkg.replace(".txz", ""), pkg_path))
            if installed_pkg == "":
                upgrade_all.append(pkg)
        sys.stdout.write("Done\n")
        if upgrade_all:
            print("\nThese packages need upgrading:\n")
            for upgrade in upgrade_all:
                print("{0}[ upgrade ] --> {1}{2}".format(
                        colors.GREEN, colors.ENDC, upgrade))
                for dwn in dwn_list:
                    if upgrade in dwn:
                        dwn_patches.append(dwn)
            read = raw_input("\nWould you like to upgrade [Y/n]? ")
            if read == "Y" or read == "y":
                for dwn in dwn_patches:
                    subprocess.call("wget -N --directory-prefix={0} {1}".format(
                               pch_path, dwn), shell=True)
                for pkg in upgrade_all:
                    print("{0}[ upgrading ] --> {1}{2}".format(
                            colors.GREEN, colors.ENDC, pkg))
                    pkg_upgrade((pch_path + pkg).split())
                for kernel in upgrade_all:
                    if "kernel" in kernel:
                        print("The kernel has been upgraded, reinstall `lilo` ...")
                        subprocess.call("lilo", shell=True)
                        break
                read = raw_input("Removal downloaded packages [Y/n]? ")
                if read == "Y" or read == "y":
                    for pkg in upgrade_all:
                        os.remove(pch_path + pkg)
                    if os.listdir(pch_path) == []:
                        print("Packages removed")
                    else:
                        print("\nThere are packages in direcrory {0}\n".format(
                                pch_path))
                else:
                    print("\nThere are packages in directory {0}\n".format(                                                        pch_path))
        else:
            if arch == "x86_64":
                slack_arch = 64
            else:
                slack_arch = ""
            print("\nSlackware{0} v{1} distribution is up to date\n".format(
                    slack_arch, slack_ver()))
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
