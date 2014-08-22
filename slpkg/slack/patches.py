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
from slpkg.url_read import url_read
from slpkg.messages import template
from slpkg.__metadata__ import pkg_path, slpkg_tmp, sp

from slpkg.pkg.manager import pkg_upgrade

from mirrors import mirrors
from slack_version import slack_ver

def patches():
    '''
    Install new patches from official Slackware mirrors
    '''
    try:
        upgrade_all, package_name, package_location = [], [], []
        comp_list, uncomp_list, comp_sum, uncomp_sum = [], [], [], []
        dwn_list, dwn_patches, comp_size, uncomp_size = [], [], [], []
        pch_path = slpkg_tmp + "patches/"
        slack_arch = ""
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
		        package_name.append(line[15:].strip())
            if line.startswith("PACKAGE LOCATION"):
		        package_location.append(line[21:].strip())
            if line.startswith("PACKAGE SIZE (compressed):  "):
                comp_size.append(line[28:-2].strip())
            if line.startswith("PACKAGE SIZE (uncompressed):  "):
                uncomp_size.append(line[30:-2].strip())
        for loc, name in zip(package_location, package_name):
            dwn_list.append("{0}{1}/{2}".format(mirrors("",""), loc, name))
        for name, size in zip(package_name, comp_size):
            comp_list.append("{0}{1}".format(name, size))
        for name, size in zip(package_name, uncomp_size):
            uncomp_list.append("{0}{1}".format(name, size))
        for pkg in package_name:
            if not os.path.isfile(pkg_path + pkg[:-4]):
                upgrade_all.append(pkg)
        sys.stdout.write("Done\n")
        if upgrade_all:
            print("\nThese packages need upgrading:\n")
            template(78)
            print "| Package",  " "*33, "Arch", " "*3, "Build", " ", "Repos", " ", "Size"
            template(78)
            print("Upgrading:")
            for upgrade in upgrade_all:
                for size in comp_list:
                    if upgrade in size:
                        Kb = size.replace(upgrade, "")
                        if "-noarch-" in upgrade:
                            arch = "noarch"
                        elif sp+os.uname()[4]+sp in upgrade:
                            arch = os.uname()[4]
                        elif "-i486-" in upgrade:
                            arch = "i486"
                        elif "-i686-" in upgrade:
                            arch = "i686"
                        elif "-x86-" in upgrade:
                            arch = "x86"
                        elif "-fw-" in upgrade:
                            arch = "fw"
                        else:
                            arch = ""
                        if "_slack" in upgrade:
                            slack = "_slack" + slack_ver()
                        else:
                            slack = ""
                        print " ", upgrade[:-(5+len(slack))].replace(
                              sp+arch+sp, ""), " "*(40-len(upgrade[:-(
                              5+len(slack))].replace(sp+arch+sp, ""))), arch, " "*(
                              7-len(arch)), upgrade[-15:-14].replace(sp+arch+sp, ""), " "*(
                              6-len(upgrade[-15:-14].replace(sp+arch+sp, ""))), "Slack", " ", Kb, " "*(
                              3-len(Kb)), "K"
                for dwn in dwn_list:
                    if "/" + upgrade in dwn:
                        dwn_patches.append(dwn)
            for install in upgrade_all:
                for comp in comp_list:
                    if install == comp[:-(len(comp)-len(install))]:
                        comp_sum.append(comp.replace(install, ""))
                for uncomp in uncomp_list:
                    if install == uncomp[:-(len(uncomp)-len(install))]:
                        uncomp_sum.append(uncomp.replace(install, ""))
            comp_unit, uncomp_unit = "Mb", "Mb"
            compressed = round((sum(map(float, comp_sum)) * 0.0001220703125), 2)
            uncompressed = round((sum(map(float, uncomp_sum)) * 0.0001220703125), 2)
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
            print("="*79)
            print("Total {0} {1} will be upgrading.".format(len(upgrade_all), msg_pkg))
            print("Need to get {0} {1} of archives.".format(compressed, comp_unit))
            print("After this process, {0} {1} of additional disk space will be used.".format(
                   uncompressed, uncomp_unit))
            read = raw_input("\nWould you like to upgrade [Y/n]? ")
            if read == "Y" or read == "y":
                for dwn in dwn_patches:
                    subprocess.call("wget -N --directory-prefix={0} {1} {2}.asc".format(
                               pch_path, dwn, dwn), shell=True)
                for pkg in upgrade_all:
                    print("{0}[ upgrading ] --> {1}{2}".format(
                        colors.GREEN, colors.ENDC, pkg[:-4]))
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
                        os.remove(pch_path + pkg + ".asc")
                    if os.listdir(pch_path) == []:
                        print("Packages removed")
                    else:
                        print("\nThere are packages in direcrory {0}\n".format(pch_path))
                else:
                    print("\nThere are packages in directory {0}\n".format(pch_path))
        else:
            if os.uname()[4] == "x86_64":
                slack_arch = 64
            print("\nSlackware{0} v{1} distribution is up to date\n".format(
                    slack_arch, slack_ver()))
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
