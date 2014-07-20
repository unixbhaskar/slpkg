#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys

from ..url_read import url_read
from ..functions import rmv_unused

from repository import repository

def sbo_search_pkg(name):
    '''
    Find SlackBuilds packages links from repository slackbuilds.org
    '''
    sbo_url = "http://slackbuilds.org/repository/14.1/"
    search_name = re.escape(name)
    search_name = ">" + search_name + "<"
    toolbar_width = len(repository)
    sys.stdout.write("Searching `" + name + "` from slackbuilds.org .%s " %
                    (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))
    for kind in repository:
        sys.stdout.write(".")
        sys.stdout.flush()
        sbo_url_sub = sbo_url + kind + "/"
        find_SBo = re.findall(search_name, url_read(sbo_url_sub))
        find_SBo = rmv_unused(" ".join(find_SBo))
        if name in find_SBo:
            return sbo_url_sub + name + "/"
