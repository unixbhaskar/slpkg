#!/usr/bin/python
# -*- coding: utf-8 -*-

from slpkg.colors import colors
from slpkg.messages import pkg_not_found, template

from greps import *
from search import sbo_search_pkg
from download import sbo_slackbuild_dwn

dep_links_results = []
dep_results = []

def sbo_dependencies_pkg(name):
    '''
    Search for package dependecies
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

def sbo_dependencies_links_pkg(name):
    '''
    Search for packages dependecies links
    '''
    if name != "%README%":
        sbo_url = sbo_search_pkg(name)
        if sbo_url is None:
            message = "From slackbuilds.org"
            bol, eol = "\n", "\n"
            pkg_not_found(bol, name, message, eol)
        else:
            version = ("@" + sbo_version_pkg(sbo_url, name)).split()
            sbo_dwn = sbo_slackbuild_dwn(sbo_url, name).split()
            source_dwn = sbo_source_dwn(sbo_url, name).split()
            extra_dwn = sbo_extra_dwn(sbo_url, name)
            sbo_req = sbo_requires_pkg(sbo_url, name).split()
            if extra_dwn != []:
                flag = ("extra" + str(len(extra_dwn))).split()
                dep_links_results.append(flag)
            dep_links_results.append(extra_dwn)
            dep_links_results.append(version)
            dep_links_results.append(source_dwn)
            dep_links_results.append(sbo_dwn)
            if sbo_req != []:
                dep_links_results.append(sbo_req)
            for line in sbo_req:
                sbo_dependencies_links_pkg(line)
            return dep_links_results

def pkg_tracking(name):
    '''
    Find package dependecies and print all
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
