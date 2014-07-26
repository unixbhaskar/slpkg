#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

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
