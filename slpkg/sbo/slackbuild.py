#!/usr/bin/python
# -*- coding: utf-8 -*-

# slackbuild.py file is part of slpkg.

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

from init import initialization
from downloader import Download
from splitting import split_package
from __metadata__ import (tmp, pkg_path, build_path,
                          log_path, lib_path, sp)
from colors import RED, GREEN, GREY, YELLOW, CYAN, ENDC
from messages import (pkg_found, template, build_FAILED,
                      pkg_not_found)

from pkg.find import find_package
from pkg.build import build_package
from pkg.manager import PackageManager

from greps import SBoGrep
from search import sbo_search_pkg
from download import sbo_slackbuild_dwn
from dependency import sbo_dependencies_pkg


class SlackBuild(object):
    '''
    Download, build and install or upgrade packages
    with all dependencies if version is greater than
    that established.
    '''
    def __init__(self, name):
        self.name = name
        self.sbo_ver = []
        self.pkg_arch = []
        self.installs = []
        self.upgraded = []
        self.versions = []
        self.requires = []
        self.dependencies = []
        self.pkg_sum = 0
        self.done = "{0}Done{1}\n".format(GREY, ENDC)
        self.reading_lists = "{0}Reading package lists ...{1}".format(GREY,
                                                                      ENDC)
        initialization()

    def start(self):
        '''
        Create list with package and dependencies
        '''
        sys.stdout.write(self.reading_lists)
        sys.stdout.flush()
        dependencies_list = sbo_dependencies_pkg(self.name)
        if dependencies_list or sbo_search_pkg(self.name) is not None:
            # Insert master package in list to
            # install it after dependencies
            self.requires.append(self.name)
            # Create one list for all packages
            for pkg in dependencies_list:
                self.requires += pkg
            self.requires.reverse()
            # Remove double dependencies
            for duplicate in self.requires:
                if duplicate not in self.dependencies:
                    self.dependencies.append(duplicate)
            # Create two lists one for package version and one
            # for package arch.
            for pkg in self.dependencies:
                version = SBoGrep(pkg).version()
                src = SBoGrep(pkg).source()
                self.sbo_ver.append(version)
                self.pkg_arch.append(self._select_arch(src))
                sbo_pkg = ("{0}-{1}".format(pkg, version))
                if find_package(sbo_pkg, pkg_path):
                    self.pkg_sum += 1
            sys.stdout.write(self.done)
            self._process(src)     # continue to install packages
        else:
            self._matching()    # view matching packages

    def _process(self, src):
        '''
        Continue build and install or upgrade packages with all
        dependencies.
        '''
        count_upgraded = count_installed = 0
        PKG_COLOR = DEP_COLOR = ARCH_COLOR = ""
        try:
            # Tag with color green if package already installed,
            # color yellow for packages to upgrade and color red
            # if not installed. Also if package arch is UNSUPPORTED
            # tag with color red and if UNTESTED with color yellow.
            master_pkg = ("{0}-{1}".format(self.name, self.sbo_ver[-1]))
            if find_package(master_pkg, pkg_path):
                PKG_COLOR = GREEN
            elif find_package(self.name + sp, pkg_path):
                PKG_COLOR = YELLOW
                count_upgraded += 1
            else:
                PKG_COLOR = RED
                count_installed += 1
            if "UNSUPPORTED" in self.pkg_arch[-1]:
                ARCH_COLOR = RED
            elif "UNTESTED" in self.pkg_arch[-1]:
                ARCH_COLOR = YELLOW
            print("\nThe following packages will be automatically "
                  "installed or upgraded")
            print("with new version:\n")
            self._view_top()
            print("Installing:")
            self._view_packages(PKG_COLOR, self.name, self.sbo_ver[-1],
                                ARCH_COLOR, self.pkg_arch[-1])
            print("Installing for dependencies:")
            ARCH_COLOR = ""     # reset arch color for dependencies packages
            for dep, ver, dep_arch in zip(self.dependencies[:-1],
                                          self.sbo_ver[:-1],
                                          self.pkg_arch[:-1]):
                dep_pkg = ("{0}-{1}".format(dep, ver))
                if find_package(dep_pkg, pkg_path):
                    DEP_COLOR = GREEN
                elif find_package(dep + sp, pkg_path):
                    DEP_COLOR = YELLOW
                    count_upgraded += 1
                else:
                    DEP_COLOR = RED
                    count_installed += 1
                if "UNSUPPORTED" in dep_arch:
                    ARCH_COLOR = RED
                elif "UNTESTED" in dep_arch:
                    ARCH_COLOR = YELLOW
                self._view_packages(DEP_COLOR, dep, ver, ARCH_COLOR,
                                    dep_arch)
            msgs = self._msgs(self.dependencies, count_installed,
                              count_upgraded)
            total_msg = msgs[0]
            msg_ins = msgs[1]
            msg_upg = msgs[2]
            print("\nInstalling summary")
            print("=" * 79)
            print("{0}Total {1} {2}.".format(GREY, len(self.dependencies),
                                             total_msg))
            print("{0} {1} will be installed, {2} allready installed and "
                  "{3} {4}".format(count_installed, msg_ins, self.pkg_sum,
                                   count_upgraded, msg_upg))
            print("will be upgraded.{0}\n".format(ENDC))
            # Check if package supported or tested by arch
            # before proceed to install
            UNST = ["UNSUPPORTED", "UNTESTED"]
            if src in UNST:
                print("{0}The package {1}{2}\n".format(RED, src, ENDC))
                read = ""
            # exit if all packages already installed
            elif self.pkg_sum == len(self.dependencies):
                read = ""
            else:
                read = raw_input("Do you want to continue [Y/n]? ")
            if read == "Y" or read == "y":
                self._install(count_installed, count_upgraded, msg_ins, msg_upg)
        except KeyboardInterrupt:
            print   # new line at exit
            sys.exit()

    def _install(self, count_installed, count_upgraded, msg_ins, msg_upg):
        '''
        Build and install package with all dependencies
        '''
        if not os.path.exists(build_path):
            os.mkdir(build_path)
        os.chdir(build_path)
        try:
            for pkg, ver in zip(self.dependencies, self.sbo_ver):
                prgnam = ("{0}-{1}".format(pkg, ver))
                sbo_file = "".join(find_package(prgnam, pkg_path))
                if sbo_file:
                    sbo_file_version = split_package(sbo_file)[-3]
                    template(78)
                    pkg_found(pkg, sbo_file_version)
                    template(78)
                else:
                    sbo_url = sbo_search_pkg(pkg)
                    sbo_link = sbo_slackbuild_dwn(sbo_url)
                    src_link = SBoGrep(pkg).source().split()
                    script = sbo_link.split("/")[-1]
                    Download(build_path, sbo_link).start()
                    sources = []
                    for src in src_link:
                        # get file from source
                        sources.append(src.split("/")[-1])
                        Download(build_path, src).start()
                    build_package(script, sources, build_path)
                    # Searches the package name and version in /tmp to
                    # install. If find two or more packages e.g.
                    # to build tag 2 or 3 will fit most.
                    binary_list = []
                    for search in find_package(prgnam, tmp):
                        if "_SBo" in search:
                            binary_list.append(search)
                    try:
                        binary = (tmp + max(binary_list)).split()
                    except ValueError:
                        build_FAILED(sbo_url, prgnam)
                        sys.exit()
                    if find_package(pkg + sp, pkg_path):
                        print("[ {0}Upgrading{1} ] --> {2}".format(
                              YELLOW, ENDC, pkg))
                        self.upgraded.append(pkg)
                    else:
                        print("[ {0}Installing{1} ] --> {2}".format(
                              GREEN, ENDC, pkg))
                    PackageManager(binary).upgrade()
                    self.installs.append(pkg)
                    self.versions.append(ver)
            # Reference list with packages installed
            # and upgraded.
            if len(self.installs) > 1:
                self._reference(count_installed, count_upgraded, msg_ins,
                                msg_upg)
                self._write_log(self.dependencies)
        except KeyboardInterrupt:
            print   # new line at exit
            sys.exit()

    def _matching(self):
        '''
        If the search packages failed then first searches for
        matching packages.
        '''
        ins = uns = 0
        sbo_matching = []
        index, toolbar_width = 0, 3
        with open(lib_path + "sbo_repo/SLACKBUILDS.TXT",
                  "r") as SLACKBUILDS_TXT:
            for line in SLACKBUILDS_TXT:
                if line.startswith("SLACKBUILD NAME: "):
                    sbo_name = line[17:].strip()
                    if self.name in sbo_name:
                        index += 1
                        if index == toolbar_width:
                            sys.stdout.write("{0}.{1}".format(GREY, ENDC))
                            sys.stdout.flush()
                            toolbar_width += 6
                        sbo_matching.append(sbo_name)
                        self.sbo_ver.append(SBoGrep(sbo_name).version())
                        src = SBoGrep(sbo_name).source()
                        self.pkg_arch.append(self._select_arch(src))
            SLACKBUILDS_TXT.close()
        sys.stdout.write(self.done)
        if sbo_matching:
            print("\nPackages with name matching [ {0}{1}{2} ]"
                  "\n".format(CYAN, self.name, ENDC))
            self._view_top()
            print("Matching:")
            ARCH_COLOR = ""
            for match, ver, march in zip(sbo_matching, self.sbo_ver,
                                         self.pkg_arch):
                if find_package(match + sp + ver, pkg_path):
                    self._view_packages(GREEN, match, ver, ARCH_COLOR, march)
                    ins += 1
                else:
                    self._view_packages(RED, match, ver, ARCH_COLOR, march)
                    uns += 1
            msgs = self._msgs(sbo_matching, ins, uns)
            total_msg = msgs[0]
            ins_msg = msgs[1]
            uns_msg = msgs[2]
            print("\nInstalling summary")
            print("=" * 79)
            print("{0}Total found {1} matching {2}.".format(
                  GREY, len(sbo_matching), total_msg))
            print("{0} installed {1} and {2} uninstalled {3}.{4}"
                  "\n".format(ins, ins_msg, uns, uns_msg, ENDC))
        else:
            message = "No matching"
            pkg_not_found("\n", self.name, message, "\n")

    def _msgs(self, packages, ins, uns):
        '''
        Count packages and print `packages` or
        `package`.
        '''
        total_msg = ins_msg = uns_msg = "package"
        if len(packages) > 1:
            total_msg = total_msg + "s"
        if ins > 1:
            ins_msg = ins_msg + "s"
        if uns > 1:
            uns_msg = uns_msg + "s"
        return [total_msg, ins_msg, uns_msg]

    def _view_top(self):
        '''
        View headers
        '''
        template(78)
        print("{0}{1}{2}{3}{4}{5}{6}".format(
            "| Package", " " * 30, "Version",
            " " * 10, "Arch", " " * 9, "Repository"))
        template(78)

    def _view_packages(self, PKG_COLOR, package, version, ARCH_COLOR, arch):
        '''
        View packages list
        '''
        print(" {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(
            PKG_COLOR, package, ENDC,
            " " * (38-len(package)), version,
            " " * (17-len(version)), ARCH_COLOR, arch, ENDC,
            " " * (13-len(arch)), "SBo"))

    def _reference(self, count_installed, count_upgraded, msg_ins, msg_upg):
        '''
        Reference list with packages installed
        and upgraded.
        '''
        if len(self.installs) > 1:
            template(78)
            print("| Total {0} {1} installed and {2} {3} "
                  "upgraded".format(count_installed, msg_ins,
                                    count_upgraded, msg_upg))
            template(78)
            for pkg, ver in zip(self.installs, self.versions):
                installed = ("{0}-{1}".format(pkg, ver))
                if find_package(installed, pkg_path):
                    if pkg in self.upgraded:
                        print("| Package {0} upgraded "
                              "successfully".format(installed))
                    else:
                        print("| Package {0} installed "
                              "successfully".format(installed))
                else:
                    print("| Package {0} NOT installed".format(installed))
            template(78)

    def _write_log(self, dependencies):
        '''
        write dependencies in a log file
        into directory `/var/log/slpkg/dep/`
        '''
        if find_package(self.name + sp, pkg_path):
            dep_path = log_path + "dep/"
            if not os.path.exists(dep_path):
                os.mkdir(dep_path)
            if os.path.isfile(dep_path + self.name):
                os.remove(dep_path + self.name)
            if len(dependencies) > 1:
                with open(dep_path + self.name, "w") as f:
                    for dep in dependencies:
                        f.write(dep + "\n")
                    f.close()

    def _select_arch(self, src):
        '''
        Looks if sources unsupported or untested
        from arch else select arch
        '''
        arch = os.uname()[4]
        support = [
            "UNSUPPORTED",
            "UNTESTED",
        ]
        if arch.startswith("i") and arch.endswith("86"):
                arch = "i486"
        for item in support:
            if item in src:
                arch = item
        return arch
