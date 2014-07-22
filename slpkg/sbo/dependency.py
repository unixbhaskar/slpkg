#!/usr/bin/python
# -*- coding: utf-8 -*-

from slpkg.colors import colors
from slpkg.__metadata__ import __prog__
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
            pkg_not_found(name, message="Can't find")
        else:
            sbo_req = sbo_requires_pkg(sbo_url, name)
            dependencies = sbo_req.split()
            if dependencies != []:
                dep_results.append(dependencies)
            for line in dependencies:
                print # new line after dependency
                sbo_dependencies_pkg(line)
            return dep_results

def sbo_dependencies_links_pkg(name):
    '''
    Search for packages dependecies links
    '''
    if name != "%README%":
        sbo_url = sbo_search_pkg(name)
        if sbo_url is None:
             pkg_not_found(name, message="Can't find")
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
                print # new line after dependecy
                sbo_dependencies_links_pkg(line)
            return dep_links_results

def pkg_tracking(name):
    '''
    Find dependecies from package and print all
    '''
    dependencies = sbo_dependencies_pkg(name)
    if dependencies is None:
        pass
    elif dependencies == []:
        print ("\n\n{0}: package {1} no dependencies\n".format( __prog__, name))
    else:
        pkg_len = len(name) + 18
        print ("\n")
        template(pkg_len)
        print ("| {0}`{1}`{2} dependencies :{3}".format(colors.CYAN, name,
                                              colors.YELLOW, colors.ENDC))
        template(pkg_len)
        dependencies.reverse()
        print (" |")
        for i in range(len(dependencies)):
            found = " +--", str(len(dependencies[i])), ", ".join(dependencies[i])
            print (" |")
            print " ".join(found)
        print # new line at end
