#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import getpass
import subprocess

from collections import OrderedDict

from slpkg.colors import colors
from slpkg.messages import pkg_not_found, s_user, template
from slpkg.__metadata__ import pkg_path, uname, arch, sp, log_path

from find import find_package

def pkg_install(binary):
    '''
    Install Slackware binary packages
    '''
    s_user(getpass.getuser())
    for pkg in binary:
        try:
            print subprocess.check_output('installpkg {0}'.format(pkg), shell=True)
        except subprocess.CalledProcessError:
            message = "Can't install"
            if len(binary) > 1:
                bol, eol = "", ""
            else:
                bol, eol = "\n", "\n"
            pkg_not_found(bol, pkg, message, eol)

def pkg_upgrade(binary):
    '''
    Upgrade Slackware binary packages
    '''
    s_user(getpass.getuser())
    for pkg in binary:
        try:
            print subprocess.check_output('upgradepkg --install-new {0}'.format(pkg),
                                           shell=True)
        except subprocess.CalledProcessError:
            message = "Can't upgrade"
            if len(binary) > 1:
                bol, eol = "", ""
            else:
                bol, eol = "\n", "\n"
            pkg_not_found(bol, pkg, message, eol)

def pkg_reinstall(binary):
    '''
    Reinstall Slackware binary packages
    '''
    s_user(getpass.getuser())
    for pkg in binary:
        try:
            print subprocess.check_output('upgradepkg --reinstall {0}'.format(pkg),
                                           shell=True)
        except subprocess.CalledProcessError:
            message = "Can't reinstall"
            if len(binary) > 1:
                bol, eol = "", ""
            else:
                bol, eol = "\n", "\n"
            pkg_not_found(bol, pkg, message, eol)

def pkg_remove(binary):
    '''
    Remove Slackware binary packages
    '''
    s_user(getpass.getuser())
    removed, not_found, dependencies, rmv_dependencies = [], [], [], []
    print ("\nPackages with name matching [ {0}{1}{2} ]\n".format(
        colors.CYAN, ', '.join(binary), colors.ENDC))
    for pkg in binary:
        pkgs = find_package(pkg + sp, pkg_path)
        if pkgs:
            print (colors.RED + "[ delete ] --> " + colors.ENDC + "\n               ".join(pkgs))
            removed.append(pkg)
        else:
            message = "Can't remove"
            bol, eol = "", ""
            not_found.append(pkg)
            pkg_not_found(bol, pkg, message, eol)
    if removed == []:
        print # new line at end
    else:
        msg = "package"
        if len(removed) > 1:
            msg = msg + "s"
        try:
            remove_pkg = raw_input("\nAre you sure to remove {0} {1} [Y/y] ".format(
                                    str(len(removed)), msg))
        except KeyboardInterrupt:
            print # new line at exit
            sys.exit()
        if remove_pkg == "y" or remove_pkg == "Y":
            for rmv in removed:
                '''
                If package build and install with 'slpkg -s sbo <package>'
                then look log file for dependencies in /var/log/slpkg/dep,
                read and remove all else remove only the package.
                '''
                if find_package(rmv, log_path + "dep/"):
                    f = open("{0}dep/{1}".format(log_path, rmv), "r")
                    dependencies = f.read().split()
                    print # new line at start
                    template(78)
                    print ("| Found dependencies for package {0}:".format(rmv))
                    template(78)
                    '''
                    Prints dependecies before removed except master package
                    because referred as master package
                    '''
                    for dep in dependencies[:-1]:
                        print ("| " + dep)
                    template(78)
                    try:
                        remove_dep = raw_input("\nRemove dependencies [Y/y] ")
                    except KeyboardInterrupt:
                        print # new line at exit
                        sys.exit()
                    if remove_dep == "y" or remove_dep == "Y":
                        for dep in dependencies:
                            if find_package(dep + sp, pkg_path):
                                print subprocess.check_output('removepkg {0}'.format(dep), shell=True)
                        f.close()
                        os.remove("{0}dep/{1}".format(log_path, rmv))
                        rmv_dependencies += dependencies[:-1]
                    else:
                        if find_package(rmv + sp, pkg_path):
                            print subprocess.check_output('removepkg {0}'.format(rmv), shell=True)
                        f.close()
                        os.remove("{0}dep/{1}".format(log_path, rmv))
                else:
                    if find_package(rmv + sp, pkg_path):
                        print subprocess.check_output('removepkg {0}'.format(rmv), shell=True)
            '''
            Prints all removed packages
            '''
            removed = removed + rmv_dependencies
            template(78)
            for pkg in list(OrderedDict.fromkeys(removed)):
                if find_package(pkg + sp, pkg_path) == []:
                    print ("| Package {0} removed".format(pkg))
            for pkg in not_found:
                print ("| Package {0} not found".format(pkg))
            template(78)
        print # new line at end

