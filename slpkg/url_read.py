#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
from __metadata__ import __prog__

def url_read(link):
    '''
    Open url and read
    '''
    try:
        f = urllib2.urlopen(link)
        return f.read()
    except urllib2.URLError:
        print ("\n{0}: error: connection refused".format(__prog__))
        sys.exit()
