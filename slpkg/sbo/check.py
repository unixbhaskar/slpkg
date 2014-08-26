#!/usr/bin/python
# -*- coding: utf-8 -*-

# check.py

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

from slpkg.pkg.build import build_package
from slpkg.pkg.manager import pkg_upgrade

from slpkg.colors import colors
from slpkg.messages import template
from slpkg.functions import get_file
from slpkg.__metadata__ import tmp, pkg_path, build_path
from slpkg.__metadata__ import sbo_arch, build, sbo_tag, sbo_filetype

from init import initialization
from search import sbo_search_pkg
from download import sbo_slackbuild_dwn
from greps import sbo_source_dwn, sbo_version_pkg

def sbo_check():
    '''
    Upgrade all slackbuilds packages from slackbuilds.org
    repository
    '''
    try:
        sys.stdout.write("Reading package lists ...")
        sys.stdout.flush()
        initialization()
        index, toolbar_width = 0, 3
        pkg_name, sbo_ver, pkg_for_upg, sbo_list = [], [], [], []
        for pkg in os.listdir(pkg_path):
            if "_SBo" in pkg:
                sbo_list.append(pkg)
        if sbo_list: 
            for pkg in sbo_list:
                index += 1
                if index == toolbar_width:
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    toolbar_width += 3
                if "-x86_64-" in pkg:
                    arch = "x86_64"
                elif "-i486-" in pkg:
                    arch = "i486"
                elif "-arm-" in pkg:
                    arch = "arm"
                elif "-noarch-" in pkg:
                    arch = "noarch"
                else:
                    arch = os.uname()[4]
                name = pkg[:-(len(arch) + len("_SBo") + 3)]
                pkg_version = get_file(name, "-")[1:]
                name = name[:-(len(pkg_version) + 1)]
                sbo_version = sbo_version_pkg(name)
                if sbo_version > pkg_version:
                    pkg_name.append(name)
                    pkg_for_upg.append(name + "-" + pkg_version)
                    sbo_ver.append(sbo_version)
            sys.stdout.write("Done\n")
            if pkg_for_upg:
                print("\nThese packages need upgrading:\n")
                template(78)
                print "| Package",  " "*27, "New version",  " "*5, "Arch", " "*7, "Repository"
                template(78)
                print("Upgrading:")
                for upg, ver in zip(pkg_for_upg, sbo_ver):
                    print " ",  upg, " "*(34-len(upg)), ver, " "*(
                          16-len(ver)), arch, " "*(11-len(arch)), "SBo"
                msg_pkg = "package"
                if len(pkg_for_upg) > 1:
                    msg_pkg = msg_pkg + "s"
                print("\nInstalling summary")
                print("=" * 79)
                print("Total {0} {1} will be upgraded.\n".format(len(pkg_for_upg), msg_pkg))
                read = raw_input("Would you like to upgrade [Y/n]? ")
                if read == "Y" or read == "y":
                    if not os.path.exists(build_path):
                        os.mkdir(build_path)
                    os.chdir(build_path)
                    for name, version in zip(pkg_name, sbo_ver):
                        pkg_for_install = ("{0}-{1}".format(name, version))
                        sbo_url = sbo_search_pkg(name)
                        sbo_dwn = sbo_slackbuild_dwn(sbo_url, name)
                        src_dwn = sbo_source_dwn(name).split()
                        script = get_file(sbo_dwn, "/")
                        print("\n{0}Start -->{1} {2}\n".format(colors.GREEN, colors.ENDC, name))
                        subprocess.call("wget -N {0}".format(sbo_dwn), shell=True)
                        sources = []
                        for src in src_dwn:
                            subprocess.call("wget -N {0}".format(src), shell=True)
                            sources.append(get_file(src, "/"))
                        build_package(script, sources, build_path)
                        binary = ("{0}{1}{2}{3}{4}{5}".format(
                            tmp, pkg_for_install, sbo_arch, build, sbo_tag, sbo_filetype).split())
                        print("{0}[ Upgrading ] --> {1}{2}".format(
                            colors.GREEN, colors.ENDC, name))
                        pkg_upgrade(binary)
                    print("Completed!\n")
            else:
                print("\nAll SBo packages are up to date\n")
        else:
            sys.stdout.write("Done\n")
            print("\nNo SBo packages found\n")
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
