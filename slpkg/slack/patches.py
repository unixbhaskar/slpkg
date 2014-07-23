#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os

from functions import get_to
from url_read import url_read


def patches(http):
    '''
    Find patches from oficial Slackware mirrors
    '''
    link = url_read(http)
    patches = []
    pkg_patches = []
    for line in link.split():
        if line.startswith("href"):
            line = line.replace("href=\"", "")
            txz = re.findall(".txz", line)
            if txz:
                slack = get_to(line, "\"")
                if slack.endswith(".txz"):
                    patches.append(slack)
    return patches
