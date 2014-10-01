#!/usr/bin/python
# -*- coding: utf-8 -*-

# blacklist.py file is part of slpkg.

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

from init import initialization
from __metadata__ import bls_path

if not os.path.isfile(bls_path + "blacklist"):
    init = initialization()

def black_packages():
    '''
    Return blacklist packages from /etc/slpkg/blacklist 
    configuration file.
    '''
    blacklist = []
    blackfile = bls_path + "blacklist"
    with open(blackfile, "r") as black_conf:
        for read in black_conf:
            read = read.lstrip()
            if not read.startswith("#"):
                blacklist.append(read.replace("\n", "")) 
        black_conf.close()
    return blacklist

def blacklisted():
    '''
    Print blacklist packages
    '''
    exit = 0
    print("\nPackages in blacklist:\n")
    for black in black_packages():
        if black:
            print(black)
            exit = 1
    if exit == 1:
        print # new line at exit

def add_blacklist(pkgs):
    '''
    Add blacklist packages if not exist
    '''
    exit = 0
    blackfile = bls_path + "blacklist"
    blacklist = black_packages()
    print("\nAdd packages in blacklist:\n")
    with open(blackfile, "a") as black_conf:
        for pkg in pkgs:
            if pkg not in blacklist:
                print(pkg)
                black_conf.write(pkg + "\n")
                exit = 1
        black_conf.close()
    if exit == 1:
        print # new line at exit

def remove_blacklist(pkgs):
    '''
    Remove packages from blacklist
    '''
    exit = 0
    blackfile = bls_path + "blacklist"
    print("\nRemove packages from blacklist:\n")
    with open(blackfile, "r") as read_black_conf:
        lines = read_black_conf.read()
        read_black_conf.close()
    with open(blackfile, "w") as black_conf:
        for line in lines.splitlines():
            if line not in pkgs:
                black_conf.write(line + "\n")
            else:
                print(line)
                exit = 1
        black_conf.close()
    if exit == 1:
        print # new line at exit
