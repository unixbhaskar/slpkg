#!/usr/bin/python
# -*- coding: utf-8 -*-

# views.py file is part of slpkg.

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

import os
import sys
import pydoc

from slpkg.init import initialization
from slpkg.downloader import Download
from slpkg.__metadata__ import tmp, build_path, pkg_path, sp
from slpkg.colors import RED, GREEN, GREY, CYAN, YELLOW, ENDC
from slpkg.messages import (pkg_found, pkg_not_found, template,
                            build_FAILED)

from slpkg.pkg.find import find_package
from slpkg.pkg.build import BuildPackage
from slpkg.pkg.manager import PackageManager

from read import Read
from greps import SBoGrep
from compressed import SBoLink
from search import sbo_search_pkg


class SBoNetwork(object):

    def __init__(self, name):
        self.name = name
        sys.stdout.write("{0}Reading package lists ...{1}".format(GREY, ENDC))
        sys.stdout.flush()
        initialization()
        grep = SBoGrep(self.name)
        self.sbo_url = sbo_search_pkg(self.name)
        self.sbo_desc = grep.description()[len(self.name) + 2:-1]
        self.sbo_req = grep.requires()
        self.source_dwn = grep.source().split()
        self.sbo_dwn = SBoLink(self.sbo_url).tar_gz()
        self.sbo_version = grep.version()
        self.space = ("\n" * 50)
        sys.stdout.write("{0}Done{1}\n".format(GREY, ENDC))

    def view(self):
        '''
        View SlackBuild package, read or install them
        from slackbuilds.org
        '''
        if self.sbo_url:
            prgnam = ("{0}-{1}".format(self.name, self.sbo_version))
            view_sbo(self.name, self.sbo_url, self.sbo_desc,
                     self.sbo_dwn.split("/")[-1],
                     ", ".join([src.split("/")[-1] for src in self.source_dwn]),
                     self.sbo_req)
            FAULT = error_uns(self.source_dwn)
            while True:
                choice = read_choice()
                if choice in ["D", "d"]:
                    download("", self.sbo_dwn, self.source_dwn)
                    break
                elif choice in ["R", "r"]:
                    README = Read(self.sbo_url).readme("README")
                    fill = fill_pager(README)
                    pydoc.pager(README + fill)
                elif choice in ["F", "f"]:
                    info = Read(self.sbo_url).info(self.name, ".info")
                    fill = fill_pager(info)
                    pydoc.pager(info + fill)
                elif choice in ["S", "s"]:
                    SlackBuild = Read(self.sbo_url).slackbuild(self.name,
                                                               ".SlackBuild")
                    fill = fill_pager(SlackBuild)
                    pydoc.pager(SlackBuild + fill)
                elif choice in ["B", "b"]:
                    build(self.sbo_dwn, self.source_dwn, FAULT)
                    break
                elif choice in ["I", "i"]:
                    if not find_package(prgnam + sp, pkg_path):
                        build(self.sbo_dwn, self.source_dwn, FAULT)
                        install(self.name, prgnam, self.sbo_url)
                        break
                    else:
                        template(78)
                        pkg_found(self.name, self.sbo_version)
                        template(78)
                        break
                else:
                    break
        else:
            pkg_not_found("\n", self.name, "Can't view", "\n")


def view_sbo(*args):
    '''
    View slackbuild.org
    '''
    print   # new line at start
    template(78)
    print("| {0}Package {1}{2}{3} --> {4}".format(GREEN, CYAN, args[0], GREEN,
                                                  ENDC + args[1]))
    template(78)
    print("| {0}Description : {1}{2}".format(GREEN, ENDC, args[2]))
    print("| {0}SlackBuild : {1}{2}".format(GREEN, ENDC, args[3]))
    print("| {0}Sources : {1}{2}".format(GREEN, ENDC, args[4]))
    print("| {0}Requirements : {1}{2}".format(YELLOW, ENDC, ", ".join(args[5])))
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


def fill_pager(page):
    '''
    Fix pager spaces
    '''
    tty_size = os.popen('stty size', 'r').read().split()
    rows = int(tty_size[0]) - 1
    lines = sum(1 for line in page.splitlines())
    diff = rows - lines
    fill = "\n" * diff
    if diff > 0:
        return fill
    else:
        return ""


def read_choice():
    '''
    Return choice
    '''
    try:
        choice = raw_input(" {0}Choose an option: {1}".format(GREY, ENDC))
    except KeyboardInterrupt:
        print   # new line at exit
        sys.exit()
    return choice


def error_uns(source_dwn):
    '''
    Check if package supported by arch
    before proceed to install
    '''
    UNST = ["UNSUPPORTED", "UNTESTED"]
    if "".join(source_dwn) in UNST:
        return "".join(source_dwn)


def download(path, sbo_dwn, source_dwn):
    '''
    Download sources
    '''
    Download(path, sbo_dwn).start()
    for src in source_dwn:
        Download(path, src).start()


def build(sbo_dwn, source_dwn, FAULT):
    '''
    Only build and create Slackware package
    '''
    if FAULT:
        print("\n{0}The package {1} {2}\n".format(RED, FAULT, ENDC))
        sys.exit()
    if not os.path.exists(build_path):
        os.mkdir(build_path)
    sources = []
    os.chdir(build_path)
    Download(build_path, sbo_dwn).start()
    script = sbo_dwn.split("/")[-1]
    for src in source_dwn:
        Download(build_path, src).start()
        sources.append(src.split("/")[-1])
    BuildPackage(script, sources, build_path).build()


def install(name, prgnam, sbo_url):
    '''
    Install Slackware package found in /tmp
    directory.
    '''
    binary_list = []
    for search in find_package(prgnam, tmp):
        if "_SBo" in search:
            binary_list.append(search)
        try:
            binary = (tmp + max(binary_list)).split()
        except ValueError:
            build_FAILED(sbo_url, prgnam)
            sys.exit()
        print("[ {0}Installing{1} ] --> {2}".format(GREEN, ENDC, name))
        PackageManager(binary).upgrade()
