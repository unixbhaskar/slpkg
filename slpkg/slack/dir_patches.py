#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from functions import get_to
from url_read import url_read

def dir_patches(http):
    '''
    Found directories from patches
    '''
    link = url_read(http)
    folders = []
    patch_dir = []
    dirs = ''
    for line in link.splitlines():
        if re.findall("folder", line):
            folders.append(line)
    for dirs in folders:
        folders = dirs.split()
    for folder in folders:
        if re.findall("href", folder):
            folder = folder.replace("href=\"", "")
            patch_dir.append(get_to(folder, "/"))
    return patch_dir
