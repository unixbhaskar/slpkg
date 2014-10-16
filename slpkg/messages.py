#!/usr/bin/python
# -*- coding: utf-8 -*-

# messages.py file is part of slpkg.

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
from colors import RED, GREEN, CYAN, YELLOW, ENDC


def pkg_not_found(bol, pkg, message, eol):
    '''
    Print message when package not found
    '''
    print("{0}No such package {1}: {2}{3}".format(bol, pkg, message, eol))


def pkg_found(pkg, version):
    '''
    Print message when package found
    '''
    print("| Package {0}-{1} is already installed".format(pkg, version))


def pkg_installed(pkg):
    '''
    Print message when package installed
    '''
    print("| Package {0} installed".format(pkg))


def s_user(user):
    '''
    Check for root user
    '''
    if user != "root":
        print("\nslpkg: error: must have root privileges\n")
        sys.exit()


def build_FAILED(sbo_url, prgnam):
    template(78)
    print("| Build package {0} [ {1}FAILED{2} ]".format(prgnam, RED, ENDC))
    template(78)
    print("| See log file in {0}/var/log/slpkg/sbo/build_logs{1} directory or \
          read README file:".format(CYAN, ENDC))
    print("| {0}{1}".format(sbo_url, "README"))
    template(78)
    print   # new line at end


def template(max):
    '''
    Print template
    '''
    print("+" + "=" * max)


def view_sbo(pkg, sbo_url, sbo_desc, sbo_dwn, source_dwn, sbo_req):
    print   # new line at start
    template(78)
    print("| {0}Package {1}{2}{3} --> {4}".format(GREEN, CYAN, pkg, GREEN,
                                                  ENDC + sbo_url))
    template(78)
    print("| {0}Description : {1}{2}".format(GREEN, ENDC, sbo_desc))
    print("| {0}SlackBuild : {1}{2}".format(GREEN, ENDC, sbo_dwn))
    print("| {0}Sources : {1}{2}".format(GREEN, ENDC, source_dwn))
    print("| {0}Requirements : {1}{2}".format(YELLOW, ENDC, ", ".join(sbo_req)))
    template(78)
    print(" {0}R{1}EADME               View the README file".format(RED, ENDC))
    print(" {0}S{1}lackBuild           View the SlackBuild file".format(
        RED, ENDC))
    print(" In{0}f{1}o                 View the Info file".format(RED, ENDC))
    print(" {0}D{1}ownload             Download this package".format(RED, ENDC))
    print(" {0}B{1}uild                Download and build".format(RED, ENDC))
    print(" {0}I{1}nstall              Download/Build/Install".format(
        RED, ENDC))
    print(" {0}Q{1}uit                 Quit\n".format(RED, ENDC))


def sbo_packages_view(PKG_COLOR, package, version, ARCH_COLOR, arch):
    '''
    View slackbuild packages with version and arch
    '''
    print(" {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(
        PKG_COLOR, package, ENDC,
        " " * (38-len(package)), version,
        " " * (17-len(version)), ARCH_COLOR, arch, ENDC,
        " " * (13-len(arch)), "SBo"))
