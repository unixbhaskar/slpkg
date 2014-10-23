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


def install(slack_pkg, version):
    '''
    Install packages from official Slackware distribution
    '''
    try:
        var = {
            'done': "{0}Done{1}\n".format(GREY, ENDC),
            'reading_lists': "{0}Reading package lists ...{1}".format(GREY,
                                                                      ENDC),
            'comp_sum': [],
            'uncomp_sum': [],
            'comp_size': [],
            'uncomp_size': [],
            'install_all': [],
            'package_name': [],
            'package_location': [],
            'names': [],
            'dwn_list': [],
            'pkg_sum': 0,
            'uni_sum': 0,
            'upg_sum': 0,
            'index': 0,
            'toolbar_width': 800,
            'tmp_path': slpkg_tmp + "packages/",
        }
        init(var['tmp_path'])
        print("\nPackages with name matching [ {0}{1}{2} ]\n".format(
              CYAN, slack_pkg, ENDC))
        sys.stdout.write(var['reading_lists'])
        sys.stdout.flush()
        PACKAGES = url_read(mirrors("PACKAGES.TXT", "", version))
        EXTRA = url_read(mirrors("PACKAGES.TXT", "extra/", version))
        PASTURE = url_read(mirrors("PACKAGES.TXT", "pasture/", version))
        PACKAGES_TXT = PACKAGES + EXTRA + PASTURE
        for line in PACKAGES_TXT.splitlines():
            var['index'] += 1
            if var['index'] == var['toolbar_width']:
                sys.stdout.write("{0}.{1}".format(GREY, ENDC))
                sys.stdout.flush()
                var['toolbar_width'] += 800
                time.sleep(0.00888)
            if line.startswith("PACKAGE NAME"):
                var['package_name'].append(line[15:].strip())
            if line.startswith("PACKAGE LOCATION"):
                var['package_location'].append(line[21:].strip())
            if line.startswith("PACKAGE SIZE (compressed):  "):
                var['comp_size'].append(line[28:-2].strip())
            if line.startswith("PACKAGE SIZE (uncompressed):  "):
                var['uncomp_size'].append(line[30:-2].strip())
        for loc, name, comp, uncomp in zip(var['package_location'],
                                           var['package_name'],
                                           var['comp_size'],
                                           var['uncomp_size']):
            if slack_pkg in name and slack_pkg not in BlackList().packages():
                var['dwn_list'].append("{0}{1}/{2}".format(
                    mirrors("", "", version), loc, name))
                var['install_all'].append(name)
                var['comp_sum'].append(comp)
                var['uncomp_sum'].append(uncomp)
        sys.stdout.write(var['done'] + "\n")
        if var['install_all']:
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
            for pkg, comp in zip(var['install_all'], var['comp_sum']):
                pkg_split = split_package(pkg[:-4])
                var['names'].append(pkg_split[0])
                if os.path.isfile(pkg_path + pkg[:-4]):
                    var['pkg_sum'] += 1
                    COLOR = GREEN
                elif find_package(name + "-", pkg_path):
                    COLOR = YELLOW
                    var['upg_sum'] += 1
                else:
                    COLOR = RED
                    var['uni_sum'] += 1
                print(" {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11:>12}{12}".format(
                    COLOR, pkg_split[0], ENDC,
                    " " * (25-len(pkg_split[0])), pkg_split[1],
                    " " * (19-len(pkg_split[1])), pkg_split[2],
                    " " * (8-len(pkg_split[2])), pkg_split[3],
                    " " * (7-len(pkg_split[3])), "Slack",
                    comp, " K"))
            compressed = round((sum(map(float, var['comp_sum'])) / 1024), 2)
            uncompressed = round((sum(map(float, var['uncomp_sum'])) / 1024), 2)
            if compressed > 1024:
                compressed = round((compressed / 1024), 2)
                comp_unit = "Gb"
            if uncompressed > 1024:
                uncompressed = round((uncompressed / 1024), 2)
                uncomp_unit = "Gb"
            if compressed < 1:
                compressed = sum(map(int, var['comp_sum']))
                comp_unit = "Kb"
            if uncompressed < 1:
                uncompressed = sum(map(int, var['uncomp_sum']))
                uncomp_unit = "Kb"
            msg_pkg = "package"
            msg_2_pkg = msg_pkg
            if len(var['install_all']) > 1:
                msg_pkg = msg_pkg + "s"
            if var['uni_sum'] > 1:
                msg_2_pkg = msg_2_pkg + "s"
            print("\nInstalling summary")
            print("=" * 79)
            print("{0}Total {1} {2}.".format(GREY, len(var['install_all']),
                                             msg_pkg))
            print("{0} {1} will be installed, {2} will be upgraded and {3} "
                  "will be resettled.".format(var['uni_sum'], msg_2_pkg,
                                              var['upg_sum'], var['pkg_sum']))
            print("Need to get {0} {1} of archives.".format(compressed,
                                                            comp_unit))
            print("After this process, {0} {1} of additional disk space will "
                  "be used.{2}".format(uncompressed, uncomp_unit, ENDC))
            read = raw_input("\nWould you like to install [Y/n]? ")
            if read == "Y" or read == "y":
                for dwn in var['dwn_list']:
                    Download(var['tmp_path'], dwn).start()
                    Download(var['tmp_path'], dwn + ".asc").start()
                for install, name in zip(var['install_all'], var['names']):
                    package = ((var['tmp_path'] + install).split())
                    if os.path.isfile(pkg_path + install[:-4]):
                        print("[ {0}reinstalling{1} ] --> {2}".format(
                              GREEN, ENDC, install))
                        PackageManager(package).reinstall()
                    elif find_package(name + "-", pkg_path):
                        print("[ {0}upgrading{1} ] --> {2}".format(
                              YELLOW, ENDC, install))
                        PackageManager(package).upgrade()
                    else:
                        print("[ {0}installing{1} ] --> {2}".format(
                              GREEN, ENDC, install))
                        PackageManager(package).upgrade()
                read = raw_input("Removal downloaded packages [Y/n]? ")
                if read == "Y" or read == "y":
                    for remove in var['install_all']:
                        os.remove(var['tmp_path'] + remove)
                        os.remove(var['tmp_path'] + remove + ".asc")
                    if not os.listdir(var['tmp_path']):
                        print("Packages removed")
                    else:
                        print("\nThere are packages in directory {0}\n".format(
                            var['tmp_path']))
                else:
                    print("\nThere are packages in directory {0}\n".format(
                        var['tmp_path']))
        else:
            message = "No matching"
            pkg_not_found("\n", slack_pkg, message, "\n")
    except KeyboardInterrupt:
        print   # new line at exit
        sys.exit()


def init(tmp_path):
    '''
    create directories if not exists
    '''
    if not os.path.exists(slpkg_tmp):
        os.mkdir(slpkg_tmp)
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
