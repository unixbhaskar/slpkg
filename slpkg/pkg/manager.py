#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import getpass
import subprocess

from slpkg.colors import colors
from slpkg.messages import pkg_not_found, s_user, template
from slpkg.__metadata__ import packages, __prog__, uname, arch

from find import find_package

def pkg_install(binary):
    '''
    Install Slackware binary packages
    '''
    s_user(getpass.getuser())
    for pkg in range(len(binary)):
        try:
            print subprocess.check_output('installpkg {0}'.format(binary[pkg]), shell=True)
        except subprocess.CalledProcessError:
            pkg_not_found(binary[pkg], message="Can't install")

def pkg_upgrade(binary):
    '''
    Upgrade Slackware binary packages
    '''
    s_user(getpass.getuser())
    for pkg in range(len(binary)):
        try:
            print subprocess.check_output('upgradepkg --install-new {0}'.format(binary[pkg]),
                                           shell=True)
        except subprocess.CalledProcessError:
            pkg_not_found(binary[pkg], message="Can't upgrade")

def pkg_reinstall(binary):
    '''
    Reinstall Slackware binary packages
    '''
    s_user(getpass.getuser())
    for pkg in range(len(binary)):
        try:
            print subprocess.check_output('upgradepkg --reinstall {0}'.format(binary[pkg]),
                                           shell=True)
        except subprocess.CalledProcessError:
            pkg_not_found(binary[pkg], message="Can't reinstall")

def pkg_remove(binary):
    '''
    Unistall Slackware binary packages
    '''
    s_user(getpass.getuser())
    pkgs = []
    for pkg in range(len(binary)):
        if find_package(binary[pkg], packages) == []:
             pkg_not_found(binary[pkg], message="Can't remove")
        else:
            pkgs.append(binary[pkg])
    if pkgs == []:
        sys.exit()
    count = []
    for pkg in range(len(binary)):
        pkgs = find_package(binary[pkg], packages)
        print # new line at start
        if pkgs != []:
            print (colors.RED + "delete --> " + colors.ENDC + "\n           ".join(pkgs))
            count.append(pkgs)
    sum_pkgs = 0
    for i in range(len(count)):
        sum_pkgs += len(count[i])
    remove_pkg = raw_input("\nAre you sure to remove " + str(sum_pkgs) + " package(s) [Y/y] ")
    if remove_pkg == "y" or remove_pkg == "Y":
        results_removed = []
        not_found = []
        for pkg in range(len(binary)):
            if find_package(binary[pkg], packages) == []:
                not_found.append(binary[pkg])
            else:
                try:
                    results_removed.append("".join(find_package(binary[pkg], packages)))
                    print subprocess.check_output('removepkg {0}'.format(binary[pkg]),
                                                   shell=True)
                except subprocess.CalledProcessError:
                    file_not_found(binary[pkg])
        template(78)
        for file in results_removed:
            if find_package(file, packages) == []:
                print ("| {0}: package: {1} removed".format(__prog__, file))
        for file in not_found:
            print ("| {0}: package: {1} not found".format(__prog__, file))
        template(78)
        print # new line at end

def pkg_find(binary):
    '''
    Find installed Slackware packages
    '''
    for pkg in range(len(binary)):
        if find_package(binary[pkg], packages) == []:
            pkg_not_found(binary[pkg], message="Can't find")
        else:
            print (colors.GREEN + "found --> " + colors.ENDC + "\n          ".join(
                   find_package(binary[pkg], packages)))

def pkg_display(binary):
    '''
    Print the Slackware packages contents
    '''
    for pkg in range(len(binary)):
        if find_package(binary[pkg], packages) == []:
            pkg_not_found(binary[pkg], message="Can't find")
        else:
            print subprocess.check_output("cat {0}{1}".format(packages,
                  " /var/log/packages/".join(find_package(binary[pkg], packages))), shell=True)

def pkg_list(binary):
    '''
    List with the installed packages
    '''
    if "all" in binary:
        print
        os.chdir(packages)
        os.system("ls * | more")
        print
    if "sbo" in binary:
        print
        os.chdir(packages)
        os.system("ls * | grep 'SBo' | more")
        print
