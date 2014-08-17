#!/usr/bin/python
# -*- coding: utf-8 -*-

# views.py

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

import os
import sys
import subprocess

from slpkg.colors import colors
from slpkg.functions import get_file
from slpkg.__metadata__ import tmp, pkg_path, slpkg_tmp, sp
from slpkg.__metadata__ import sbo_arch, sbo_tag, sbo_filetype, build_path
from slpkg.messages import s_user, pkg_not_found, pkg_found, view_sbo, template

from slpkg.pkg.build import build_package
from slpkg.pkg.find import find_package
from slpkg.pkg.manager import pkg_upgrade

from read import *
from greps import *
from search import sbo_search_pkg
from download import sbo_slackbuild_dwn

def sbo_network(name):
    '''
    View SlackBuild package, read or install them 
    from slackbuilds.org
    '''
    rdm_path = slpkg_tmp + "readme/"
    sys.stdout.write("Reading package lists ...")
    sbo_url = sbo_search_pkg(name)
    if sbo_url is None:
        sys.stdout.write ("Done\n")
        message = "From slackbuilds.org"
        bol, eol = "\n", "\n"
        pkg_not_found(bol, name, message, eol)
    else:
        if not os.path.exists(build_path):
            os.mkdir(build_path)
        sys.stdout.write ("Done\n")
        sbo_req = sbo_requires_pkg(sbo_url, name)
        sbo_dwn = sbo_slackbuild_dwn(sbo_url, name)
        sbo_version = sbo_version_pkg(sbo_url, name)
        source_dwn = sbo_source_dwn(sbo_url, name)
        extra_dwn = " ".join(sbo_extra_dwn(sbo_url, name))
        view_sbo(name, sbo_url, get_file(sbo_dwn, "/"), get_file(source_dwn, "/"),
                 ", ".join([get_file(extra_dwn, "/") for extra_dwn in extra_dwn.split()]),
                 sbo_req)
        while True:
            try:
                read = raw_input("_ ")
            except KeyboardInterrupt:
                print # new line at exit
                break
            if read == "D" or read == "d":
                print("\n{0}Start -->{1}\n".format(colors.GREEN, colors.ENDC))
                subprocess.call("wget -N {0} {1}".format(sbo_dwn, source_dwn), shell=True)
                if extra_dwn:
                    for src in extra_dwn.split():
                        subprocess.call("wget -N {0}".format(src), shell=True)
                break
            elif read == "R" or read == "r":
                site = "README"
                read_readme(sbo_url, name, site)
                subprocess.call("less {0}{1}.{2}".format(rdm_path, name, site), shell=True)
                os.remove("{0}{1}.{2}".format(rdm_path, name, site))
            elif read == "F" or read == "f":
                site = ".info"
                read_info_slackbuild(sbo_url, name, site)
                subprocess.call("less {0}{1}{2}".format(rdm_path, name, site), shell=True)
                os.remove("{0}{1}{2}".format(rdm_path, name, site))
            elif read == "S" or read == "s":
                site = ".SlackBuild"
                read_info_slackbuild(sbo_url, name, site)
                subprocess.call("less {0}{1}{2}".format(rdm_path, name, site), shell=True)
                os.remove("{0}{1}{2}".format(rdm_path, name, site))
            elif read == "B" or read == "b":
                os.chdir(build_path)
                script = get_file(sbo_dwn, "/")
                source = get_file(source_dwn, "/")
                print("\n{0}Start -->{1}\n".format(colors.GREEN, colors.ENDC))
                subprocess.call("wget -N {0} {1}".format(sbo_dwn, source_dwn), shell=True)
                extra = []
                if extra_dwn:
                    for src in extra_dwn.split():
                        subprocess.call("wget -N {0}".format(src), shell=True)
                        extra.append(get_file(src, "/"))
                build_package(script, source, extra, build_path)
                break
            elif read == "I" or read == "i":
                os.chdir(build_path)
                pkg_for_install = ("{0}-{1}".format(name, sbo_version))
                if find_package(name + sp, pkg_path) == []:
                    script = get_file(sbo_dwn, "/")
                    source = get_file(source_dwn, "/")
                    print("\n{0}Start -->{1}\n".format(colors.GREEN, colors.ENDC))
                    subprocess.call("wget -N {0} {1}".format(sbo_dwn, source_dwn), shell=True)
                    extra = []
                    if extra_dwn:
                        for src in extra_dwn.split():
                            subprocess.call("wget -N {0}".format(src), shell=True)
                            extra.append(get_file(src, "/"))
                    build_package(script, source, extra, build_path)
                    binary = ("{0}{1}{2}{3}{4}".format(
                               tmp, pkg_for_install, sbo_arch, sbo_tag, sbo_filetype).split())
                    pkg_upgrade(binary)
                    break
                else:
                    template(78)
                    pkg_found(name, sbo_version)
                    template(78)
                    print # new line at end
                    break
            else:
                break
