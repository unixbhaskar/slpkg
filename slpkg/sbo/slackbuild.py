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
from messages import pkg_not_found, pkg_found, template
from __metadata__ import (tmp, pkg_path, build_path, log_path, 
                          sp, build, sbo_tag, sbo_filetype)

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
    Download, build and upgrade packages with all
    dependencies
    '''
    sys.stdout.write("Building dependency tree ...")
    initialization()
    dependencies_list = sbo_dependencies_pkg(name)
    try:
        if dependencies_list is not None:
            pkg_sum = 0
            arch = os.uname()[4]
            sbo_ver, pkg_arch = [], []
            requires, dependencies = [], []
            PKG_COLOR, DEP_COLOR, ARCH_COLOR, ENDC = "", "", "", colors.ENDC
            '''
            Insert master package in list to install it after dependencies
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
                sbo_ver.append(sbo_version_pkg(pkg))
                src = sbo_source_dwn(pkg)
                if arch == "x86_64":
                    pkg_arch.append("x86_64")
                elif arch.startswith("i") and arch.endswith("86"):
                    pkg_arch.append("i486")
                elif "arm" in arch:
                    pkg_arch.append("arm")
                '''
                Looks if sources unsupported or untested from arch
                '''
                if "UNSUPPORTED" in src:
                    pkg_arch.append("UNSUPPORTED")
                elif "UNTESTED" in src:
                    pkg_arch.append("UNTESTED")
                if find_package(pkg + sp, pkg_path):
                    pkg_sum += 1
            sys.stdout.write("Done\n")
            '''
            Tag with color green if package already installed
            and color red if not installed. Also if package
            arch is UNSUPPORTED tag with color red and if 
            UNTESTED with color yellow.
            '''
            if find_package(name + sp, pkg_path):
                PKG_COLOR = colors.GREEN
            else:
                PKG_COLOR = colors.RED
            if "UNSUPPORTED" in pkg_arch[-1]:
                ARCH_COLOR = colors.RED
            elif "UNTESTED" in pkg_arch[-1]:
                ARCH_COLOR = colors.YELLOW
            print("\nThe following packages will be automatically installed or upgraded")
            print("with new version:\n")
            template(78)
            print "| Package",  " "*31, "Version",  " "*7, "Arch", " "*5, "Repository"
            template(78)
            print("Installing:")
            print " " , PKG_COLOR + name + ENDC, \
                  " " * (38-len(name)), sbo_ver[-1], \
                  " " * (14-len(sbo_ver[-1])), ARCH_COLOR + pkg_arch[-1] + ENDC, \
                  " " * (9-len(pkg_arch[-1])), "SBo"
            print("Installing for dependencies:")
            ARCH_COLOR = "" # reset arch color for dependencies packages
            for dep, ver, dep_arch in zip(dependencies[:-1], sbo_ver[:-1], pkg_arch[:-1]):
                if find_package(dep + sp, pkg_path):
                    DEP_COLOR = colors.GREEN
                else:
                    DEP_COLOR = colors.RED
                if "UNSUPPORTED" in dep_arch:
                    ARCH_COLOR = colors.RED
                elif "UNTESTED" in dep_arch:
                    ARCH_COLOR = colors.YELLOW
                print " " , DEP_COLOR + dep + ENDC, \
                      " " * (38-len(dep)), ver, \
                      " " * (14-len(ver)), ARCH_COLOR + dep_arch + ENDC, \
                      " " * (9-len(dep_arch)), "SBo"
            msg_pkg = "package"
            msg_2_pkg = msg_pkg
            if len(dependencies) > 1:
                msg_pkg = msg_pkg + "s"
            if len(dependencies) - pkg_sum > 1:
                msg_2_pkg = msg_2_pkg + "s"
            print("\nInstalling summary")
            print("="*79)
            print("Total {0} {1}.".format(len(dependencies), msg_pkg))
            print("{0} {1} will be installed, {2} allready installed.".format(
                 (len(dependencies) - pkg_sum), msg_2_pkg, pkg_sum))
            read = raw_input("\nDo you want to continue [Y/n]? ")
            if read == "Y" or read == "y":
                if not os.path.exists(build_path):
                    os.mkdir(build_path)
                os.chdir(build_path)
                for pkg in dependencies:
                    sbo_version = sbo_version_pkg(pkg)
                    sbo_file = "".join(find_package(pkg + sp, pkg_path))
                    sbo_file_version = sbo_file[len(pkg) + 1:-len(arch) - 7]
                    if sbo_version > sbo_file_version:
                        prgnam = ("{0}-{1}".format(pkg, sbo_version_pkg(pkg)))
                        sbo_url = sbo_search_pkg(pkg)
                        sbo_link = sbo_slackbuild_dwn(sbo_url)
                        src_link = sbo_source_dwn(pkg).split() 
                        script = get_file(sbo_link, "/")
                        print("\n{0}Start -->{1} {2}\n".format(colors.GREEN, colors.ENDC, pkg))
                        subprocess.call("wget -N {0}".format(sbo_link), shell=True)
                        sources = []
                        for src in src_link:
                            subprocess.call("wget -N {0}".format(src), shell=True)
                            sources.append(get_file(src, "/"))
                        build_package(script, sources, build_path)
                        '''
                        Before installing new binary package look if arch is noarch.
                        This is because some maintainers changes arch manualy.
                        '''
                        if "-noarch-" in "".join(find_package(prgnam, tmp)):
                            sbo_arch = "-noarch-"
                        else:
                            from __metadata__ import sbo_arch
                        binary = ("{0}{1}{2}{3}{4}{5}".format(
                                  tmp, prgnam, sbo_arch, build, sbo_tag, sbo_filetype).split())
                        print("{0}[ Installing ] --> {1}{2}".format(
                              colors.GREEN, colors.ENDC, pkg))
                        pkg_upgrade(binary)
                    else:
                        template(78)
                        pkg_found(pkg, sbo_file_version)
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
