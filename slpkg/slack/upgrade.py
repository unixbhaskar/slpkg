#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from dir_patches import dir_patches
from patches import patches
from slack_version import slack_ver
from __metadata__ import arch, packages
from pkg.find import find_package
from colors import colors
from url_read import url_read
from mirrors import mirrors


def upgrade_all():
    upgrades = []
    sum_upgrades = []
    dirs = dir_patches(mirrors(name = ''))
    upgrades.append((patches(mirrors(name = ''))))
    version = slack_ver() 
    tag = "slack" 
    ftype = ".txz"
    updates = []
    slack_type_len = len(arch + tag + version + ftype) + 4
    ftype_len = len(ftype) 
    
    if dirs:
        for d in dirs:
            http = mirrors(d) + "/"
            upgrades.append((patches(http)))
    
    for i in range(len(upgrades)):
        for j in range(len(upgrades[i])):
            sum_upgrades.append(upgrades[i][j])
    
    
    for patch in sum_upgrades:
        print patch
        patch_name = patch[:-ftype_len]
        pkg = ''.join(find_package(patch_name, packages))
        patch = patch.replace(ftype, '')
        if patch > pkg:
            updates.append(patch + ftype)
    if updates != []:
        print ("\nThese packages need upgrading:")
        for update in updates:
            print ("{0}update -->{1} {2}".format(colors.RED, colors.ENDC, update))
        read = raw_input("\nWould you like to upgrade ? [Y/y] ")
        if read == "Y" or read == "y":
            os.system("wget -N " + http + ''.join(updates))
    else:
        print ("Your Slackware system is up to date")
