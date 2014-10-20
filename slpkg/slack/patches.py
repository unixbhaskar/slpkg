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

from slpkg.url_read import url_read
from slpkg.messages import template
from slpkg.downloader import Download
from slpkg.blacklist import BlackList
from slpkg.splitting import split_package
from slpkg.colors import GREY, YELLOW, ENDC
from slpkg.__metadata__ import pkg_path, slpkg_tmp

from slpkg.pkg.manager import PackageManager

from mirrors import mirrors
from slack_version import slack_ver


def patches(version):
    '''
    Install new patches from official Slackware mirrors
    '''
    try:
        done = "{0}Done{1}\n".format(GREY, ENDC)
        reading_lists = "{0}Reading package lists ...{1}".format(GREY, ENDC)
        [
            comp_sum,
            uncomp_sum,
            dwn_patches,
            comp_size,
            uncomp_size,
            upgrade_all,
            package_name,
            package_location
        ] = ([] for i in range(8))
        slack_arch = ""
        patch_path = slpkg_tmp + "patches/"
        if not os.path.exists(slpkg_tmp):
            os.mkdir(slpkg_tmp)
        if not os.path.exists(patch_path):
            os.mkdir(patch_path)
        sys.stdout.write(reading_lists)
        sys.stdout.flush()
        blacklist = BlackList().packages()
        if version == "stable":
            PACKAGE_TXT = url_read(mirrors("PACKAGES.TXT", "patches/", version))
            step = 100
        else:
            PACKAGE_TXT = url_read(mirrors("PACKAGES.TXT", "", version))
            step = 700
        index, toolbar_width = 0, step
        for line in PACKAGE_TXT.splitlines():
            index += 1
            if index == toolbar_width:
                sys.stdout.write("{0}.{1}".format(GREY, ENDC))
                sys.stdout.flush()
                toolbar_width += step
                time.sleep(0.05)
            if line.startswith("PACKAGE NAME"):
                package_name.append(line[15:].strip())
            if line.startswith("PACKAGE LOCATION"):
                package_location.append(line[21:].strip())
            if line.startswith("PACKAGE SIZE (compressed):  "):
                comp_size.append(line[28:-2].strip())
            if line.startswith("PACKAGE SIZE (uncompressed):  "):
                uncomp_size.append(line[30:-2].strip())
        if version == "stable":    # stables versions upgrade
            for loc, name, comp, uncomp in zip(package_location, package_name,
                                               comp_size, uncomp_size):
                if (not os.path.isfile(pkg_path + name[:-4]) and split_package(
                        name)[0] not in blacklist):
                    dwn_patches.append("{0}{1}/{2}".format(
                        mirrors("", "", version), loc, name))
                    comp_sum.append(comp)
                    uncomp_sum.append(uncomp)
                    upgrade_all.append(name)
        else:   # current version upgrade
            installed = []
            # get all installed packages and store the package name.
            for pkg in os.listdir(pkg_path):
                installed.append(split_package(pkg)[0])
            for loc, name, comp, uncomp in zip(package_location, package_name,
                                               comp_size, uncomp_size):
                # If the package from the current repository is installed
                # (check with the name) but not is in the path (check with
                # all package like 'apr-1.5.0-x86_64-1') then add to list for
                # upgrade.
                # etc. 'apr' in list 'installed' ?? if yes 'apr-1.5.0-x86_64-1'
                # exist in /var/log/packages ?? if no add to upgrade.
                if split_package(name)[0] in installed:
                    if (not os.path.isfile(pkg_path + name[:-4]) and
                            split_package(name)[0] not in blacklist):
                        dwn_patches.append("{0}{1}/{2}".format(
                            mirrors("", "", version), loc, name))
                        comp_sum.append(comp)
                        uncomp_sum.append(uncomp)
                        upgrade_all.append(name)
        sys.stdout.write(done)
        if upgrade_all:
            print("\nThese packages need upgrading:\n")
            template(78)
            print("{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(
                "| Package", " " * 17,
                "Version", " " * 12,
                "Arch", " " * 4,
                "Build", " " * 2,
                "Repos", " " * 10,
                "Size"))
            template(78)
            print("Upgrading:")
            for upgrade, size in zip(upgrade_all, comp_sum):
                pkg_split = split_package(upgrade[:-4])
                name = pkg_split[0]
                ver = pkg_split[1]
                arch = pkg_split[2]
                build = pkg_split[3]
                print(" {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11:>12}{12}".format(
                    YELLOW, name, ENDC,
                    " " * (25-len(name)), ver,
                    " " * (19-len(ver)), arch,
                    " " * (8-len(arch)), build,
                    " " * (7-len(build)), "Slack",
                    size, " K"))
            comp_unit = uncomp_unit = "Mb"
            compressed = round((sum(map(float, comp_sum)) / 1024), 2)
            uncompressed = round((sum(map(float, uncomp_sum)) / 1024), 2)
            if compressed > 1024:
                compressed = round((compressed / 1024), 2)
                comp_unit = "Gb"
            if uncompressed > 1024:
                uncompressed = round((uncompressed / 1024), 2)
                uncomp_unit = "Gb"
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
            print("{0}Total {1} {2} will be upgraded.".format(GREY,
                                                              len(upgrade_all),
                                                              msg_pkg))
            print("Need to get {0} {1} of archives.".format(compressed,
                                                            comp_unit))
            print("After this process, {0} {1} of additional disk space will "
                  "be used.{2}".format(uncompressed, uncomp_unit, ENDC))
            read = raw_input("\nWould you like to upgrade [Y/n]? ")
            if read == "Y" or read == "y":
                for dwn in dwn_patches:
                    Download(patch_path, dwn).start()
                    Download(patch_path, dwn + ".asc").start()
                for pkg in upgrade_all:
                    print("[ {0}upgrading{1} ] --> {2}".format(YELLOW, ENDC,
                                                               pkg[:-4]))
                    PackageManager((patch_path + pkg).split()).upgrade()
                for kernel in upgrade_all:
                    if "kernel" in kernel:
                        print("The kernel has been upgraded, reinstall "
                              "`lilo` ...")
                        subprocess.call("lilo", shell=True)
                        break
                read = raw_input("Removal downloaded packages [Y/n]? ")
                if read == "Y" or read == "y":
                    for pkg in upgrade_all:
                        os.remove(patch_path + pkg)
                        os.remove(patch_path + pkg + ".asc")
                    if not os.listdir(patch_path):
                        print("Packages removed")
                    else:
                        print("\nThere are packages in direcrory {0}\n".format(
                            patch_path))
                else:
                    print("\nThere are packages in directory {0}\n".format(
                        patch_path))
        else:
            if os.uname()[4] == "x86_64":
                slack_arch = 64
            print(
                "\nSlackware{0} '{1}' v{2} distribution is up to date\n".format(
                    slack_arch, version, slack_ver()))
    except KeyboardInterrupt:
        print   # new line at exit
        sys.exit()
