#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2

def url_read(name):
    '''
    Open url and read
    '''
    try:
        f = urllib2.urlopen(name)
        return f.read()
    except urllib2.URLError:
        print ("\nslpkg: error: connection refused")
        sys.exit()
