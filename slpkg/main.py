#!/usr/bin/python
# -*- coding: utf-8 -*-

# main.py file is part of slpkg.

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

'''
slpkg - Utility for easy management packages in Slackware

Optional arguments:
  -h, --help                   show this help message and exit
  -v, --version                print version and exit
  -a, script [source...]       auto build packages
  -l, all, sbo, slack, noarch  list of installed packages
  -c, <repository> --upgrade   check if your packages is up to date
  -s, <repository> <package>   download, build & install packages
  -f, <package>                find installed packages
  -t, <package>                packages tracking dependencies from SBo
  -n, <package>                view packages from SBo repository
  -i, [package...]             install binary packages
  -u, [package...]             upgrade binary packages
  -o, [package...]             reinstall binary packages
  -r, [package...]             remove binary packages
  -d, [package...]             display the contents of the packages

Repositories:
      SlackBuilds = sbo
      Slackware = slack
'''

import getpass

from colors import *
from messages import s_user
from version import prog_version
from __metadata__ import path, __version__

from pkg.manager import *
from pkg.build import build_package

from sbo.check import sbo_check
from sbo.views import sbo_network
from sbo.slackbuild import sbo_build
from sbo.dependency import pkg_tracking

from slack.patches import patches
from slack.install import install


def main():
    arguments = [
            "slpkg - version {0}\n".format(__version__),
            "Utility for easy management packages in Slackware\n",
            "Optional arguments:",
            "  -h, --help                   show this help message and exit",
            "  -v, --version                print version and exit",
            "  -a, script [source...]       auto build packages",
            "  -l, all, sbo, slack, noarch  list of installed packages",
            "  -c, <repository> --upgrade   check if your packages is up to date",
            "  -s, <repository> <package>   download, build & install packages",
            "  -f, <package>                find installed packages",
            "  -t, <package>                packages tracking dependencies from SBo",
            "  -n, <package>                view packages from SBo repository",
            "  -i, [package...]             install binary packages",
            "  -u, [package...]             upgrade binary packages",
            "  -o, [package...]             reinstall binary packages",
            "  -r, [package...]             remove binary packages",
            "  -d, [package...]             display the contents of the packages\n",
            "Repositories:",
            "      SlackBuilds = sbo",
            "      Slackware = slack\n",
            ]
    usage = [
            "slpkg - version {0}\n".format(__version__),
            "Usage: slpkg [-h] [-v] [-a script [sources...]]",
            "             [-l all, sbo, slack, noarch]", 
            "             [-c <repository> --upgrade]",
            "             [-s <repository> <package>]",
            "             [-f] [-t] [-n] [-i [...]]",
            "             [-u  [...]] [-o [...]] [-r [...]] [-d [...]]\n",
            "For more information try 'slpkg --help'\n"
            ]
    args = sys.argv
    args.pop(0)
    repository = ["sbo", "slack"]
    if len(args) == 0:
        for opt in usage: print(opt)
    elif len(args) == 1 and args[0] == "-h" or args[0] == "--help":
        for opt in arguments: print(opt)
    elif len(args) == 1 and args[0] == "-v" or args[0] == "--version":
        prog_version()
    elif len(args) == 3 and args[0] == "-a":
        s_user(getpass.getuser())
        build_package(args[1], args[2:], path)
    elif len(args) == 2 and args[0] == "-l":
        sbo_list = ["all", "sbo", "slack", "noarch"]
        if args[1] in sbo_list:
            pkg_list(args[1])
        else:
            for opt in usage: print(opt)
    elif len(args) == 3 and args[0] == "-c":
        s_user(getpass.getuser())
        if args[1] == repository[0] and args[2] == "--upgrade":
            sbo_check()
        elif args[1] == repository[1] and args[2] == "--upgrade":
            patches()
        else:
            for opt in usage: print(opt)
    elif len(args) == 3 and args[0] == "-s":
        s_user(getpass.getuser())
        if args[1] == repository[0]:
            sbo_build(args[2])
        elif args[1] == repository[1]:
            install(args[2])         
    elif len(args) == 2 and args[0] == "-t":
        s_user(getpass.getuser())
        pkg_tracking(args[1])
    elif len(args) == 2 and args[0] == "-n":
        s_user(getpass.getuser())
        sbo_network(args[1])
    elif len(args) > 1 and args[0] == "-i":
        s_user(getpass.getuser())
        pkg_install(args[1:])
    elif len(args) > 1 and args[0] == "-u":
        s_user(getpass.getuser())
        pkg_upgrade(args[1:])
    elif len(args) > 1 and args[0] == "-o":
        s_user(getpass.getuser())
        pkg_reinstall(args[1:])
    elif len(args) > 1 and args[0] == "-r":
        s_user(getpass.getuser())
        pkg_remove(args[1:])
    elif len(args) > 1 and args[0] == "-f":
        pkg_find(args[1:])
    elif len(args) > 1 and args[0] == "-d":
        pkg_display(args[1:])
    else:
        for opt in usage: print(opt)
if __name__ == "__main__":
    main()   
