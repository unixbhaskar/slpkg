#!/usr/bin/python
# -*- coding: utf-8 -*-

# greps.py file is part of slpkg.

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

from slpkg.__metadata__ import arch, lib_path


class SBoGrep(object):
    '''
    Class data grab
    '''
    def __init__(self, name):
        self.name = name
        arch64 = "x86_64"
        self.line_name = "SLACKBUILD NAME: "
        self.line_down = "SLACKBUILD DOWNLOAD: "
        self.line_down_64 = "SLACKBUILD DOWNLOAD_{0}: ".format(arch64)
        self.line_req = "SLACKBUILD REQUIRES: "
        self.line_ver = "SLACKBUILD VERSION: "
        self.line_md5 = "SLACKBUILD MD5SUM: "
        self.line_md5_64 = "SLACKBUILD MD5SUM_{0}: ".format(arch64)
        self.line_des = "SLACKBUILD SHORT DESCRIPTION:  "
        self.sbo_txt = lib_path + "sbo_repo/SLACKBUILDS.TXT"

        # open an read SLACKBUILDS.TXT file
        f = open(self.sbo_txt, "r")
        self.SLACKBUILDS_TXT = f.read()
        f.close()

    def source(self):
        '''
        Grab sources downloads links
        '''
        if arch == "x86_64":
            for line in self.SLACKBUILDS_TXT.splitlines():
                if line.startswith(self.line_name):
                    sbo_name = line[17:].strip()
                if line.startswith(self.line_down_64):
                    if sbo_name == self.name:
                        if line[28:].strip():
                            return line[28:].strip()
        for line in self.SLACKBUILDS_TXT.splitlines():
            if line.startswith(self.line_name):
                sbo_name = line[17:].strip()
            if line.startswith(self.line_down):
                if sbo_name == self.name:
                    return line[21:].strip()

    def requires(self):
        '''
        Grab package requirements
        '''
        for line in self.SLACKBUILDS_TXT.splitlines():
            if line.startswith(self.line_name):
                sbo_name = line[17:].strip()
            if line.startswith(self.line_req):
                if sbo_name == self.name:
                    return line[21:].strip().split()

    def version(self):
        '''
        Grab package version
        '''
        for line in self.SLACKBUILDS_TXT.splitlines():
            if line.startswith(self.line_name):
                sbo_name = line[17:].strip()
            if line.startswith(self.line_ver):
                if sbo_name == self.name:
                    return line[20:].strip()

    def checksum(self):
        '''
        Grab checksum string
        '''
        if arch == "x86_64":
            for line in self.SLACKBUILDS_TXT.splitlines():
                if line.startswith(self.line_name):
                    sbo_name = line[17:].strip()
                if line.startswith(self.line_md5_64):
                    if sbo_name == self.name:
                        if line[26:].strip():
                            return line[26:].strip()
        for line in self.SLACKBUILDS_TXT.splitlines():
            if line.startswith(self.line_name):
                sbo_name = line[17:].strip()
            if line.startswith(self.line_md5):
                if sbo_name == self.name:
                    return line[19:].strip()

    def description(self):
        '''
        Grab package verion
        '''
        for line in self.SLACKBUILDS_TXT.splitlines():
            if line.startswith(self.line_name):
                sbo_name = line[17:].strip()
            if line.startswith(self.line_des):
                if sbo_name == self.name:
                    return line[31:].strip()
