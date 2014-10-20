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

import sys
import getpass

from queue import QueuePkgs
from messages import s_user
from blacklist import BlackList
from version import prog_version
from __metadata__ import path, __version__

from pkg.build import build_package
from pkg.manager import PackageManager

from sbo.check import sbo_check
from sbo.views import sbo_network
from sbo.tracking import track_dep
from sbo.slackbuild import sbo_install

from slack.patches import patches
from slack.install import install


def main():

    # root privileges required
    s_user(getpass.getuser())
    arguments = [
        "slpkg - version {0}\n".format(__version__),
        "Utility for easy management packages in Slackware\n",
        "Optional arguments:",
        "  -h, --help                                show this help message " +
        "and exit",
        "  -v, --version                             print version and exit",
        "  -a, script [source...]                    auto build packages",
        "  -b, --list, [package...] --add, --remove  add, remove packages in " +
        "blacklist",
        "  -q, --list, [package...] --add, --remove  add, remove packages in " +
        "queue",
        "      --build, --install, --build-install   build or install from " +
        "queue",
        "  -l, all, sbo, slack, noarch               list of installed " +
        "packages",
        "  -c, <repository> --upgrade --current      check for updated " +
        "packages",
        "  -s, <repository> <package> --current      download, build & install",
        "  -f, <package>                             find installed packages",
        "  -t, <package>                             tracking dependencies " +
        "from SBo",
        "  -n, <package>                             view packages from SBo",
        "  -i, [package...]                          install binary packages",
        "  -u, [package...]                          upgrade binary packages",
        "  -o, [package...]                          reinstall binary packages",
        "  -r, [package...]                          remove binary packages",
        "  -d, [package...]                          display the contents\n",
        "Repositories:",
        "      SlackBuilds = sbo",
        "      Slackware = slack '--current'\n",
    ]
    usage = [
        "slpkg - version {0}\n".format(__version__),
        "Usage: slpkg [-h] [-v] [-a script [sources...]]",
        "             [-b --list, [...] --add, --remove]",
        "             [-q --list, [...] --add, --remove]",
        "             [-q --build, --install, --build-install]",
        "             [-l all, sbo, slack, noarch]",
        "             [-c <repository> --upgrade --current]",
        "             [-s <repository> <package> --current]",
        "             [-f] [-t] [-n] [-i [...]] [-u  [...]]",
        "             [-o  [...]] [-r [...]] [-d [...]]\n",
        "For more information try 'slpkg --help'\n"
    ]
    args = sys.argv
    args.pop(0)
    repository = ["sbo", "slack"]
    blacklist = BlackList()
    queue = QueuePkgs()
    if len(args) == 0:
        for opt in usage:
            print(opt)
    elif (len(args) == 1 and args[0] == "-h" or
            args[0] == "--help" and args[1:] == []):
        for opt in arguments:
            print(opt)
    elif (len(args) == 1 and args[0] == "-v" or
            args[0] == "--version" and args[1:] == []):
        prog_version()
    elif len(args) == 3 and args[0] == "-a":
        build_package(args[1], args[2:], path)
    elif len(args) == 2 and args[0] == "-l":
        sbo_list = ["all", "sbo", "slack", "noarch"]
        if args[1] in sbo_list:
            PackageManager(None).list(args[1])
        else:
            for opt in usage:
                print(opt)
    elif len(args) == 3 and args[0] == "-c":
        if args[1] == repository[0] and args[2] == "--upgrade":
            sbo_check()
        elif args[1] == repository[1] and args[2] == "--upgrade":
            version = "stable"
            patches(version)
        else:
            for opt in usage:
                print(opt)
    elif len(args) == 4 and args[0] == "-c":
        if args[1] == repository[1] and args[3] == "--current":
            version = "current"
            patches(version)
        else:
            for opt in usage:
                print(opt)
    elif len(args) == 3 and args[0] == "-s":
        if args[1] == repository[0]:
            sbo_install(args[2])
        elif args[1] == repository[1]:
            version = "stable"
            install(args[2], version)
    elif len(args) == 4 and args[0] == "-s":
        if args[1] == repository[1] and args[3] == "--current":
            version = "current"
            install(args[2], version)
        else:
            for opt in usage:
                print(opt)
    elif len(args) == 2 and args[0] == "-t":
        track_dep(args[1])
    elif len(args) == 2 and args[0] == "-n":
        sbo_network(args[1])
    elif len(args) == 2 and args[0] == "-b" and args[1] == "--list":
        blacklist.listed()
    elif len(args) > 2 and args[0] == "-b" and args[-1] == "--add":
        blacklist.add(args[1:-1])
    elif len(args) > 2 and args[0] == "-b" and args[-1] == "--remove":
        blacklist.remove(args[1:-1])
    elif len(args) == 2 and args[0] == "-q" and args[1] == "--list":
        queue.listed()
    elif len(args) > 2 and args[0] == "-q" and args[-1] == "--add":
        queue.add(args[1:-1])
    elif len(args) > 2 and args[0] == "-q" and args[-1] == "--remove":
        queue.remove(args[1:-1])
    elif len(args) == 2 and args[0] == "-q" and args[1] == "--build":
        queue.build()
    elif len(args) == 2 and args[0] == "-q" and args[1] == "--install":
        queue.install()
    elif len(args) == 2 and args[0] == "-q" and args[1] == "--build-install":
        queue.build()
        queue.install()
    elif len(args) > 1 and args[0] == "-i":
        PackageManager(args[1:]).install()
    elif len(args) > 1 and args[0] == "-u":
        PackageManager(args[1:]).upgrade()
    elif len(args) > 1 and args[0] == "-o":
        PackageManager(args[1:]).reinstall()
    elif len(args) > 1 and args[0] == "-r":
        PackageManager(args[1:]).remove()
    elif len(args) > 1 and args[0] == "-f":
        PackageManager(args[1:]).find()
    elif len(args) > 1 and args[0] == "-d":
        PackageManager(args[1:]).display()
    else:
        for opt in usage:
            print(opt)

if __name__ == "__main__":
    main()
