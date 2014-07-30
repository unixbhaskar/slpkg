#!/usr/bin/python
# -*- coding: utf-8 -*-

from slpkg.colors import colors
from slpkg.messages import pkg_not_found, template

from greps import *
from search import sbo_search_pkg
from download import sbo_slackbuild_dwn

dep_results = []

def sbo_dependencies_pkg(name):
    '''
    Build tree of dependencies
    '''
    if name != "%README%":
        sbo_url = sbo_search_pkg(name)
        if sbo_url is None:
            message = "From slackbuilds.org"
            bol, eol = "\n", "\n"
            pkg_not_found(bol, name, message, eol)
        else:
            sbo_req = sbo_requires_pkg(sbo_url, name)
            dependencies = sbo_req.split()
            if dependencies != []:
                dep_results.append(dependencies)
            for line in dependencies:
                sbo_dependencies_pkg(line)
            return dep_results

def pkg_tracking(name):
    '''
    Print tree of dependencies
    '''
    dependencies = sbo_dependencies_pkg(name)
    if dependencies is None:
        pass
    elif dependencies == []:
        print ("\nPackage {0} no dependencies\n".format(name))
    else:
        print # new line at start
        pkg_len = len(name) + 24
        template(pkg_len)
        print ("| Package {0}{1}{2} dependencies :".format(colors.CYAN, name,
                                                           colors.ENDC))
        template(pkg_len)
        dependencies.reverse()
        print ("\\")
        print (" +---{0}[ Tree of dependencies ]{1}".format(colors.YELLOW, colors.ENDC))
        for i in range(len(dependencies)):
            print (" |")
            print (" ".join((" +--", str(len(dependencies[i])),
            ", ".join(dependencies[i]))))
        print # new line at end
