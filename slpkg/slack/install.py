#!/usr/bin/python
# -*- coding: utf-8 -*-

# install.py file is part of slpkg.

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
from functions import get_file
from url_read import url_read
from messages import pkg_not_found, template
from __metadata__ import slpkg_tmp, pkg_path, slack_archs

from pkg.find import find_package
from pkg.manager import pkg_upgrade, pkg_reinstall

from mirrors import mirrors
from slack_version import slack_ver

def install(slack_pkg):
    '''
    Install packages from official Slackware distribution
    '''
    try:
        pkg_sum = uni_sum = upg_sum = int()
        comp_sum, uncomp_sum, names, dwn_list, comp_size, \
        uncomp_size, install_all, package_name, \
        package_location = ([] for i in range(9))
        GREEN, GREY, ENDC = colors.GREEN, colors.GREY, colors.ENDC
        arch = COLOR = str()
        # create directories if not exist
        tmp_path = slpkg_tmp + "packages/"
        if not os.path.exists(slpkg_tmp):
            os.mkdir(slpkg_tmp)
        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)
        print("\nPackages with name matching [ {0}{1}{2} ]\n".format(
                colors.CYAN, slack_pkg, ENDC)) 
        sys.stdout.write ("{0}Reading package lists ...{1}".format(colors.GREY, ENDC))
        sys.stdout.flush()
        PACKAGES = url_read(mirrors(name="PACKAGES.TXT", location=""))
        EXTRA = url_read(mirrors(name="PACKAGES.TXT", location="extra/"))
        PASTURE = url_read(mirrors(name="PACKAGES.TXT", location="pasture/"))
        PACKAGES_TXT = PACKAGES + EXTRA + PASTURE
        index, toolbar_width = 0, 800
        for line in PACKAGES_TXT.splitlines():
            index += 1
            if index == toolbar_width:
                sys.stdout.write("{0}.{1}".format(colors.GREY, ENDC))
                sys.stdout.flush()
                toolbar_width += 800
                time.sleep(0.00888)
            if line.startswith("PACKAGE NAME"):
                package_name.append(line[15:].strip())
            if line.startswith("PACKAGE LOCATION"):
                package_location.append(line[21:].strip())
            if line.startswith("PACKAGE SIZE (compressed):  "):
                comp_size.append(line[28:-2].strip())
            if line.startswith("PACKAGE SIZE (uncompressed):  "):
                uncomp_size.append(line[30:-2].strip())
        for loc, name, comp, uncomp in zip(package_location, package_name, comp_size, uncomp_size):
            if slack_pkg in name:
                dwn_list.append("{0}{1}/{2}".format(mirrors("",""), loc, name))
                install_all.append(name)
                comp_sum.append(comp)
                uncomp_sum.append(uncomp)
        sys.stdout.write("{0}Done{1}\n\n".format(colors.GREY, ENDC))
        if install_all:
            template(78)
            print("{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(
                  "| Package", " " * 17, "Version", " " * 12, "Arch", " " * 4, \
                  "Build", " " * 2, "Repos", " " * 10, "Size"))
            template(78)
            print("Installing:")
            for pkg, comp in zip(install_all, comp_sum):
                for archs in slack_archs:
                    if archs in pkg:
                        pkgs = pkg[:-4]
                        build = get_file(pkgs, "-").replace("-", "")
                        name_ver = pkgs[:-(len(archs) + len(build))]
                        ver = get_file(name_ver, "-").replace("-", "")
                        name = name_ver[:-(len(ver) + 1)]
                        arch = archs[1:-1]
                        names.append(name)
                if os.path.isfile(pkg_path + pkg[:-4]):
                    pkg_sum += 1
                    COLOR = colors.GREEN
                elif find_package(name + "-", pkg_path):
                    COLOR = colors.YELLOW
                    upg_sum += 1
                else:
                    COLOR = colors.RED
                    uni_sum += 1
                print(" {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11:>12}{12}".format(
                      COLOR, name, ENDC, \
                      " " * (25-len(name)), ver, \
                      " " * (19-len(ver)), arch, \
                      " " * (8-len(arch)), build, \
                      " " * (7-len(build)), "Slack", \
                      comp, " K"))
            comp_unit = uncomp_unit = "Mb"
            compressed = round((sum(map(float, comp_sum)) / 1024), 2)
            uncompressed = round((sum(map(float, uncomp_sum)) / 1024), 2)
            if compressed < 1:
                compressed, comp_unit = sum(map(int, comp_sum)), "Kb"
            if uncompressed < 1:
                uncompressed, uncomp_unit = sum(map(int, uncomp_sum)), "Kb"
            msg_pkg = "package"
            msg_2_pkg = msg_pkg
            if len(install_all) > 1:
                msg_pkg = msg_pkg + "s"
            if uni_sum > 1:
                msg_2_pkg = msg_2_pkg + "s"
            print("\nInstalling summary")
            print("=" * 79)
            print("{0}Total {1} {2}.".format(GREY, len(install_all), msg_pkg))
            print("{0} {1} will be installed, {2} will be upgraded and {3} will be resettled.".format(
                 uni_sum, msg_2_pkg, upg_sum, pkg_sum))
            print("Need to get {0} {1} of archives.".format(compressed, comp_unit))
            print("After this process, {0} {1} of additional disk space will be used.{2}".format(
                  uncompressed, uncomp_unit, ENDC))
            read = raw_input("\nWould you like to install [Y/n]? ")
            if read == "Y" or read == "y":
                for dwn in dwn_list:
                    subprocess.call("wget -N --directory-prefix={0} {1} {2}.asc".format(
                                    tmp_path, dwn, dwn), shell=True)
                for install, name in zip(install_all, names):
                    if os.path.isfile(pkg_path + install[:-4]):
                        print("{0}[ reinstalling ] --> {1}{2}".format(
                              GREEN, ENDC, install))
                        pkg_reinstall((tmp_path + install).split())
                    elif find_package(name + "-", pkg_path):
                        print("{0}[ upgrading ] --> {1}{2}".format(
                              GREEN, ENDC, install))
                        pkg_upgrade((tmp_path + install).split())
                    else:
                        print("{0}[ installing ] --> {1}{2}".format(
                              GREEN, ENDC, install))
                        pkg_upgrade((tmp_path + install).split())
                print("Completed!\n")
                read = raw_input("Removal downloaded packages [Y/n]? ")
                if read == "Y" or read == "y":
                    for remove in install_all:
                        os.remove(tmp_path + remove)
                        os.remove(tmp_path + remove + ".asc")
                    if os.listdir(tmp_path) == []:
                        print("Packages removed")
                    else:
                        print("\nThere are packages in directory {0}\n".format(tmp_path))
                else:
                    print("\nThere are packages in directory {0}\n".format(tmp_path))
        else:
            message = "No matching"
            pkg_not_found("", slack_pkg, message, "\n")
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
