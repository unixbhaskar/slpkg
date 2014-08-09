#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def find_package(find_pkg, directory):
    '''
    Find packages
    '''
    pkgs = []
    for pkg in os.listdir(directory):
        if pkg.startswith(find_pkg):
            pkgs.append(pkg)
    return pkgs
