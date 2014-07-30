#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
       .__          __            
  _____|  | ______ |  | __  ____  
 /  ___/  | \____ \|  |/ / / ___\ 
 \___ \|  |_|  |_> >    < / /_/  >
/____  >____/   __/|__|_ \\___  / 
     \/     |__|        \/_____/  


usage: slpkg   [-h] [-v] [-a script [source ...]]
               [-l all, sbo, slack, noarch, other [all, sbo, slack, noarch, other ...]]
               [-c sbo, slack [sbo, slack ...]]
               [-s sbo, slack [sbo, slack ...]] [-t] [-n] [-i  [...]]
               [-u  [...]] [-o  [...]] [-r  [...]] [-f  [...]] [-d  [...]]

Utility for easy management packages in Slackware

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         print version and exit
  -a script [source ...]
                        auto build package
  -l all, sbo, slack, noarch, other [all, sbo, slack, noarch, other ...]
                        list of installed packages
  -c sbo, slack [sbo, slack ...]
                        check if your packages is up to date
  -s sbo, slack [sbo, slack ...]
                        download, build & install packages
  -t                    tracking dependencies
  -n                    find packages from SBo repository
  -i  [ ...]            install binary packages
  -u  [ ...]            upgrade binary packages
  -o  [ ...]            reinstall binary packages
  -r  [ ...]            remove packages
  -f  [ ...]            find if packages installed
  -d  [ ...]            display the contents of the packages
'''

import argparse
from version import *
from functions import *
from colors import colors
from messages import ext_err_args
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
    parser.add_argument("-a", help="auto build package",
                        type=str, nargs="+", metavar=('script', 'source'))
    parser.add_argument("-l", help="list of installed packages", nargs="+", 
                        choices="all sbo slack noarch other".split(),
			            metavar=('all, sbo, slack, noarch, other'))
    parser.add_argument("-c", help="check if your packages is up to date",
                        type=str, nargs="+", metavar=('sbo, slack'))
    parser.add_argument("-s", help="download, build & install packages",
                        type=str, nargs="+", metavar=('sbo, slack'))
    parser.add_argument("-t", help="tracking dependencies",
                        type=str, metavar=(''))
    parser.add_argument("-n", help="find packages from SBo repository",
                        type=str, metavar=(''))
    parser.add_argument("-i", help="install binary packages",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-u", help="upgrade binary packages",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-o", help="reinstall binary packages",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-r", help="remove packages",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-f", help="find if packages installed",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-d", help="display the contents of the packages",
                        type=str, nargs="+", metavar=(''))
    args = parser.parse_args()
    if args.verbose:
        prog_version()
    if args.a:
        build_package(args.a[0], args.a[1], args.a[2:])
    if args.l:
        pkg_list(args.l)
    if args.t:
        pkg_tracking(args.t)
    if args.n:
        sbo_network(args.n)
    if args.c:
        if len(args.c) == 2:
            if "sbo" in args.c:
                sbo_check(''.join(args.c[1]))
            elif "slack" in args.c:
                if args.c[1] == "upgrade":
                    patches()
                else:
                    choices = ['upgrade']
                    ext_err_args()
                    err1_args(''.join(args.c), choices)
            else:
                choices = ['sbo', 'slack']
                ext_err_args()
                err1_args(''.join(args.c[0]), choices)
        elif len(args.c) < 2:
            if "sbo" in args.c or "slack" in args.c:
                ext_err_args()
                err2_args()
            else:
                choices = ['sbo', 'slack']
                ext_err_args()
                err1_args(''.join(args.c), choices)
        else:
            ext_err_args()
            err2_args()    
    if args.s:
        if len(args.s) == 2:
            if "sbo" in args.s:
                sbo_build(''.join(args.s[1]))
            elif "slack" in args.s:
                install(''.join(args.s[1]))
            else:
                choices = ['sbo', 'slack']
                ext_err_args()
                err1_args(''.join(args.s), choices)
        elif len(args.s) < 2:
            if "sbo" in args.s or "slack" in args.s:
                ext_err_args()
                err2_args()
            else:
                choices = ['sbo', 'slack']
                ext_err_args()
                err1_args(''.join(args.s), choices)
        else:
            ext_err_args()
            err2_args()
    if args.i:
        pkg_install(args.i)
    if args.u:
        pkg_upgrade(args.u)
    if args.o:
        pkg_reinstall(args.o)
    if args.r:
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

if __name__ == "__main__":
    main()
