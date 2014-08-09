#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
from slpkg.colors import colors
from slpkg.url_read import url_read
from slpkg.functions import get_file

from slpkg.slack.slack_version import slack_ver

def sbo_search_pkg(name):
    '''
    Find SlackBuilds packages from slackbuilds.org
    '''
    try:
        sbo_location = []
        sbo_url = ("http://slackbuilds.org/slackbuilds/{0}/".format(slack_ver()))
        SLACKBUILDS_TXT = url_read((
        "http://slackbuilds.org/slackbuilds/{0}/SLACKBUILDS.TXT".format(slack_ver())))
        for line in SLACKBUILDS_TXT.splitlines():
            if line.startswith('SLACKBUILD LOCATION'):
                sbo_location.append(line.replace('SLACKBUILD LOCATION: ./', ''))
        for loc in sbo_location:
            if get_file(loc, '/') == name:
                print ('{0}[ found ] --> {1}{2}'.format(colors.CYAN, colors.ENDC, name))
                return sbo_url + loc.replace(name, '') + name + "/"
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
