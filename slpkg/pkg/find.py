#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def find_package(find_pkg, directory):
    '''
    Find installed packages
    '''
    results = []
    for file in os.listdir(directory):
        if file.startswith(find_pkg + '-'):
            results.append(file)
    return results
