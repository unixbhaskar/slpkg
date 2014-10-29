#!/usr/bin/python
# -*- coding: utf-8 -*-

# arguments.py file is part of slpkg.

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


from __metadata__ import __version__


def options():
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
    for opt in arguments:
        print(opt)


def usage():
    view = [
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
    for usg in view:
        print(usg)
