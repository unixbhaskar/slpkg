#!/usr/bin/python
# -*- coding: utf-8 -*-

# manager.py file is part of slpkg.

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

from slpkg.messages import pkg_not_found, template
from slpkg.colors import RED, GREEN, CYAN, GREY, ENDC
from slpkg.__metadata__ import pkg_path, sp, log_path

from find import find_package


class PackageManager(object):
    '''
    Package manager class for install, upgrade,
    reinstall, remove, find and display packages.
    '''

    def __init__(self, binary):
        self.binary = binary

    def install(self):
        '''
        Install Slackware binary packages
        '''
        for pkg in self.binary:
            try:
                print(subprocess.check_output("installpkg {0}".format(
                                              pkg), shell=True))
                print("Completed!\n")
            except subprocess.CalledProcessError:
                message = "Can't install"
                if len(self.binary) > 1:
                    bol = eol = ""
                else:
                    bol = eol = "\n"
                pkg_not_found(bol, pkg, message, eol)

    def upgrade(self):
        '''
        Upgrade Slackware binary packages
        '''
        for pkg in self.binary:
            try:
                print(subprocess.check_output("upgradepkg --install-new "
                                              "{0}".format(pkg), shell=True))
                print("Completed!\n")
            except subprocess.CalledProcessError:
                message = "Can't upgrade"
                if len(self.binary) > 1:
                    bol = eol = ""
                else:
                    bol = eol = "\n"
                pkg_not_found(bol, pkg, message, eol)

    def reinstall(self):
        '''
        Reinstall Slackware binary packages
        '''
        for pkg in self.binary:
            try:
                print(
                    subprocess.check_output("upgradepkg --reinstall {0}".format(
                        pkg), shell=True))
                print("Completed!\n")
            except subprocess.CalledProcessError:
                message = "Can't reinstall"
                if len(self.binary) > 1:
                    bol = eol = ""
                else:
                    bol = eol = "\n"
                pkg_not_found(bol, pkg, message, eol)

    def remove(self):
        '''
        Remove Slackware binary packages
        '''
        dep_path = log_path + "dep/"
        [removed,
         dependencies,
         rmv_list,
         ] = ([] for i in range(3))
        print("\nPackages with name matching [ {0}{1}{2} ]\n".format(
              CYAN, ", ".join(self.binary), ENDC))
        for pkg in self.binary:
            pkgs = find_package(pkg + sp, pkg_path)
            if pkgs:
                print("[ {0}delete{1} ] --> {2}".format(RED, ENDC,
                      "\n               ".join(pkgs)))

                removed.append(pkg)
            else:
                message = "Can't remove"
                pkg_not_found("", pkg, message, "")
        if not removed:
            print   # new line at end
        else:
            msg = "package"
            if len(removed) > 1:
                msg = msg + "s"
            try:
                remove_pkg = raw_input(
                    "\nAre you sure to remove {0} {1} [Y/n]? ".format(
                        str(len(removed)), msg))
            except KeyboardInterrupt:
                print   # new line at exit
                sys.exit()
            if remove_pkg == "y" or remove_pkg == "Y":
                for rmv in removed:
                    # If package build and install with 'slpkg -s sbo <package>'
                    # then look log file for dependencies in /var/log/slpkg/dep,
                    # read and remove all else remove only the package.
                    if os.path.isfile(dep_path + rmv):
                        with open(dep_path + rmv, "r") as f:
                            dependencies = f.read().split()
                            f.close()
                        print   # new line at start
                        template(78)
                        print("| Found dependencies for package {0}:".format(
                            rmv))
                        template(78)
                        # Prints dependecies before removed except master
                        # package because referred as master package
                        for dep in dependencies[:-1]:
                            print("| {0}{1}{2}".format(RED, dep, ENDC))
                        template(78)
                        try:
                            remove_dep = raw_input(
                                "\nRemove dependencies (maybe used by other "
                                "packages) [Y/n]? ")
                        except KeyboardInterrupt:
                            print  # new line at exit
                            sys.exit()
                        if remove_dep == "y" or remove_dep == "Y":
                            for dep in dependencies:
                                if find_package(dep + sp, pkg_path):
                                    print(subprocess.check_output(
                                        "removepkg {0}".format(dep),
                                        shell=True))
                                    rmv_list.append(dep)
                            os.remove(dep_path + rmv)
                        else:
                            if find_package(rmv + sp, pkg_path):
                                print(subprocess.check_output(
                                    "removepkg {0}".format(rmv),
                                    shell=True))
                                rmv_list.append(rmv)
                            f.close()
                            os.remove(dep_path + rmv)
                    else:
                        if find_package(rmv + sp, pkg_path):
                            print(subprocess.check_output(
                                "removepkg {0}".format(rmv),
                                shell=True))
                            rmv_list.append(rmv)
                # Prints all removed packages
                if len(rmv_list) > 1:
                    template(78)
                    print("| Total {0} packages removed".format(len(rmv_list)))
                template(78)
                for pkg in rmv_list:
                    if not find_package(pkg + sp, pkg_path):
                        print("| Package {0} removed".format(pkg))
                    else:
                        print("| Package {0} not found".format(pkg))
                template(78)
            print   # new line at end

    def find(self):
        '''
        Find installed Slackware packages
        '''
        self.binary = "".join(self.binary)
        matching = size = 0
        print("\nPackages with matching name [ {0}{1}{2} ]\n".format(
              CYAN, self.binary, ENDC))
        for match in find_package(self.binary, pkg_path):
            if self.binary in match:
                matching += 1
                print("[ {0}installed{1} ] - {2}".format(
                      GREEN, ENDC, match))
                with open(pkg_path + match, "r") as f:
                    data = f.read()
                    f.close()
                for line in data.splitlines():
                    if line.startswith("UNCOMPRESSED PACKAGE SIZE:"):
                        if "M" in line[26:]:
                            size += float(line[26:-1]) * 1024
                        else:
                            size += float(line[26:-1])
                        break
        if matching == 0:
            message = "Can't find"
            pkg_not_found("", self.binary, message, "\n")
        else:
            print("\n{0}Total found {1} matching packages.{2}".format(
                  GREY, matching, ENDC))
            unit = "Kb"
            if size > 1024:
                unit = "Mb"
                size = (size / 1024)
            print("{0}Size of installed packages {1} {2}.{3}\n".format(
                  GREY, round(size, 2), unit, ENDC))

    def display(self):
        '''
        Print the Slackware packages contents
        '''
        for pkg in self.binary:
            find = find_package(pkg + sp, pkg_path)
            if find:
                with open(pkg_path + "".join(find), "r") as package:
                    for line in package:
                        print(line).strip()
                    print   # new line per file
            else:
                message = "Can't dislpay"
                if len(self.binary) > 1:
                    bol = eol = ""
                else:
                    bol = eol = "\n"
                pkg_not_found(bol, pkg, message, eol)

    def list(self, pattern):
        '''
        List with the installed packages
        '''
        try:
            if "sbo" in pattern:
                search = "_SBo"
            elif "slack" in pattern:
                search = "_slack"
            elif "noarch" in pattern:
                search = "-noarch-"
            elif "all" in pattern:
                search = ""
            index, page = 0, 50
            for pkg in find_package("", pkg_path):
                if search in pkg:
                    index += 1
                    print("{0}{1}:{2} {3}".format(GREY, index, ENDC, pkg))
                    if index == page:
                        print   # new line at start
                        raw_input("Press [ {0}Enter{1} ] >> Next page ".format(
                            CYAN, ENDC))
                        page += 50
            print   # new line at end
        except KeyboardInterrupt:
            print   # new line at exit
            sys.exit()
