#!/usr/bin/python
# -*- coding: utf-8 -*-

# queue.py file is part of slpkg.

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

from downloader import Download
from colors import GREEN, RED, ENDC
from __metadata__ import lib_path, build_path, tmp

from sbo.greps import SBoGrep
from pkg.find import find_package
from pkg.build import build_package
from sbo.search import sbo_search_pkg
from pkg.manager import PackageManager
from sbo.download import sbo_slackbuild_dwn


class QueuePkgs(object):
    '''
    Class to list, add or remove packages in queue,
    also build or install.
    '''

    def __init__(self):
        queue_file = [
            "# In this file you can create a list of\n",
            "# packages you want to build or install.\n",
            "#\n"
        ]
        self.quit = False
        self.queue = lib_path + "queue/"
        self.queue_list = self.queue + "queue_list"
        if not os.path.exists(lib_path):
            os.mkdir(lib_path)
        if not os.path.exists(self.queue):
            os.mkdir(self.queue)
        if not os.path.isfile(self.queue_list):
            with open(self.queue_list, "w") as queue:
                for line in queue_file:
                    queue.write(line)
                queue.close()

        f = open(self.queue_list, "r")
        self.queued = f.read()
        f.close()

    def packages(self):
        '''
        Return queue list from /var/lib/queue/queue_list
        file.
        '''
        queue_list = []
        for read in self.queued.splitlines():
            read = read.lstrip()
            if not read.startswith("#"):
                queue_list.append(read.replace("\n", ""))
        return queue_list

    def listed(self):
        '''
        Print packages from queue
        '''
        print("\nPackages in queue:\n")
        for pkg in self.packages():
            if pkg:
                print("{0}{1}{2}".format(GREEN, pkg, ENDC))
                self.quit = True
        if self.quit:
            print   # new line at exit

    def add(self, pkgs):
        '''
        Add packages in queue if not exist
        '''
        queue_list = self.packages()
        pkgs = set(pkgs)
        print("\nAdd packages in queue:\n")
        with open(self.queue_list, "a") as queue:
            for pkg in pkgs:
                find = sbo_search_pkg(pkg)
                if pkg not in queue_list and find is not None:
                    print("{0}{1}{2}".format(GREEN, pkg, ENDC))
                    queue.write(pkg + "\n")
                    self.quit = True
                else:
                    print("{0}{1}{2}".format(RED, pkg, ENDC))
                    self.quit = True
            queue.close()
        if self.quit:
            print   # new line at exit

    def remove(self, pkgs):
        '''
        Remove packages from queue
        '''
        print("\nRemove packages from queue:\n")
        if pkgs == ["all"]:
            pkgs = self.packages()
        with open(self.queue_list, "w") as queue:
            for line in self.queued.splitlines():
                if line not in pkgs:
                    queue.write(line + "\n")
                else:
                    print("{0}{1}{2}".format(RED, line, ENDC))
                    self.quit = True
            queue.close()
        if self.quit:
            print   # new line at exit

    def build(self):
        '''
        Build packages from queue
        '''
        packages = self.packages()
        if packages:
            for pkg in packages:
                if not os.path.exists(build_path):
                    os.mkdir(build_path)
                sbo_url = sbo_search_pkg(pkg)
                sbo_dwn = sbo_slackbuild_dwn(sbo_url)
                source_dwn = SBoGrep(pkg).source().split()
                sources = []
                os.chdir(build_path)
                script = sbo_dwn.split("/")[-1]
                Download(build_path, sbo_dwn).start()
                for src in source_dwn:
                    Download(build_path, src).start()
                    sources.append(src.split("/")[-1])
                build_package(script, sources, build_path)
        else:
            print("\nPackages not found in the queue for building\n")

    def install(self):
        '''
        Install packages from queue
        '''
        packages = self.packages()
        if packages:
            print   # new line at start
            for pkg in packages:
                # check if package exist in repository
                find = find_package(pkg, tmp)
                try:
                    find = max(find)
                except ValueError:
                    print("Package '{0}' not found in /tmp\n".format(pkg))
                if pkg in find:
                    binary = "{0}{1}".format(tmp, find)
                    PackageManager(binary.split()).install()
        else:
            print("\nPackages not found in the queue for installation\n")
