#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import getpass
import subprocess

from ..colors import colors
from ..messages import file_not_found, s_user, template
from ..__metadata__ import packages, __prog__, uname, arch

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
            file_not_found(binary[pkg])

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
            file_not_found(binary[pkg])

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
            file_not_found(binary[pkg])

def pkg_remove(binary):
    '''
    Unistall Slackware binary packages
    '''
    s_user(getpass.getuser())
    pkgs = []
    for pkg in range(len(binary)):
        if find_package(binary[pkg], packages) == []:
             file_not_found(binary[pkg])
        else:
            pkgs.append(binary[pkg])
    if pkgs == []:
        sys.exit()
    print ("These package(s) will be deleted:")
    count = []
    for pkg in range(len(binary)):
        pkgs = find_package(binary[pkg], packages)
        if pkgs != []:
            sbo_tag_len = len(arch) + 7
            found_pkg = pkgs[0][:-sbo_tag_len]
            print (colors.RED + found_pkg + colors.ENDC)
            count.append(pkgs)
    sum_pkgs = 0
    for i in range(len(count)):
        sum_pkgs += len(count[i])
    print ("{0}{1} package marked{2}".format(colors.GREEN, sum_pkgs, colors.ENDC))
    remove_pkg = raw_input("Are you sure to remove this package(s) [Y/y] ")
    if remove_pkg == "y" or remove_pkg == "Y":
        results_removed = []
        not_found = []
        for pkg in range(len(binary)):
            if find_package(binary[pkg], packages) == []:
                not_found.append(binary[pkg])
            else:
                try:
                    print subprocess.check_output('removepkg {0}'.format(binary[pkg]),
                                                   shell=True)
                except subprocess.CalledProcessError:
                    file_not_found(binary[pkg])
                results_removed.append(binary[pkg])
        template(78)
        for file in results_removed:
            if find_package(file, packages) == []:
                print ("| {0}: package: {1} removed".format(__prog__, file))
        for file in not_found:
            print ("| {0}: package: {1} not found".format(__prog__, file))
        template(78)
        print

def pkg_find(binary):
    '''
    Find installed Slackware packages
    '''
    print
    for pkg in range(len(binary)):
        if find_package(binary[pkg], packages) == []:
            print ("{0}: package: {1} not found".format(__prog__, binary[pkg]))
        else:
            found_pkg = find_package(binary[pkg], packages)
            sbo_tag_len = len(arch) + 7
            found_pkg = found_pkg[0][:-sbo_tag_len]
            print (__prog__ + ": package: " + colors.GREEN + "found --> " + colors.ENDC + found_pkg)
    print

def pkg_display(binary):
    '''
    Print the Slackware packages contents
    '''
    for pkg in range(len(binary)):
        if find_package(binary[pkg], packages) == []:
            file_not_found(binary[pkg])
        else:
            print subprocess.check_output("cat {0}{1}".format(packages,
                  "\n".join(find_package(binary[pkg], packages))), shell=True)

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
