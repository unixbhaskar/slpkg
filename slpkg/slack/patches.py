#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from url_read import url_read
from mirrors import mirrors
from slack_version import slack_ver
from pkg.find import find_package
from __metadata__ import packages, dwn_path
from colors import colors
from pkg.manager import pkg_upgrade

def patches():
    '''
    Install new patches from official Slackware
    '''
    dwn_list = []
    dwn_patches = []
    upgrade_all = []
    package_name = []
    package_location = []
    os.system("mkdir -p {0}{1}".format(dwn_path, 'patches/'))
    PACKAGE_TXT = url_read(mirrors(name='PACKAGES.TXT', location='patches/'))
    for line in PACKAGE_TXT.splitlines():
        if line.startswith('PACKAGE NAME'):
            package_name.append(line.replace('PACKAGE NAME:  ', ''))
        if line.startswith('PACKAGE LOCATION'):
            package_location.append(line.replace('PACKAGE LOCATION:  ./', ''))
    for loc, name in zip(package_location, package_name):
        dwn_list.append('{0}{1}/{2}'.format(mirrors('',''), loc, name))
    for pkg in package_name:
        installed_pkg = ''.join(find_package(pkg.replace('.txz', ''), packages))
        if installed_pkg == '':
            upgrade_all.append(pkg)
    if upgrade_all != []:
        print ("\nThese packages need upgrading:\n")
        for upgrade in upgrade_all:
            print ("{0}[ upgrade ] --> {1}{2}".format(colors.CYAN, colors.ENDC, upgrade))
            for dwn in dwn_list:
                if upgrade in dwn:
                    dwn_patches.append(dwn)
        read = raw_input("\nWould you like to download ? [Y/y] ")
        if read == "Y" or read == "y":
            for dwn in dwn_patches:
                os.system("wget -N --directory-prefix={0}{1} {2}".format(dwn_path, 'patches/', dwn))
