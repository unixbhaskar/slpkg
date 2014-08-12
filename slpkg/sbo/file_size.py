#!/usr/bin/python
# -*- coding: utf-8 -*

import os
import sys
import urllib2

def server_file_size(url):
    '''
    Returns the size of remote files
    '''
    try:
        tar = urllib2.urlopen(url)
        meta = tar.info()
        return meta.getheaders("Content-Length")
    except urllib2.URLError:
        print ("\nError: connection refused\n")
        sys.exit()
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()

def local_file_size(registry):
    '''
    Returns the size of local files
    '''
    return os.path.getsize(registry)
