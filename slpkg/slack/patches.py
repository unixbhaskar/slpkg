#!/usr/bin/python
# -*- coding: utf-8 -*-

# patches.py file is part of slpkg.

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
import subprocess

from colors import colors
from url_read import url_read
from messages import template
from __metadata__ import (pkg_path, slpkg_tmp, 
                            slack_archs)

from pkg.manager import pkg_upgrade

from mirrors import mirrors
from slack_version import slack_ver

def patches():
    '''
    Install new patches from official Slackware mirrors
    '''
    try:
        comp_sum, uncomp_sum = [], []
        dwn_patches, comp_size, uncomp_size = [], [], []
        upgrade_all, package_name, package_location = [], [], []
        GREEN, RED, ENDC = colors.GREEN, colors.RED, colors.ENDC
        patch_path = slpkg_tmp + "patches/"
        slack_arch = ""
        if not os.path.exists(slpkg_tmp):
            os.mkdir(slpkg_tmp)
        if not os.path.exists(patch_path):
            os.mkdir(patch_path)
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
		        package_name.append(line[15:].strip())
            if line.startswith("PACKAGE LOCATION"):
		        package_location.append(line[21:].strip())
            if line.startswith("PACKAGE SIZE (compressed):  "):
                comp_size.append(line[28:-2].strip())
            if line.startswith("PACKAGE SIZE (uncompressed):  "):
                uncomp_size.append(line[30:-2].strip())
        for loc, name, comp, uncomp in zip(package_location, package_name, comp_size, uncomp_size):
            if not os.path.isfile(pkg_path + name[:-4]):
                dwn_patches.append("{0}{1}/{2}".format(mirrors("",""), loc, name))
                comp_sum.append(comp)
                uncomp_sum.append(uncomp)
                upgrade_all.append(name)
        sys.stdout.write("Done\n")
        if upgrade_all:
            print("\nThese packages need upgrading:\n")
            template(78)
            print "| Package",  " " * 33, "Arch", " " * 3, "Build", " ", "Repos", " ", "Size"
            template(78)
            print("Upgrading:")
            for upgrade, size in zip(upgrade_all, comp_sum):
                for archs in slack_archs:
                    if archs in upgrade:
                        upg = upgrade.replace(archs, "")
                        arch = archs[1:-1]
                if "_slack" in upgrade:
                    slack = "_slack" + slack_ver()
                else:
                    slack = ""
                print " " , GREEN + upg[:-(5+len(slack))] + ENDC, \
                      " " * (40-len(upg[:-(5+len(slack))])), arch, \
                      " " * (7-len(arch)), upg[-(5+len(slack)):-(4+len(slack))], \
                      " " * (6-len(upg[-(5+len(slack)):-(4+len(slack))])), "Slack", \
                      " " , size, " " * (3-len(size)), "K"
            comp_unit, uncomp_unit = "Mb", "Mb"
            compressed = round((sum(map(float, comp_sum)) / 1024), 2)
            uncompressed = round((sum(map(float, uncomp_sum)) / 1024), 2)
            if compressed < 1:
                compressed = sum(map(int, comp_sum))
                comp_unit = "Kb"
            if uncompressed < 1:
                uncompressed = sum(map(int, uncomp_sum))
                uncomp_unit = "Kb"
            msg_pkg = "package"
            if len(upgrade_all) > 1:
                msg_pkg = msg_pkg + "s"
            print("\nInstalling summary")
            print("=" * 79)
            print("Total {0} {1} will be upgraded.".format(len(upgrade_all), msg_pkg))
            print("Need to get {0} {1} of archives.".format(compressed, comp_unit))
            print("After this process, {0} {1} of additional disk space will be used.".format(
                  uncompressed, uncomp_unit))
            read = raw_input("\nWould you like to upgrade [Y/n]? ")
            if read == "Y" or read == "y":
                for dwn in dwn_patches:
                    subprocess.call("wget -N --directory-prefix={0} {1} {2}.asc".format(
                                    patch_path, dwn, dwn), shell=True)
                for pkg in upgrade_all:
                    print("{0}[ upgrading ] --> {1}{2}".format(GREEN, ENDC, pkg[:-4]))
                    pkg_upgrade((patch_path + pkg).split())
                for kernel in upgrade_all:
                    if "kernel" in kernel:
                        print("The kernel has been upgraded, reinstall `lilo` ...")
                        subprocess.call("lilo", shell=True)
                        break
                print("Completed!\n")
                read = raw_input("Removal downloaded packages [Y/n]? ")
                if read == "Y" or read == "y":
                    for pkg in upgrade_all:
                        os.remove(patch_path + pkg)
                        os.remove(patch_path + pkg + ".asc")
                    if os.listdir(patch_path) == []:
                        print("Packages removed")
                    else:
                        print("\nThere are packages in direcrory {0}\n".format(patch_path))
                else:
                    print("\nThere are packages in directory {0}\n".format(patch_path))
        else:
            if os.uname()[4] == "x86_64":
                slack_arch = 64
            print("\nSlackware{0} v{1} distribution is up to date\n".format(
                  slack_arch, slack_ver()))
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
