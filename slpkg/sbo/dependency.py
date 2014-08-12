#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from slpkg.colors import colors
from slpkg.__metadata__ import pkg_path, sp
from slpkg.messages import pkg_not_found, template

from slpkg.pkg.find import find_package

from greps import *
from search import sbo_search_pkg
from download import sbo_slackbuild_dwn

dep_results = []

def sbo_dependencies_pkg(name):
    '''
    Build tree of dependencies
    '''
    try:
        if name is not "%README%":
            sbo_url = sbo_search_pkg(name)
            if sbo_url is None:
                message = "From slackbuilds.org"
                bol, eol = "", "\n"
                pkg_not_found(bol, name, message, eol)
            else:
                sbo_req = sbo_requires_pkg(sbo_url, name)
                dependencies = sbo_req.split()
                if dependencies:
                    dep_results.append(dependencies)
                for line in dependencies:
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    sbo_dependencies_pkg(line)
                return dep_results
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()

def pkg_tracking(name):
    '''
    Print tree of dependencies
    '''
    sys.stdout.write ('Reading package lists.')
    dependencies_list = sbo_dependencies_pkg(name)
    sys.stdout.write(' Done\n')
    if dependencies_list is None:
        pass
    elif dependencies_list == []:
        print ("\nPackage {0} no dependencies\n".format(name))
    else:
        print # new line at start
        requires, dependencies = [], []
        for pkg in dependencies_list:
            requires += pkg
        requires.reverse()
        for duplicate in requires:
            if duplicate not in dependencies:
                dependencies.append(duplicate)
        pkg_len = len(name) + 24
        template(pkg_len)
        print ("| Package {0}{1}{2} dependencies :".format(colors.CYAN, name,
                                                           colors.ENDC))
        template(pkg_len)
        #clear_dependencies.reverse()
        print ("\\")
        print (" +---{0}[ Tree of dependencies ]{1}".format(colors.YELLOW, colors.ENDC))
        index = 0
        for pkg in dependencies:
            index += 1
            if find_package(pkg + sp, pkg_path):
                print (" |")
                print (" {0}{1}: {2}{3}{4}".format("+--", index, colors.GREEN, pkg, colors.ENDC))
            else:
                print (" |")
                print (" {0}{1}: {2}{3}{4}".format("+--", index, colors.RED, pkg, colors.ENDC))
        print ("\n NOTE: green installed, red not installed\n")
