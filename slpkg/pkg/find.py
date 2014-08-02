#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def find_package(find_pkg, directory):
    '''
    Find installed packages from
    /var/log/packages/
    '''
    results = []
    for pkg in os.listdir(directory):
        if pkg.startswith(find_pkg):
            results.append(pkg)
    return results
