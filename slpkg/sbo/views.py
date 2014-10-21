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

from slpkg.colors import RED, GREEN, GREY, ENDC
from slpkg.init import initialization
from slpkg.downloader import Download
from slpkg.__metadata__ import tmp, build_path, pkg_path, sp
from slpkg.messages import (pkg_found, view_sbo, pkg_not_found,
                            template, build_FAILED)

from slpkg.pkg.build import build_package
from slpkg.pkg.find import find_package
from slpkg.pkg.manager import PackageManager

from greps import SBoGrep
from search import sbo_search_pkg
from download import sbo_slackbuild_dwn
from read import read_readme, read_info_slackbuild


def sbo_network(name):
    '''
    View SlackBuild package, read or install them
    from slackbuilds.org
    '''
    done = "{0}Done{1}\n".format(GREY, ENDC)
    reading_lists = "{0}Reading package lists ...{1}".format(GREY, ENDC)
    sys.stdout.write(reading_lists)
    sys.stdout.flush()
    initialization()
    sbo_url = sbo_search_pkg(name)
    sys.stdout.write(done)
    if sbo_url:
        grep = SBoGrep(name)
        sbo_desc = grep.description()[len(name) + 2:-1]
        sbo_req = grep.requires()
        source_dwn = grep.source().split()
        sbo_dwn = sbo_slackbuild_dwn(sbo_url)
        sbo_version = grep.version()
        prgnam = ("{0}-{1}".format(name, sbo_version))
        view_sbo(name, sbo_url, sbo_desc, sbo_dwn.split("/")[-1],
                 ", ".join([src.split("/")[-1] for src in source_dwn]),
                 sbo_req)
        # Check if package supported by arch
        # before proceed to install
        FAULT = ""
        UNST = ["UNSUPPORTED", "UNTESTED"]
        if "".join(source_dwn) in UNST:
            FAULT = "".join(source_dwn)
        while True:
            try:
                choice = raw_input(" {0}Choose an option: {1}".format(GREY,
                                                                      ENDC))
            except KeyboardInterrupt:
                print   # new line at exit
                break
            if choice in ["D", "d"]:
                download("", sbo_dwn, source_dwn)
                break
            elif choice in ["R", "r"]:
                readme = "README"
                pydoc.pager(read_readme(sbo_url, readme))
            elif choice in ["F", "f"]:
                _info = ".info"
                pydoc.pager(read_info_slackbuild(sbo_url, name, _info))
            elif choice in ["S", "s"]:
                _SlackBuild = ".SlackBuild"
                pydoc.pager(read_info_slackbuild(sbo_url, name, _SlackBuild))
            elif choice in ["B", "b"]:
                build(sbo_dwn, source_dwn, FAULT)
                break
            elif choice in ["I", "i"]:
                if not find_package(prgnam + sp, pkg_path):
                    build(sbo_dwn, source_dwn, FAULT)
                    install(name, prgnam, sbo_url)
                    break
                else:
                    template(78)
                    pkg_found(name, sbo_version)
                    template(78)
                    break
            else:
                break
    else:
        message = "Can't view"
        pkg_not_found("\n", name, message, "\n")


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
    build_package(script, sources, build_path)


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
        print("[ {0}Installing{1} ] --> {2}".format(GREEN, ENDC,
                                                    name))
        PackageManager(binary).upgrade()
