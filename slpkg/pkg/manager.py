#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import getpass
import subprocess

from ..colors import colors
from ..functions import s_user

from find import find_package

packages = "/var/log/packages/"

def pkg_install(name):
    '''
    Install Slackware binary packages
    '''
    s_user(getpass.getuser())
    for i in range(len(name)):
        try:
            print subprocess.check_output('installpkg %s' % name[i], shell=True)
        except subprocess.CalledProcessError:
            print ("\n{}Cannot install {}`{}`{} file not found\n{}".format(colors.RED,
                    colors.CYAN, name[i], colors.RED, colors.ENDC))

def pkg_upgrade(name):
    '''
    Upgrade Slackware binary packages
    '''
    s_user(getpass.getuser())
    for i in range(len(name)):
        try:
            print subprocess.check_output('upgradepkg --install-new %s' % name[i], shell=True)
        except subprocess.CalledProcessError:
            print ("\n{}Cannot install {}`{}`{} file not found\n{}".format(colors.RED,
                    colors.CYAN, name[i], colors.RED, colors.ENDC))

def pkg_reinstall(name):
    '''
    Reinstall Slackware binary packages
    '''
    s_user(getpass.getuser())
    for i in range(len(name)):
        try:
            print subprocess.check_output('upgradepkg --reinstall %s' % name[i], shell=True)
        except subprocess.CalledProcessError:
            print ("\n{}Cannot install {}`{}`{} file not found\n{}".format(colors.RED,
                    colors.CYAN, name[i], colors.RED, colors.ENDC))

def pkg_remove(name):
    '''
    Unistall Slackware binary packages
    '''
    s_user(getpass.getuser())
    pkg = []
    for i in range(len(name)):
        if find_package(name[i], packages) == []:
            print ("{}The package {}`{}`{} not found{}".format(colors.CYAN, colors.ENDC,
                    name[i], colors.CYAN, colors.ENDC))
        else:
            pkg.append(name[i])
    if pkg == []:
        sys.exit()
    print ("These package(s) will be deleted:")
    count = []
    for i in range(len(name)):
        pkg = find_package(name[i], packages)
        if pkg != []:
            print colors.RED + '\n'.join(pkg) + colors.ENDC
            count.append(pkg)
    sum_pkgs = 0
    for i in range(len(count)):
        sum_pkgs += len(count[i])
    if sum_pkgs > 1:
        print ("{} packages matching".format(sum_pkgs))
        print ("Perhaps you need to specify the package")
        print ("Example: slpkg -r pip-1.5.6")
    remove_pkg = raw_input("Are you sure to remove this package(s) [Y/y] ")
    if remove_pkg == "y" or remove_pkg == "Y":
        results_removed = []
        not_found = []
        for i in range(len(name)):
            if find_package(name[i], packages) == []:
                not_found.append(name[i])
            else:
                os.system("removepkg {}".format(name[i]))
                results_removed.append(name[i])
        print
        for file in results_removed:
            if find_package(file, packages) == []:
                print ("{}The package {}`{}`{} removed{}".format(colors.YELLOW,
                        colors.CYAN, file,colors.YELLOW, colors.ENDC))
        for file in not_found:
            print ("{}The package {}`{}`{} not found{}".format(colors.RED, colors.CYAN,
                    file, colors.RED, colors.ENDC))
    print

def pkg_find(name):
    '''
    Find installed Slackware packages
    '''
    print
    for i in range(len(name)):
        if find_package(name[i], packages) == []:
            print ("{}The package {}`{}`{} not found{}".format(colors.RED, colors.CYAN,
                    name[i], colors.RED, colors.ENDC))
        else:
            print (colors.GREEN + "found --> " + colors.ENDC + "\n".join(find_package(
                   name[i], packages)))
    print

def pkg_display(name):
    '''
    Print the Slackware packages contents
    '''
    print
    for i in range(len(name)):
        if find_package(name[i], packages) == []:
            print ("{}The package {}`{}`{} not found{}".format(colors.RED, colors.CYAN,
                    name[i], colors.RED, colors.ENDC))
        else:
            os.system("cat {}{}".format(packages, "\n".join(find_package(name[i], packages))))
    print

def pkg_list(name):
    '''
    List with the installed packages
    '''
    if "all" in name:
        print
        os.chdir(packages)
        os.system("ls * | more")
        print
    if "sbo" in name:
        print
        os.chdir(packages)
        os.system("ls * | grep 'SBo' | more")
        print
