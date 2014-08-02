#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib2

def url_read(link):
    '''
    Open url and read
    '''
    try:
        f = urllib2.urlopen(link)
        return f.read()
    except urllib2.URLError:
        print ("\nError: connection refused\n")
        sys.exit()
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
