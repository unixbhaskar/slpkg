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
import subprocess

from colors import colors
from functions import get_file
from __metadata__ import tmp, pkg_path, build_path, log_path, sp
from messages import pkg_not_found, pkg_found, template, build_FAILED

from pkg.find import find_package 
from pkg.build import build_package
from pkg.manager import pkg_upgrade

from init import initialization
from search import sbo_search_pkg
from file_size import server_file_size
from download import sbo_slackbuild_dwn
from dependency import sbo_dependencies_pkg
from greps import sbo_source_dwn, sbo_version_pkg

def sbo_build(name):
    '''
    Download, build and install or upgrade packages 
    with all dependencies if version is greater than
    that established.
    '''
    sys.stdout.write("Building dependency tree ...")
    initialization()
    dependencies_list = sbo_dependencies_pkg(name)
    try:
        if dependencies_list is not None:
            pkg_sum, count_upgraded, count_installed = 0, 0, 0
            arch = os.uname()[4]
            sbo_ver, pkg_arch  = [], []
            installs, upgraded, versions = [], [], []
            requires, dependencies = [], []
            PKG_COLOR, DEP_COLOR, ARCH_COLOR = "", "", ""
            ENDC = colors.ENDC
            '''
            Insert master package in list to 
            install it after dependencies
            '''
            requires.append(name)
            '''
            Create one list for all packages
            '''
            for pkg in dependencies_list:
                requires += pkg
            requires.reverse()
            '''
            Remove double dependencies
            '''
            for duplicate in requires:
                if duplicate not in dependencies:
                    dependencies.append(duplicate)
            '''
            Create two lists one for package version and one
            for package arch.
            '''
            for pkg in dependencies:
                version = sbo_version_pkg(pkg)
                sbo_ver.append(version)
                src = sbo_source_dwn(pkg)
                if arch == "x86_64":
                    pkg_arch.append("x86_64")
                elif arch.startswith("i") and arch.endswith("86"):
                    pkg_arch.append("i486")
                elif "arm" in arch:
                    pkg_arch.append("arm")
                '''
                Looks if sources unsupported or untested
                from arch
                '''
                if "UNSUPPORTED" in src:
                    pkg_arch.append("UNSUPPORTED")
                elif "UNTESTED" in src:
                    pkg_arch.append("UNTESTED")
                sbo_pkg = ("{0}-{1}".format(pkg, version))
                if find_package(sbo_pkg, pkg_path):
                    pkg_sum += 1
            sys.stdout.write("Done\n")
            '''
            Tag with color green if package already installed
            and color red if not installed. Also if package
            arch is UNSUPPORTED tag with color red and if 
            UNTESTED with color yellow.
            '''
            master_pkg = ("{0}-{1}".format(name, sbo_ver[-1]))
            if find_package(master_pkg, pkg_path):
                PKG_COLOR = colors.GREEN
            elif find_package(name + sp, pkg_path):
                PKG_COLOR = colors.YELLOW
                count_upgraded += 1    
            else:
                PKG_COLOR = colors.RED
                count_installed += 1
            if "UNSUPPORTED" in pkg_arch[-1]:
                ARCH_COLOR = colors.RED
            elif "UNTESTED" in pkg_arch[-1]:
                ARCH_COLOR = colors.YELLOW
            print("\nThe following packages will be automatically installed or upgraded")
            print("with new version:\n")
            template(78)
            print "| Package",  " " * 31, "Version",  " " * 7, "Arch", " " * 5, "Repository"
            template(78)
            print("Installing:")
            print " " , PKG_COLOR + name + ENDC, \
                  " " * (38-len(name)), sbo_ver[-1], \
                  " " * (14-len(sbo_ver[-1])), ARCH_COLOR + pkg_arch[-1] + ENDC, \
                  " " * (9-len(pkg_arch[-1])), "SBo"
            print("Installing for dependencies:")
            ARCH_COLOR = "" # reset arch color for dependencies packages
            for dep, ver, dep_arch in zip(dependencies[:-1], sbo_ver[:-1], pkg_arch[:-1]):
                dep_pkg = ("{0}-{1}".format(dep, ver))
                if find_package(dep_pkg, pkg_path):
                    DEP_COLOR = colors.GREEN
                elif find_package(dep + sp, pkg_path):
                    DEP_COLOR = colors.YELLOW
                    count_upgraded += 1
                else:
                    DEP_COLOR = colors.RED
                    count_installed += 1
                if "UNSUPPORTED" in dep_arch:
                    ARCH_COLOR = colors.RED
                elif "UNTESTED" in dep_arch:
                    ARCH_COLOR = colors.YELLOW
                print " " , DEP_COLOR + dep + ENDC, \
                      " " * (38-len(dep)), ver, \
                      " " * (14-len(ver)), ARCH_COLOR + dep_arch + ENDC, \
                      " " * (9-len(dep_arch)), "SBo"
            msg_ins = "package"
            msg_upg = msg_ins
            if count_installed > 1:
                msg_ins = msg_ins + "s"
            if msg_upg > 1:
                msg_upg = msg_upg + "s"
            print("\nInstalling summary")
            print("=" * 79)
            print("Total {0} {1}.".format(len(dependencies), msg_ins))
            print("{0} {1} will be installed, {2} allready installed and {3} {4}".format(
                 count_installed, msg_ins, pkg_sum, count_upgraded, msg_upg))
            print("will be upgraded.")
            '''
            Check if package supported by arch
            before proceed to install
            '''
            UNST = ["UNSUPPORTED", "UNTESTED"]
            for item in UNST:
                for un in pkg_arch:
                    if item == un:
                        print("\n{0}The package {1}{2}\n".format(colors.RED, item, ENDC))
                        sys.exit()
            read = raw_input("\nDo you want to continue [Y/n]? ")
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
                        src_link = sbo_source_dwn(pkg).split() 
                        script = get_file(sbo_link, "/")
                        print("\n{0}Start -->{1} {2}\n".format(colors.GREEN, ENDC, pkg))
                        subprocess.call("wget -N {0}".format(sbo_link), shell=True)
                        sources = []
                        for src in src_link:
                            subprocess.call("wget -N {0}".format(src), shell=True)
                            sources.append(get_file(src, "/"))
                        build_package(script, sources, build_path)
                        '''
                        Searches the package name and version in /tmp to install.
                        If find two or more packages e.g. to build tag 
                        2 or 3 will fit most.
                        '''
                        binary_list = []
                        for search in find_package(prgnam, tmp):
                            if "_SBo" in search:
                                binary_list.append(search)
                        try:
                            binary = (tmp + max(binary_list)).split()
                        except ValueError:
                            build_FAILED(sbo_url, prgnam)
                            sys.exit()
                        if find_package(pkg, pkg_path):
                            print("{0}[ Upgrading ] --> {1}{2}".format(
                                  colors.GREEN, ENDC, pkg))
                            upgraded.append(pkg)
                        else:
                            print("{0}[ Installing ] --> {1}{2}".format(
                                  colors.GREEN, ENDC, pkg))
                        pkg_upgrade(binary)
                        print("Complete!\n")
                        installs.append(pkg)
                        versions.append(ver)
                '''
                Reference list with packages installed
                and upgraded.
                '''
                if len(installs) > 1:
                    template(78)
                    print("| Total {0} {1} installed and {2} {3} upgraded".format(
                          count_installed, msg_ins, count_upgraded, msg_upg))
                    template(78)
                    for pkg, ver in zip(installs, versions):
                        installed = ("{0}-{1}".format(pkg, ver))
                        if find_package(installed, pkg_path):
                            if pkg in upgraded:
                                print("| Package {0} upgraded successfully".format(installed))
                            else:
                                print("| Package {0} installed successfully".format(installed))
                        else:
                            print("| Package {0} NOT installed".format(installed))
                    template(78)
                '''
                Write dependencies in a log file 
                into directory `/var/log/slpkg/dep/`
                '''
                if find_package(name + sp, pkg_path):
                    dep_path = log_path + "dep/"
                    if not os.path.exists(dep_path):
                        os.mkdir(dep_path)
                    if os.path.isfile(dep_path + name): 
                        os.remove(dep_path + name)
                    if len(dependencies) > 1:
                        f = open(dep_path + name, "w")
                        for dep in dependencies:
                            f.write(dep + "\n")
                        f.close()
        else:
            sys.stdout.write("Done\n")
            message = "From slackbuilds.org"
            pkg_not_found("\n", name, message, "\n")
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
