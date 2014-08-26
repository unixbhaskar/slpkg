#!/usr/bin/python
# -*- coding: utf-8 -*-

# install.py

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
from slpkg.messages import pkg_not_found, template
from slpkg.__metadata__ import slpkg_tmp, pkg_path, sp

from slpkg.pkg.manager import pkg_upgrade, pkg_reinstall

from mirrors import mirrors

def install(slack_pkg):
    '''
    Install packages from official Slackware distribution
    '''
    try:
        comp_sum, uncomp_sum = [], []
        dwn_list, comp_size, uncomp_size = [], [], []
        install_all, package_name, package_location = [], [], []
        tmp_path = slpkg_tmp + "packages/"
        pkg_sum = 0
        if not os.path.exists(tmp_path):
            if not os.path.exists(slpkg_tmp):
                os.mkdir(slpkg_tmp)
                os.mkdir(tmp_path)
        print("\nPackages with name matching [ {0}{1}{2} ]\n".format(
                colors.CYAN, slack_pkg, colors.ENDC)) 
        sys.stdout.write ("Reading package lists ...")
        sys.stdout.flush()
        PACKAGE_TXT = url_read(mirrors(name="PACKAGES.TXT", location=""))
        index, toolbar_width = 0, 800
        for line in PACKAGE_TXT.splitlines():
            index += 1
            if index == toolbar_width:
                sys.stdout.write(".")
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
        sys.stdout.write("Done\n\n")
        if install_all:
            template(78)
            print "| Package",  " "*33, "Arch", " "*3, "Build", " ", "Repos", " ", "Size"
            template(78)
            print("Installing:")
            for pkg, comp in zip(install_all, comp_sum):
                if "-noarch-" in pkg:
                    arch = "noarch"
                elif "-x86_64-" in pkg:
                    arch = "x86_64"
                elif "-i386-" in pkg:
                    arch = "i386"
                elif "-i486-" in pkg:
                    arch = "i486"
                elif "-i686-" in pkg:
                    arch = "i686"
                elif "-x86-" in pkg:
                    arch = "x86"
                elif "-fw-" in pkg:
                    arch = "fw"
                else:
                    arch = ""
                if os.path.isfile(pkg_path + pkg[:-4]):
                    pkg_sum += 1
                    SC, EC = colors.GREEN, colors.ENDC
                else:
                    SC, EC = colors.RED, colors.ENDC
                print " ", SC + pkg[:-5].replace(sp+arch+sp, "") + EC, " "*(
                      40-len(pkg[:-5].replace(sp+arch+sp, ""))), arch, " "*(
                      7-len(arch)), pkg[-5:-4].replace(sp+arch+sp, ""), " "*(
                      6-len(pkg[-5:-4].replace(sp+arch+sp, ""))), "Slack", " ", comp, " "*(
                      3-len(comp)), "K"
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
            msg_2_pkg = msg_pkg
            if len(install_all) > 1:
                msg_pkg = msg_pkg + "s"
            if len(install_all) - pkg_sum > 1:
                msg_2_pkg = msg_2_pkg + "s"
            print("\nInstalling summary")
            print("="*79)
            print("Total {0} {1}.".format(len(install_all), msg_pkg))
            print("{0} {1} will be installed, {2} allready installed.".format(
                  (len(install_all) - pkg_sum), msg_2_pkg, pkg_sum))
            print("Need to get {0} {1} of archives.".format(compressed, comp_unit))
            print("After this process, {0} {1} of additional disk space will be used.".format(
                   uncompressed, uncomp_unit))
            read = raw_input("\nWould you like to install [Y/n]? ")
            if read == "Y" or read == "y":
                for dwn in dwn_list:
                    subprocess.call("wget -N --directory-prefix={0} {1} {2}.asc".format(
                                     tmp_path, dwn, dwn), shell=True)
                for install in install_all:
                    if not os.path.isfile(pkg_path + install[:-4]):
                        print("{0}[ installing ] --> {1}{2}".format(
                               colors.GREEN, colors.ENDC, install))
                        pkg_upgrade((tmp_path + install).split())
                    else:
                        print("{0}[ reinstalling ] --> {1}{2}".format(
                               colors.GREEN, colors.ENDC, install))
                        pkg_reinstall((tmp_path + install).split())
                print("Completed!\n")
                read = raw_input("Removal downloaded packages [Y/n]? ")
                if read == "Y" or read == "y":
                    for remove in install_all:
                        os.remove(tmp_path + remove)
                        os.remove(tmp_path + remove + ".asc")
                    if os.listdir(tmp_path) == []:
                        print("Packages removed")
                    else:
                        print("\nThere are packages in directory {0}\n".format(
                                tmp_path))
                else:
                    print("\nThere are packages in directory {0}\n".format(
                            tmp_path))
        else:
            bol, eol = "", "\n"
            message = "No matching"
            pkg_not_found(bol, slack_pkg, message, eol)
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
