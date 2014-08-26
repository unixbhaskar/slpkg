#!/usr/bin/python
# -*- coding: utf-8 -*-

# main.py

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

'''
     _       _         
 ___| |_ __ | | ____ _ 
/ __| | '_ \| |/ / _` |
\__ \ | |_) |   < (_| |
|___/_| .__/|_|\_\__, |
      |_|        |___/


usage: slpkg   [-h] [-v] [-a script [source ...]]
               [-l all, sbo, slack, noarch, other]
               [-c sbo, slack [sbo, slack ...]]
               [-s sbo, slack [sbo, slack ...]] [-t] [-n] [-i  [...]]
               [-u  [...]] [-o  [...]] [-r  [...]] [-f  [...]] [-d  [...]]

Utility for easy management packages in Slackware

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         print version and exit
  -a script [source ...]
                        auto build packages
  -l all, sbo, slack, noarch, other [all, sbo, slack, noarch, other ...]
                        list of installed packages
  -c sbo, slack [sbo, slack ...]
                        check if your packages is up to date
  -s sbo, slack [sbo, slack ...]
                        download, build & install packages
  -t                    packages tracking dependencies from SBo
  -n                    view packages from SBo repository
  -i  [ ...]            install binary packages
  -u  [ ...]            upgrade binary packages
  -o  [ ...]            reinstall binary packages
  -r  [ ...]            remove binary packages
  -f  [ ...]            view installed packages
  -d  [ ...]            display the contents of the packages

'''

import getpass
import argparse

from version import *
from functions import *
from colors import colors
from __metadata__ import path
from messages import ext_err_args, s_user
from messages import err1_args, err2_args

from pkg.build import build_package
from pkg.manager import *

from sbo.slackbuild import *
from sbo.dependency import *
from sbo.check import sbo_check
from sbo.views import sbo_network

from slack.patches import patches
from slack.install import install

def main():
    description = "Utility for easy management packages in Slackware"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-v", "--verbose", help="print version and exit",
                        action="store_true")
    parser.add_argument("-a", help="auto build packages",
                        type=str, nargs="+", metavar=("script", "source"))
    parser.add_argument("-l", help="list of installed packages",  
                        choices="all sbo slack noarch".split(),
			            metavar=("all, sbo, slack, noarch"))
    parser.add_argument("-c", help="check if your packages is up to date",
                        type=str, nargs="+", metavar=("sbo, slack"))
    parser.add_argument("-s", help="download, build & install packages",
                        type=str, nargs="+", metavar=("sbo, slack"))
    parser.add_argument("-t", help="packages tracking dependencies from SBo",
                        type=str, metavar=(""))
    parser.add_argument("-n", help="view packages from SBo repository",
                        type=str, metavar=(""))
    parser.add_argument("-i", help="install binary packages",
                        type=str, nargs="+", metavar=(""))
    parser.add_argument("-u", help="upgrade binary packages",
                        type=str, nargs="+", metavar=(""))
    parser.add_argument("-o", help="reinstall binary packages",
                        type=str, nargs="+", metavar=(""))
    parser.add_argument("-r", help="remove binary packages",
                        type=str, nargs="+", metavar=(""))
    parser.add_argument("-f", help="view installed packages",
                        type=str, nargs="+", metavar=(""))
    parser.add_argument("-d", help="display the contents of the packages",
                        type=str, nargs="+", metavar=(""))
    args = parser.parse_args()
    try:
        if args.verbose:
            prog_version()
        if args.a:
    	    s_user(getpass.getuser())
            build_package(args.a[0], args.a[1:], path)
        if args.l:
            pkg_list(args.l)
        if args.t:
            s_user(getpass.getuser())
            pkg_tracking(args.t)
        if args.n:
            s_user(getpass.getuser())
            sbo_network(args.n)
        if args.c:
            s_user(getpass.getuser())
            if len(args.c) == 2:
                if "sbo" in args.c:
                    if args.c[1] == "upgrade":
                        sbo_check()
                    else:
                        choices = ["upgrade"]
                        ext_err_args()
                        err1_args("".join(args.c[1]), choices)
                elif "slack" in args.c:
                    if args.c[1] == "upgrade":
                        patches()
                    else:
                        choices = ["upgrade"]
                        ext_err_args()
                        err1_args("".join(args.c[1]), choices)
                else:
                    choices = ["sbo", "slack"]
                    ext_err_args()
                    err1_args("".join(args.c[0]), choices)
            elif len(args.c) < 2:
                if "sbo" in args.c or "slack" in args.c:
                    choices = ['upgrade']
                    ext_err_args()
                    err2_args(choices)
                else:
                    choices = ["sbo", "slack"]
                    ext_err_args()
                    err1_args("".join(args.c), choices)
            else:
                ext_err_args()
                err2_args()    
        if args.s:
            s_user(getpass.getuser())
            if len(args.s) == 2:
                if "sbo" in args.s:
                    sbo_build("".join(args.s[1]))
                elif "slack" in args.s:
                    install("".join(args.s[1]))
                else:
                    choices = ["sbo", "slack"]
                    ext_err_args()
                    err1_args("".join(args.s[0]), choices)
            elif len(args.s) < 2:
                if "sbo" in args.s or "slack" in args.s:
                    choices = ["upgrade"]
                    ext_err_args()
                    err2_args(choices)
                else:
                    choices = ["sbo", "slack"]
                    ext_err_args()
                    err1_args("".join(args.s), choices)
            else:
                ext_err_args()
                err2_args()
        if args.i:
            s_user(getpass.getuser())
            pkg_install(args.i)
        if args.u:
            s_user(getpass.getuser())
            pkg_upgrade(args.u)
        if args.o:
    	    s_user(getpass.getuser())
            pkg_reinstall(args.o)
        if args.r:
            s_user(getpass.getuser())
            pkg_remove(args.r)
        if args.f:
            pkg_find(args.f)
        if args.d:
            pkg_display(args.d)
        if not any([args.verbose,
                    args.s,
                    args.t,
                    args.c,
                    args.n,
                    args.o,
                    args.i,
                    args.u,
                    args.a,
                    args.r,
                    args.l,
                    args.f,
                    args.d]):
            os.system("slpkg -h")
    except IndexError:
        ext_err_args()
        err2_args("")

if __name__ == "__main__":
    main()
