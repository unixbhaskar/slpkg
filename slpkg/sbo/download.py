#!/usr/bin/python
# -*- coding: utf-8 -*-

def sbo_slackbuild_dwn(sbo_url, name):
    '''
    Find SlackBuilds packages links for download
    '''
    sbo_url = sbo_url.replace(name + "/", name + ".tar.gz")
    return sbo_url.replace("repository", "slackbuilds")
