#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from slpkg.colors import colors
from slpkg.url_read import url_read
from slpkg.__metadata__ import pkg_path, slpkg_path

from slpkg.pkg.find import find_package
from slpkg.pkg.manager import pkg_upgrade

from mirrors import mirrors

def patches():
    '''
    Install new patches from official Slackware mirrors
    '''
    dwn_list, dwn_patches = [], []
    upgrade_all, package_name, package_location = [], [], []
    os.system("mkdir -p {0}{1}".format(slpkg_path, 'patches/'))
    PACKAGE_TXT = url_read(mirrors(name='PACKAGES.TXT', location='patches/'))
    for line in PACKAGE_TXT.splitlines():
        if line.startswith('PACKAGE NAME'):
            package_name.append(line.replace('PACKAGE NAME:  ', ''))
        if line.startswith('PACKAGE LOCATION'):
            package_location.append(line.replace('PACKAGE LOCATION:  ./', ''))
    for loc, name in zip(package_location, package_name):
        dwn_list.append('{0}{1}/{2}'.format(mirrors('',''), loc, name))
    for pkg in package_name:
        installed_pkg = ''.join(find_package(pkg.replace('.txz', ''), pkg_path))
        if installed_pkg == '':
            upgrade_all.append(pkg)
    if upgrade_all != []:
        print ("\nThese packages need upgrading:\n")
        for upgrade in upgrade_all:
            print ("{0}[ upgrade ] --> {1}{2}".format(
                    colors.GREEN, colors.ENDC, upgrade))
            for dwn in dwn_list:
                if upgrade in dwn:
                    dwn_patches.append(dwn)
        read = raw_input("\nWould you like to upgrade ? [Y/y] ")
        if read == "Y" or read == "y":
            for dwn in dwn_patches:
                os.system("wget -N --directory-prefix={0}{1} {2}".format(
                           slpkg_path, 'patches/', dwn))
            for pkg in upgrade_all:
                print ("{0}[ upgrading ] --> {1}{2}".format(
                        colors.GREEN, colors.ENDC, pkg))
                pkg_upgrade((slpkg_path + 'patches/' + pkg).split())
        read = raw_input("Remove the packages downloaded ? [Y/y] ")
        if read == "Y" or read == "y":
            for pkg in upgrade_all:
                os.remove("{0}{1}{2}".format(slpkg_path, 'patches/', pkg))
                if os.listdir(slpkg_path + 'patches/') == []:
                    print ("Packages removed")
                else:
                    print ("\nThere are packages in direcrory {0}{1}\n".format(
                            slpkg_path, 'patches/'))
        else:
            print ("\nThere are packages in directory {0}{1}\n".format(
                    slpkg_path, 'patches/'))
    else:
        print ("\nYour system is up to date\n")
