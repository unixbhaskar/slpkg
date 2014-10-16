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

from slpkg.init import initialization
from slpkg.downloader import Download
from slpkg.__metadata__ import (tmp, pkg_path, build_path,
                                log_path, lib_path, sp)
from slpkg.colors import RED, GREEN, GREY, YELLOW, CYAN, ENDC
from slpkg.messages import (pkg_found, template, build_FAILED,
                            pkg_not_found, sbo_packages_view)


from slpkg.pkg.find import find_package
from slpkg.pkg.build import build_package
from slpkg.pkg.manager import PackageManager

from greps import SBoGrep
from search import sbo_search_pkg
from download import sbo_slackbuild_dwn
from dependency import sbo_dependencies_pkg


def sbo_build(name):
    '''
    Download, build and install or upgrade packages
    with all dependencies if version is greater than
    that established.
    '''
    done = "{0}Done{1}\n".format(GREY, ENDC)
    reading_lists = "{0}Reading package lists ...{1}".format(GREY, ENDC)
    sys.stdout.write(reading_lists)
    sys.stdout.flush()
    initialization()
    [
        sbo_ver,
        pkg_arch,
        installs,
        upgraded,
        versions,
        requires,
        dependencies
    ] = ([] for i in range(7))
    PKG_COLOR = DEP_COLOR = ARCH_COLOR = str()
    dependencies_list = sbo_dependencies_pkg(name)
    try:
        if dependencies_list or sbo_search_pkg(name) is not None:
            pkg_sum = count_upgraded = count_installed = int()
            # Insert master package in list to
            # install it after dependencies
            requires.append(name)
            # Create one list for all packages
            for pkg in dependencies_list:
                requires += pkg
            requires.reverse()
            # Remove double dependencies
            for duplicate in requires:
                if duplicate not in dependencies:
                    dependencies.append(duplicate)
            # Create two lists one for package version and one
            # for package arch.
            for pkg in dependencies:
                version = SBoGrep(pkg).version()
                sbo_ver.append(version)
                src = SBoGrep(pkg).source()
                pkg_arch.append(select_arch(src))
                sbo_pkg = ("{0}-{1}".format(pkg, version))
                if find_package(sbo_pkg, pkg_path):
                    pkg_sum += 1
            sys.stdout.write(done)
            # Tag with color green if package already installed,
            # color yellow for packages to upgrade and color red
            # if not installed. Also if package arch is UNSUPPORTED
            # tag with color red and if UNTESTED with color yellow.
            master_pkg = ("{0}-{1}".format(name, sbo_ver[-1]))
            if find_package(master_pkg, pkg_path):
                PKG_COLOR = GREEN
            elif find_package(name + sp, pkg_path):
                PKG_COLOR = YELLOW
                count_upgraded += 1
            else:
                PKG_COLOR = RED
                count_installed += 1
            if "UNSUPPORTED" in pkg_arch[-1]:
                ARCH_COLOR = RED
            elif "UNTESTED" in pkg_arch[-1]:
                ARCH_COLOR = YELLOW
            print("\nThe following packages will be automatically installed "
                  "or upgraded")
            print("with new version:\n")
            template(78)
            print("{0}{1}{2}{3}{4}{5}{6}".format(
                "| Package", " " * 30, "Version",
                " " * 10, "Arch", " " * 9, "Repository"))
            template(78)
            print("Installing:")
            sbo_packages_view(PKG_COLOR, name, sbo_ver[-1], ARCH_COLOR,
                              pkg_arch[-1])
            print("Installing for dependencies:")
            ARCH_COLOR = ""     # reset arch color for dependencies packages
            for dep, ver, dep_arch in zip(dependencies[:-1], sbo_ver[:-1],
                                          pkg_arch[:-1]):
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
                sbo_packages_view(DEP_COLOR, dep, ver, ARCH_COLOR, dep_arch)
            msg_upg = msg_ins = "package"
            if count_installed > 1:
                msg_ins = msg_ins + "s"
            if count_upgraded > 1:
                msg_upg = msg_upg + "s"
            print("\nInstalling summary")
            print("=" * 79)
            print("{0}Total {1} {2}.".format(GREY, len(dependencies), msg_ins))
            print("{0} {1} will be installed, {2} allready installed and "
                  "{3} {4}".format(count_installed, msg_ins, pkg_sum,
                                   count_upgraded, msg_upg))
            print("will be upgraded.{0}\n".format(ENDC))
            # Check if package supported or tested by arch
            # before proceed to install
            UNST = ["UNSUPPORTED", "UNTESTED"]
            if src in UNST:
                print("{0}The package {1}{2}\n".format(RED, src, ENDC))
                read = ""
            # exit if all packages already installed
            elif pkg_sum == len(dependencies):
                read = ""
            else:
                read = raw_input("Do you want to continue [Y/n]? ")
            if read == "Y" or read == "y":
                if not os.path.exists(build_path):
                    os.mkdir(build_path)
                os.chdir(build_path)
                for pkg, ver, ar in zip(dependencies, sbo_ver, pkg_arch):
                    prgnam = ("{0}-{1}".format(pkg, ver))
                    sbo_file = "".join(find_package(prgnam, pkg_path))
                    if sbo_file:
                        sbo_file_version = sbo_file[len(pkg) + 1:-len(ar) - 7]
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
                        # install. If find two or more packages e.g. to build
                        # tag 2 or 3 will fit most.
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
                            print("{0}[ Upgrading ] --> {1}{2}".format(
                                  GREEN, ENDC, pkg))
                            upgraded.append(pkg)
                        else:
                            print("{0}[ Installing ] --> {1}{2}".format(
                                  GREEN, ENDC, pkg))
                        PackageManager(binary).upgrade()
                        installs.append(pkg)
                        versions.append(ver)
                # Reference list with packages installed
                # and upgraded.
                if len(installs) > 1:
                    template(78)
                    print("| Total {0} {1} installed and {2} {3} "
                          "upgraded".format(count_installed, msg_ins,
                                            count_upgraded, msg_upg))
                    template(78)
                    for pkg, ver in zip(installs, versions):
                        installed = ("{0}-{1}".format(pkg, ver))
                        if find_package(installed, pkg_path):
                            if pkg in upgraded:
                                print("| Package {0} upgraded "
                                      "successfully".format(installed))
                            else:
                                print("| Package {0} installed "
                                      "successfully".format(installed))
                        else:
                            print("| Package {0} NOT installed".format(
                                installed))
                    template(78)
                # Write dependencies in a log file
                # into directory `/var/log/slpkg/dep/`
                if find_package(name + sp, pkg_path):
                    dep_path = log_path + "dep/"
                    if not os.path.exists(dep_path):
                        os.mkdir(dep_path)
                    if os.path.isfile(dep_path + name):
                        os.remove(dep_path + name)
                    if len(dependencies) > 1:
                        with open(dep_path + name, "w") as f:
                            for dep in dependencies:
                                f.write(dep + "\n")
                            f.close()
        else:
            ins = uns = int()
            sbo_matching = []
            index, toolbar_width = int(), 3
            with open(lib_path + "sbo_repo/SLACKBUILDS.TXT",
                      "r") as SLACKBUILDS_TXT:
                for line in SLACKBUILDS_TXT:
                    if line.startswith("SLACKBUILD NAME: "):
                        sbo_name = line[17:].strip()
                        if name in sbo_name:
                            index += 1
                            if index == toolbar_width:
                                sys.stdout.write("{0}.{1}".format(GREY, ENDC))
                                sys.stdout.flush()
                                toolbar_width += 6
                            sbo_matching.append(sbo_name)
                            sbo_ver.append(SBoGrep(sbo_name).version())
                            src = SBoGrep(sbo_name).source()
                            pkg_arch.append(select_arch(src))
            SLACKBUILDS_TXT.close()
            sys.stdout.write(done)
            if sbo_matching:
                print("\nPackages with name matching [ {0}{1}{2} ]\n".format(
                      CYAN, name, ENDC))
                template(78)
                print("{0}{1}{2}{3}{4}{5}{6}".format(
                    "| Package", " " * 30, "Version",
                    " " * 10, "Arch", " " * 9, "Repository"))
                template(78)
                print("Matching:")
                ARCH_COLOR = str()
                for match, ver, march in zip(sbo_matching, sbo_ver, pkg_arch):
                    if find_package(match + sp + ver, pkg_path):
                        sbo_packages_view(GREEN, match, ver, ARCH_COLOR, march)
                        ins += 1
                    else:
                        sbo_packages_view(RED, match, ver, ARCH_COLOR, march)
                        uns += 1
                total_msg = ins_msg = uns_msg = "package"
                if len(sbo_matching) > 1:
                    total_msg = total_msg + "s"
                if ins > 1:
                    ins_msg = ins_msg + "s"
                if uns > 1:
                    uns_msg = uns_msg + "s"
                print("\nInstalling summary")
                print("=" * 79)
                print("{0}Total found {1} matching {2}.".format(
                      GREY, len(sbo_matching), total_msg))
                print("{0} installed {1} and {2} uninstalled {3}.{4}\n".format(
                      ins, ins_msg, uns, uns_msg, ENDC))
            else:
                message = "No matching"
                pkg_not_found("\n", name, message, "\n")
    except KeyboardInterrupt:
        print   # new line at exit
        sys.exit()


def select_arch(src):
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
