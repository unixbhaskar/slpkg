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

import os

from slpkg.url_read import url_read
from slpkg.__metadata__ import arch, lib_path

from search import sbo_search_pkg

def sbo_source_dwn(name):
    '''
    Grab sources downloads links
    '''
    if arch == "x86_64":
        with open(lib_path + "sbo_repo/SLACKBUILDS.TXT", "r") as SLACKBUILDS_TXT:
            for line in SLACKBUILDS_TXT:
                if arch == "x86_64":
                    if line.startswith("SLACKBUILD NAME: "):
                        sbo_name = line[17:].strip()
                    if line.startswith("SLACKBUILD DOWNLOAD_x86_64: "):
                        if sbo_name == name:
                            if line[28:].strip():
                                SLACKBUILDS_TXT.close()
                                return line[28:].strip()
    with open(lib_path + "sbo_repo/SLACKBUILDS.TXT", "r") as SLACKBUILDS_TXT:
        for line in SLACKBUILDS_TXT:
            if line.startswith("SLACKBUILD NAME: "):
                sbo_name = line[17:].strip()
            if line.startswith("SLACKBUILD DOWNLOAD: "):
                if sbo_name == name:
                    SLACKBUILDS_TXT.close()
                    return line[21:].strip() 
        
def sbo_requires_pkg(name):
    '''
    Grab package requirements
    '''
    with open(lib_path + "sbo_repo/SLACKBUILDS.TXT", "r") as SLACKBUILDS_TXT:
        for line in SLACKBUILDS_TXT:
            if line.startswith("SLACKBUILD NAME: "):
                sbo_name = line[17:].strip()
            if line.startswith("SLACKBUILD REQUIRES: "):
                if sbo_name == name:
                    SLACKBUILDS_TXT.close()
                    return line[21:].strip().split()

def sbo_build_tag(sbo_url, name):
    # This feature is not yet used
    # because the program is doing heavy on search.
    # Looking for the best option to be able to use
    # the BUILD tag
    '''
    Grab .SlackBuild BUILD tag
    '''
    read_info = url_read(sbo_url + name + ".SlackBuild")
    for line in read_info.splitlines():
        if line.startswith("BUILD=${BUILD:"):
            return line[15:-1].strip().split()

def sbo_version_pkg(name):
    '''
    Grab package verion
    '''
    with open(lib_path + "sbo_repo/SLACKBUILDS.TXT", "r") as SLACKBUILDS_TXT:
        for line in SLACKBUILDS_TXT:
            if line.startswith("SLACKBUILD NAME: "):
                sbo_name = line[17:].strip()
            if line.startswith("SLACKBUILD VERSION: "):
                if sbo_name == name:
                    SLACKBUILDS_TXT.close()
                    return line[20:].strip()

def sbo_checksum_pkg(name):
    '''
    Grab checksum string
    '''
    if arch == "x86_64":
        with open(lib_path + "sbo_repo/SLACKBUILDS.TXT", "r") as SLACKBUILDS_TXT:
            for line in SLACKBUILDS_TXT:
                if arch == "x86_64":
                    if line.startswith("SLACKBUILD NAME: "):
                        sbo_name = line[17:].strip()
                    if line.startswith("SLACKBUILD MD5SUM_x86_64: "):
                        if sbo_name == name:
                            if line[26:].strip():
                                SLACKBUILDS_TXT.close()
                                return line[26:].strip()
    with open(lib_path + "sbo_repo/SLACKBUILDS.TXT", "r") as SLACKBUILDS_TXT:
        for line in SLACKBUILDS_TXT:
            if line.startswith("SLACKBUILD NAME: "):
                sbo_name = line[17:].strip()
            if line.startswith("SLACKBUILD MD5SUM: "):
                if sbo_name == name:
                    SLACKBUILDS_TXT.close()
                    return line[19:].strip()
    
def sbo_description_pkg(name):
    '''
    Grab package verion
    '''
    with open(lib_path + "sbo_repo/SLACKBUILDS.TXT", "r") as SLACKBUILDS_TXT:
        for line in SLACKBUILDS_TXT:
            if line.startswith("SLACKBUILD NAME: "):
                sbo_name = line[17:].strip()
            if line.startswith("SLACKBUILD SHORT DESCRIPTION:  "):
                if sbo_name == name:
                    SLACKBUILDS_TXT.close()
                    return line[31:].strip()
