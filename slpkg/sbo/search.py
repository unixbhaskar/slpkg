#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
from colors import colors
from url_read import url_read
from functions import get_file

from slack.slack_version import slack_ver

def sbo_search_pkg(name):
    '''
    Find SlackBuilds packages links from repository slackbuilds.org
    '''
    sbo_location = []
    print ('Searching {0}[ {1} ]{2} from slackbuilds.org ...'.format(
            colors.CYAN, name, colors.ENDC))
    sbo_url = ("http://slackbuilds.org/repository/{0}/".format(slack_ver()))
    SLACKBUILDS_TXT = url_read(("http://slackbuilds.org/slackbuilds/{0}/SLACKBUILDS.TXT".format(
                                 slack_ver())))
    for line in SLACKBUILDS_TXT.splitlines():
        if line.startswith('SLACKBUILD LOCATION'):
            sbo_location.append(line.replace('SLACKBUILD LOCATION: ./', ''))
    for loc in sbo_location:
        if get_file(loc, '/') == name:
            return sbo_url + loc.replace(name, '') + name + "/"
    