def pkg_find(binary):
    '''
    Find installed Slackware packages
    '''
    print ("\nPackages with name matching [ {0}{1}{2} ]\n".format(
            colors.CYAN, ', '.join(binary), colors.ENDC))
    for pkg in binary:
        if find_package(pkg + sp, pkg_path) == []:
            message = "Can't find"
            bol, eol = "", ""
            pkg_not_found(bol, pkg, message, eol)
        else:
            print (colors.GREEN + "[ installed ] - " + colors.ENDC + "\n                ".join(
                   find_package(pkg + sp, pkg_path)))
    print # new line at end

def pkg_display(binary):
    '''
    Print the Slackware packages contents
    '''
    for pkg in binary:
        if find_package(pkg + sp, pkg_path) == []:
            message = "Can't dislpay"
            if len(binary) > 1:
                bol, eol = "", ""
            else:
                bol, eol = "\n", "\n"
            pkg_not_found(bol, pkg, message, eol)
        else:
            print subprocess.check_output("cat {0}{1}".format(pkg_path,
                  " /var/log/packages/".join(find_package(pkg +sp, pkg_path))), shell=True)

def pkg_list(binary):
    '''
    List with the installed packages
    '''
    try:
        print # new line at start
        index, page = 0, 50
        if "all" in binary:
            for pkg in os.listdir(pkg_path):
                index += 1
                print ("{0}{1}:{2} {3}".format(colors.GREY, index, colors.ENDC, pkg))
                if index == page:
                    key = raw_input('\nPress [ {0}Enter{1} ] >> Next page '.format(
                                     colors.CYAN, colors.ENDC))
                    page += 50
        if "sbo" in binary:
            for pkg in os.listdir(pkg_path):
                if 'SBo' in pkg:
                    index += 1
                    print ("{0}{1}:{2} {3}".format(colors.GREY, index, colors.ENDC, pkg))
                    if index == page:
                        key = raw_input('\nPress [ {0}Enter{1} ] >> Next page '.format(
                                         colors.CYAN, colors.ENDC))
                        page += 50
        if "slack" in binary:
            for pkg in os.listdir(pkg_path):
                if 'slack' in pkg:
                    index += 1
                    print ("{0}{1}:{2} {3}".format(colors.GREY, index, colors.ENDC, pkg))
                    if index == page:
                        key = raw_input('\nPress [ {0}Enter{1} ] >> Next page '.format(
                                         colors.CYAN, colors.ENDC))
                        page += 50
        if "noarch" in binary:
            for pkg in os.listdir(pkg_path):
                if 'noarch' in pkg:
                    index += 1
                    print ("{0}{1}:{2} {3}".format(colors.GREY, index, colors.ENDC, pkg))
                    if index == page:
                        key = raw_input('\nPress [ {0}Enter{1} ] >> Next page '.format(
                                         colors.CYAN, colors.ENDC))
                        page += 50
        if "other" in binary:
            for pkg in os.listdir(pkg_path):
                if 'SBo' in pkg or 'slack' in pkg or 'noarch' in pkg:
                    pass
                else:
                    index += 1
                    print ("{0}{1}:{2} {3}".format(colors.GREY, index, colors.ENDC, pkg))
                    if index == page:
                        key = raw_input('\nPress [ {0}Enter{1} ] >> Next page '.format(
                                         colors.CYAN, colors.ENDC))
                        page += 50
        print # new line at end
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
