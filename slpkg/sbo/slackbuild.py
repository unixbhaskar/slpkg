#!/usr/bin/python
# -*- coding: utf-8 -*-

# slackbuild.py

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
import subprocess

from slpkg.colors import colors
from slpkg.functions import get_file
from slpkg.messages import pkg_not_found, pkg_found, template
from slpkg.__metadata__ import sbo_arch, build, sbo_tag, sbo_filetype
from slpkg.__metadata__ import tmp, pkg_path, build_path, log_path, sp

from slpkg.pkg.find import find_package 
from slpkg.pkg.build import build_package
from slpkg.pkg.manager import pkg_upgrade

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
    if dependencies_list == None:
        pass
    else:
        try:
            if not os.path.exists(build_path):
                os.mkdir(build_path)
            os.chdir(build_path)
            requires, dependencies = [], []
            requires.append(name)
            for pkg in dependencies_list:
                requires += pkg
            requires.reverse()
            for duplicate in requires:
                if duplicate not in dependencies:
                    dependencies.append(duplicate)
            pkg_sum = 0 
            pkg_for_install = []
            if find_package(name + sp, pkg_path):
                pkg_for_install.append(colors.GREEN + name + colors.ENDC)
                pkg_sum = 1
            else:
                pkg_for_install.append(colors.RED + name + colors.ENDC)
            sbo_ver = sbo_version_pkg(name)
            sys.stdout.write("Done\n")
            src = sbo_source_dwn(name)
            arch = os.uname()[4]
            if arch == "x86_64":
                arch = "x86_64"
            elif arch.startswith("i") and arch.endswith("86"):
                arch = "i486"
            elif "arm" in arch:
                arch = "arm"
            else:
                arch = os.uname()[4]
            if "UNSUPPORTED" in src:
                arch = "UNSUPPORTED"
            elif "UNTESTED" in src:
                arch = "UNTESTED"
            print("The following packages will be automatically installed or upgraded with new version:\n")
            template(78)
            print "| Package",  " "*31, "Version",  " "*7, "Arch", " "*5, "Repository"
            template(78)
            print("Installing:")
            print " ",  "".join(pkg_for_install), " "*(38-len(name)), sbo_ver, " "*(
                    14-len(sbo_ver)), arch, " "*(9-len(arch)), "SBo"
            print("Installing for dependencies:")
            for dep in dependencies[:-1]:
                sbo_ver = sbo_version_pkg(dep)
                if find_package(dep + sp, pkg_path):
                    print " ",  colors.GREEN + dep + colors.ENDC, " "*(38-len(dep)), sbo_ver, " "*(
                            14-len(sbo_ver)), arch, " "*(9-len(arch)), "SBo"
                    pkg_sum += 1
                else:
                    print " ",  colors.RED + dep + colors.ENDC, " "*(38-len(dep)), sbo_ver, " "*(
                            14-len(sbo_ver)), arch, " "*(9-len(arch)), "SBo"
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
                for pkg in dependencies:
                    sbo_version = sbo_version_pkg(pkg)
                    sbo_file = "".join(find_package(pkg + sp, pkg_path))
                    sbo_file_version = sbo_file[len(pkg) + 1:-len(arch) - 7]
                    if sbo_version > sbo_file_version:
                        prgnam = ("{0}-{1}".format(pkg, sbo_version_pkg(pkg)))
                        sbo_url = sbo_search_pkg(pkg)
                        sbo_link = sbo_slackbuild_dwn(sbo_url, pkg)
                        src_link = sbo_source_dwn(pkg).split() 
                        script = get_file(sbo_link, "/")
                        print("\n{0}Start -->{1} {2}\n".format(colors.GREEN, colors.ENDC, pkg))
                        subprocess.call("wget -N {0}".format(sbo_link), shell=True)
                        sources = []
                        for src in src_link:
                            subprocess.call("wget -N {0}".format(src), shell=True)
                            sources.append(get_file(src, "/"))
                        build_package(script, sources, build_path)
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
        except KeyboardInterrupt:
            print # new line at exit
            sys.exit()
