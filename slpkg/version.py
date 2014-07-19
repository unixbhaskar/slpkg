#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "dslackw"
__version_info__ = (1, 5, 9)
__version__ = "{0}.{1}.{2}".format(*__version_info__)
__license__ = "GNU General Public License v3 (GPLv3)"
__email__ = "d.zlatanidis@gmail.com"

def pkg_version():
    '''
    Print version, license and email
    '''
    print ("Version : {}".format(__version__))
    print ("Licence : {}".format(__license__))
    print ("Email   : {}".format(__email__))

