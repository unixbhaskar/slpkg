#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from colors import colors
from __metadata__ import __prog__

def pkg_not_found(pkg, message):
    '''
    Print message when package not found
    '''
    print ("\n{0}: No such package {1}: {2}\n".format(__prog__, pkg, message))

def pkg_found(pkg):
    '''
    Print message when package found
    '''
    print ("| {0}: package {1} is already installed".format(__prog__, pkg))

def pkg_installed(pkg):
    '''
    Print message when package installed
    '''
    print ("| {0}: package {1} installed".format(__prog__, pkg))

def s_user(user):
    '''
    Check for root user
    '''
    if user != "root":
        print ("{0}: error: must have root privileges".format(__prog__))
        sys.exit()

def template(max):
    '''
    Print view template
    '''
    print ("+" + "=" * max)

def view_sbo(pkg, sbo_url, sbo_dwn, source_dwn, extra_dwn, sbo_req):
    print ("\n")
    template(78)
    print ("| {0}The {1}`{2}`{3} found in --> {4}".format(colors.GREEN,
            colors.CYAN, pkg, colors.GREEN, colors.ENDC + sbo_url))
    template(78)
    print ("| {0}Download SlackBuild : {1}{2}".format(colors.GREEN, colors.ENDC, sbo_dwn))
    print ("| {0}Source Downloads : {1}{2}".format(colors.GREEN, colors.ENDC, source_dwn))
    print ("| {0}Extra Downloads : {1}{2}".format(colors.GREEN, colors.ENDC, extra_dwn))
    print ("| {0}Package requirements : {1}{2}".format(colors.YELLOW, colors.ENDC, sbo_req))
    template(78)
    print (" {0}R{1}EADME               View the README file".format(colors.RED, colors.ENDC))
    print (" {0}S{1}lackBuild           View the SlackBuild file".format(colors.RED, colors.ENDC))
    print (" In{0}f{1}o                 View the Info file".format(colors.RED, colors.ENDC))
    print (" {0}D{1}ownload             Download this package".format(colors.RED, colors.ENDC))
    print (" {0}B{1}uild                Download and build".format(colors.RED, colors.ENDC))
    print (" {0}I{1}nstall              Download/Build/Install\n".format(colors.RED, colors.ENDC))

