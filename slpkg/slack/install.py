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

from url_read import url_read
from downloader import Download
from blacklist import BlackList
from splitting import split_package
from messages import pkg_not_found, template
from __metadata__ import slpkg_tmp, pkg_path
from colors import RED, GREEN, CYAN, YELLOW, GREY, ENDC

from pkg.find import find_package
from pkg.manager import PackageManager

from mirrors import mirrors


def slack_install(slack_pkg, version):
    '''
    Install packages from official Slackware distribution
    '''
    try:
        tmp_path = slpkg_tmp + "packages/"
        _init(tmp_path)
        print("\nPackages with name matching [ {0}{1}{2} ]\n".format(
              CYAN, slack_pkg, ENDC))
        sys.stdout.write("{0}Reading package lists ...{1}".format(GREY, ENDC))
        sys.stdout.flush()
        PACKAGES_TXT = _data(version)
        dwn_list, install_all, comp_sum, uncomp_sum = _greps(PACKAGES_TXT,
                                                             slack_pkg, version)
        sys.stdout.write("{0}Done{1}\n\n".format(GREY, ENDC))
        if install_all:
            template(78)
            print("{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(
                "| Package", " " * 17,
                "Version", " " * 12,
                "Arch", " " * 4,
                "Build", " " * 2,
                "Repos", " " * 10,
                "Size"))
            template(78)
            print("Installing:")
            sums = _views(install_all, comp_sum)
            unit, size = _units(comp_sum, uncomp_sum)
            msgs = _msgs(install_all, sums[2])
            print("\nInstalling summary")
            print("=" * 79)
            print("{0}Total {1} {2}.".format(GREY, len(install_all),
                                             msgs[0]))
            print("{0} {1} will be installed, {2} will be upgraded and {3} "
                  "will be resettled.".format(sums[2], msgs[1],
                                              sums[1], sums[0]))
            print("Need to get {0} {1} of archives.".format(size[0],
                                                            unit[0]))
            print("After this process, {0} {1} of additional disk space will "
                  "be used.{2}".format(size[1], unit[1], ENDC))
            read = raw_input("\nWould you like to install [Y/n]? ")
            if read == "Y" or read == "y":
                _download(tmp_path, dwn_list)
                _install(tmp_path, install_all)
                _remove(tmp_path, install_all)
        else:
            pkg_not_found("", slack_pkg, "No matching", "\n")
    except KeyboardInterrupt:
        print   # new line at exit
        sys.exit()


def _init(tmp_path):
    '''
    Create directories if not exists
    '''
    if not os.path.exists(slpkg_tmp):
        os.mkdir(slpkg_tmp)
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)


def _data(version):
    '''
    Collects and return data
    '''
    PACKAGES = url_read(mirrors("PACKAGES.TXT", "", version))
    EXTRA = url_read(mirrors("PACKAGES.TXT", "extra/", version))
    PASTURE = url_read(mirrors("PACKAGES.TXT", "pasture/", version))
    return (PACKAGES + EXTRA + PASTURE)


def _toolbar(index, width):
    '''
    Print toolbar status
    '''
    if index == width:
        sys.stdout.write("{0}.{1}".format(GREY, ENDC))
        sys.stdout.flush()
        width += 800
        time.sleep(0.00888)
    return width


def _greps(PACKAGES_TXT, slack_pkg, version):
    '''
    Grap data packages
    '''
    (pkg_name, pkg_location, size, unsize, dwn,
     install, comp_sum, uncomp_sum) = ([] for i in range(8))
    toolbar_width, index = 800, 0
    for line in PACKAGES_TXT.splitlines():
        index += 1
        toolbar_width = _toolbar(index, toolbar_width)
        if line.startswith("PACKAGE NAME"):
            pkg_name.append(line[15:].strip())
        if line.startswith("PACKAGE LOCATION"):
            pkg_location.append(line[21:].strip())
        if line.startswith("PACKAGE SIZE (compressed):  "):
            size.append(line[28:-2].strip())
        if line.startswith("PACKAGE SIZE (uncompressed):  "):
            unsize.append(line[30:-2].strip())
    for name, loc, comp, uncomp in zip(pkg_name, pkg_location,
                                       size, unsize):
        if slack_pkg in name and slack_pkg not in BlackList().packages():
            dwn.append("{0}{1}/{2}".format(mirrors("", "", version),
                                           loc, name))
            install.append(name)
            comp_sum.append(comp)
            uncomp_sum.append(uncomp)
    print dwn, install
    return [dwn, install, comp_sum, uncomp_sum]


def _views(install_all, comp_sum):
    '''
    Views packages
    '''
    pkg_sum = uni_sum = upg_sum = 0
    for pkg, comp in zip(install_all, comp_sum):
        pkg_split = split_package(pkg[:-4])
        if os.path.isfile(pkg_path + pkg[:-4]):
            pkg_sum += 1
            COLOR = GREEN
        elif find_package(pkg_split[0] + "-", pkg_path):
            COLOR = YELLOW
            upg_sum += 1
        else:
            COLOR = RED
            uni_sum += 1
        print(" {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11:>12}{12}".format(
            COLOR, pkg_split[0], ENDC,
            " " * (25-len(pkg_split[0])), pkg_split[1],
            " " * (19-len(pkg_split[1])), pkg_split[2],
            " " * (8-len(pkg_split[2])), pkg_split[3],
            " " * (7-len(pkg_split[3])), "Slack",
            comp, " K"))
    return [pkg_sum, upg_sum, uni_sum]


def _units(comp_sum, uncomp_sum):
    '''
    Calculate package size
    '''
    compressed = round((sum(map(float, comp_sum)) / 1024), 2)
    uncompressed = round((sum(map(float, uncomp_sum)) / 1024), 2)
    comp_unit = uncomp_unit = "Mb"
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
    return [comp_unit, uncomp_unit], [compressed, uncompressed]


def _msgs(install_all, uni_sum):
    msg_pkg = "package"
    msg_2_pkg = msg_pkg
    if len(install_all) > 1:
        msg_pkg = msg_pkg + "s"
    if uni_sum > 1:
        msg_2_pkg = msg_2_pkg + "s"
    return [msg_pkg, msg_2_pkg]


def _download(tmp_path, dwn_list):
    '''
    Download packages
    '''
    for dwn in dwn_list:
        Download(tmp_path, dwn).start()
        Download(tmp_path, dwn + ".asc").start()


def _install(tmp_path, install_all):
    '''
    Install or upgrade packages
    '''
    for install in zip(install_all):
        package = ((tmp_path + install).split())
        if os.path.isfile(pkg_path + install[:-4]):
            print("[ {0}reinstalling{1} ] --> {2}".format(
                  GREEN, ENDC, install))
            PackageManager(package).reinstall()
        elif find_package(split_package(install)[0] + "-", pkg_path):
            print("[ {0}upgrading{1} ] --> {2}".format(
                  YELLOW, ENDC, install))
            PackageManager(package).upgrade()
        else:
            print("[ {0}installing{1} ] --> {2}".format(
                  GREEN, ENDC, install))
            PackageManager(package).upgrade()


def _remove(tmp_path, install_all):
    '''
    Remove downloaded packages
    '''
    read = raw_input("Removal downloaded packages [Y/n]? ")
    if read == "Y" or read == "y":
        for remove in install_all:
            os.remove(tmp_path + remove)
            os.remove(tmp_path + remove + ".asc")
        if not os.listdir(tmp_path):
            print("Packages removed")
        else:
            print("\nThere are packages in directory {0}\n".format(
                tmp_path))
    else:
        print("\nThere are packages in directory {0}\n".format(
              tmp_path))
