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
from __metadata__ import path
from blacklist import BlackList
from version import prog_version
from arguments import options, usage

from pkg.build import BuildPackage
from pkg.manager import PackageManager

from sbo.check import SBoCheck
from sbo.views import SBoNetwork
from sbo.tracking import track_dep
from sbo.slackbuild import SBoInstall

from slack.install import Slack
from slack.patches import Patches


def main():

    # root privileges required
    s_user(getpass.getuser())
    args = sys.argv
    args.pop(0)
    repository = ["sbo", "slack"]
    blacklist = BlackList()
    queue = QueuePkgs()

    if len(args) == 0:
        usage()
    elif (len(args) == 1 and args[0] == "-h" or
            args[0] == "--help" and args[1:] == []):
        options()
    elif (len(args) == 1 and args[0] == "-v" or
            args[0] == "--version" and args[1:] == []):
        prog_version()
    elif len(args) == 3 and args[0] == "-a":
        BuildPackage(args[1], args[2:], path).build()
    elif len(args) == 2 and args[0] == "-l":
        sbo_list = ["all", "sbo", "slack", "noarch"]
        if args[1] in sbo_list:
            PackageManager(None).list(args[1])
        else:
            usage()
    elif len(args) == 3 and args[0] == "-c":
        if args[1] == repository[0] and args[2] == "--upgrade":
            SBoCheck().start()
        elif args[1] == repository[1] and args[2] == "--upgrade":
            version = "stable"
            Patches(version).start()
        else:
            usage()
    elif len(args) == 4 and args[0] == "-c":
        if args[1] == repository[1] and args[3] == "--current":
            version = "current"
            Patches(version).start()
        else:
            usage()
    elif len(args) == 3 and args[0] == "-s":
        if args[1] == repository[0]:
            SBoInstall(args[2]).start()
        elif args[1] == repository[1]:
            Slack(args[2], "stable").start()
        else:
            usage()
    elif len(args) == 4 and args[0] == "-s":
        if args[1] == repository[1] and args[3] == "--current":
            Slack(args[2], "current").start()
        else:
            usage()
    elif len(args) == 2 and args[0] == "-t":
        track_dep(args[1])
    elif len(args) == 2 and args[0] == "-n":
        SBoNetwork(args[1]).view()
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
        usage()

if __name__ == "__main__":
    main()
