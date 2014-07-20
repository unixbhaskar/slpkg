#!/usr/bin/python
# -*- coding: utf-8 -*-


''' Utility to help package management in Slackware.
Slpkg is a terminal tool in order to easy use Slackware packages.


It's a quick and easy way to manage your packages in Slackware to a command.



usage: slpkg [-h] [-v] [-s script [source ...]] [-l all, sbo [all, sbo ...]]
             [-t] [-n] [-c] [-b] [-i  [...]] [-u  [...]] [-a  [...]]
             [-r  [...]] [-f  [...]] [-d  [...]]

Utility to help package management in Slackware

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         print version and exit
  -s script [source ...]
                        auto build package
  -l all, sbo [all, sbo ...]
                        list of installed packages
  -t                    tracking dependencies
  -n                    find from SBo repositority
  -c                    check if your package is up to date
  -b                    download, build & install pkg from SBo
  -i  [ ...]            install binary packages
  -u  [ ...]            install-upgrade packages with new
  -a  [ ...]            reinstall the same packages
  -r  [ ...]            remove packages
  -f  [ ...]            find if packages installed
  -d  [ ...]            display the contents of the packages

'''

import argparse

from version import *
from functions import *
from colors import colors
from __metadata__ import __prog__

from pkg.build import *
from pkg.manager import *

from sbo.slackbuild import *
from sbo.dependency import *
from sbo.check import sbo_check
from sbo.views import sbo_network

def pkg_slackbuild(name):
    '''
    Select build package for build with extra source or not
    '''
    s_user(getpass.getuser())
    if len(name) == 2:
        build_package(name[0], name[1])
    elif len(name) > 2:
        build_extra_pkg(name[0], name[1], name[2:])
    else:
        print ("\n{0}: error: must enter at least two arguments\n".format(
                __prog__))

def main():
    description = "Utility to help package management in Slackware"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-v", "--verbose", help="print version and exit",
                        action="store_true")
    parser.add_argument("-a", help="auto build package",
                        type=str, nargs="+", metavar=('script', 'source'))
    parser.add_argument("-l", help="list of installed packages", nargs="+", 
                        choices="all sbo".split(), metavar=('all, sbo'))
    parser.add_argument("-t", help="tracking dependencies",
                        type=str, metavar=(''))
    parser.add_argument("-n", help="find from SBo repositority",
                        type=str, metavar=(''))
    parser.add_argument("-c", help="check if your package is up to date",
                        type=str, metavar=(''))
    parser.add_argument("-s", help="download, build & install pkg from SBo",
                        type=str, metavar=(''))
    parser.add_argument("-i", help="install binary packages",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-u", help="install-upgrade packages with new",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-o", help="reinstall the same packages",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-r", help="remove packages",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-f", help="find if packages installed",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-d", help="display the contents of the packages",
                        type=str, nargs="+", metavar=(''))
    args = parser.parse_args()
    if args.verbose:
        pkg_version()
    if args.a:
        pkg_slackbuild(args.a)
    if args.l:
        pkg_list(args.l)
    if args.t:
        pkg_tracking(args.t)
    if args.n:
        sbo_network(args.n)
    if args.c:
        sbo_check(args.c)
    if args.s:
        sbo_build(args.s)
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
