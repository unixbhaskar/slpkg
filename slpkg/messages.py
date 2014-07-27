#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from colors import colors

def pkg_not_found(bol, pkg, message, eol):
    '''
    Print message when package not found
    '''
    print ("{0}No such package {1}: {2}{3}".format(bol, pkg, message, eol))

def pkg_found(pkg):
    '''
    Print message when package found
    '''
    print ("| Package {0} is already installed".format(pkg))

def pkg_installed(pkg):
    '''
    Print message when package installed
    '''
    print ("| Package {0} installed".format(pkg))

def err_args(bol, eol):
    '''
    Print error message arguments
    '''
    print ("{0}Error: must enter at least two arguments{1}".format(bol, eol))

def s_user(user):
    '''
    Check for root user
    '''
    if user != "root":
        print ("\nError: must have root privileges\n")
        sys.exit()

def template(max):
    '''
    Print view template
    '''
    print ("+" + "=" * max)

def view_sbo(pkg, sbo_url, sbo_dwn, source_dwn, extra_dwn, sbo_req):
    print # new line at start
    template(78)
    print ("| {0}Package {1}{2}{3} --> {4}".format(colors.GREEN,
            colors.CYAN, pkg, colors.GREEN, colors.ENDC + sbo_url))
    template(78)
    print ("| {0}SlackBuild : {1}{2}".format(colors.GREEN, colors.ENDC, sbo_dwn))
    print ("| {0}Source : {1}{2}".format(colors.GREEN, colors.ENDC, source_dwn))
    print ("| {0}Extra : {1}{2}".format(colors.GREEN, colors.ENDC, extra_dwn))
    print ("| {0}Requirements : {1}{2}".format(colors.YELLOW, colors.ENDC,
                                               ", ".join(sbo_req.split())))
    template(78)
    print (" {0}R{1}EADME               View the README file".format(colors.RED, colors.ENDC))
    print (" {0}S{1}lackBuild           View the SlackBuild file".format(colors.RED, colors.ENDC))
    print (" In{0}f{1}o                 View the Info file".format(colors.RED, colors.ENDC))
    print (" {0}D{1}ownload             Download this package".format(colors.RED, colors.ENDC))
    print (" {0}B{1}uild                Download and build".format(colors.RED, colors.ENDC))
    print (" {0}I{1}nstall              Download/Build/Install\n".format(colors.RED, colors.ENDC))
