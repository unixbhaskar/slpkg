#!/usr/bin/python
# -*- coding: utf-8 -*-

from slpkg.__metadata__ import arch
from slack_version import slack_ver

def mirrors(name, location):
    '''
    Select Slackware mirror packages
    based architecture
    '''
    if arch == "x86_64":
        http = "http://mirrors.slackware.com/slackware/slackware64-{0}/{1}{2}".format(
                slack_ver(), location, name)
    else:
        http = "http://mirrors.slackware.com/slackware/slackware-{0}/{1}{3}".format(
                slack_ver(), location, name)
    return http
