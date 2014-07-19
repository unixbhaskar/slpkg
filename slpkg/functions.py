#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from colors import colors

def s_user(user):
    '''
    Check for root user
    '''
    if user != "root":
        print ("\n{}Must have {}`root`{} privileges ...{}\n".format(
                colors.RED, colors.GREEN, colors.RED, colors.ENDC))
        sys.exit()

def rmv_unused(name):
    '''
    Remove unused chars
    '''
    rmv = "><"
    for ch in rmv:
        name = name.replace(ch, "")
    return name

def get_file(link, char):
    '''
    Get filename from links
    '''
    i = 0
    results = []
    for file in range(len(link)):
        i -= 1
        results.append(link[i])
        if link[i] == char:
            break
    return ''.join(results[::-1]).replace('/', '').strip(' ')
