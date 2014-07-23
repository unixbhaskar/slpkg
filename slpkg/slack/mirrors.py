#!/usr/bin/python
# -*- coding: utf-8 -*-

from __metadata__ import uname, arch

def mirrors(name):
    '''
    Choose Slackware mirror based
    architecture
    '''
    if arch == "x86_64":
        http = "http://mirrors.slackware.com/slackware/slackware64-14.1/patches/packages/" + name
    else:
        http = "http://mirrors.slackware.com/slackware/slackware-14.1/patches/packages/" + name
    return http

 
