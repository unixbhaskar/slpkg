#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import getpass

from slpkg.colors import colors
from slpkg.functions import get_file
from slpkg.__metadata__ import tmp, packages, __prog__
from slpkg.__metadata__ import sbo_arch, sbo_tag, sbo_filetype
from slpkg.messages import s_user, pkg_found, pkg_installed, template

from slpkg.pkg.build import *
from slpkg.pkg.find import find_package
from slpkg.pkg.manager import pkg_upgrade

from dependency import sbo_dependencies_links_pkg

def sbo_build(name):
    '''
    Download, build packages and install or upgrade with all
    dependecies
    '''
    s_user(getpass.getuser())
    dependencies_links = sbo_dependencies_links_pkg(name)
    '''
    create one list for all
    '''
    if dependencies_links is None:
        sys.exit()
    elif dependencies_links != []:
        results = []
        for i in range(len(dependencies_links)):
            for j in range(len(dependencies_links[i])):
                results.append(dependencies_links[i][j])
    '''
    grep http links from list
    '''
    dwn_link = []
    for link in results:
        if link.startswith('http'):
            dwn_link.append(link)
        if link.startswith('ftp'):
            dwn_link.append(link)
    '''
    grep package version
    '''
    version = []
    for ver in results:
        if ver.startswith("@"):
            ver = ver.replace("@", "")
            version.append(ver)
    '''
    upside-down lists
    '''
    version .reverse()
    dwn_link.reverse()
    '''
    get tar archives from link
    '''
    files = []
    for i in range(len(dwn_link)):
        files.append(get_file(dwn_link[i], "/"))
    '''
    removes archive type and store the package name
    '''
    filename = []
    y = 0
    for i in range(len(files) / 2):
        if files[y].endswith("tar.gz"):
            file = files[y]
            file = file[:-7]
            filename.append(file)
            y += 2
    '''
    create package installation package + version
    '''
    filename_version = []
    for i in range(len(filename)):
        filename_version.append(filename[i] + "-" + version[i])
    '''
    remove links and files if packages already installed
    and keep lists for report
    '''
    i = 0
    pkg_for_install = []
    pkg_already_installed = []
    for file in filename_version:
        if find_package(file, packages) == []:
            i += 2
            pkg_for_install.append(file)
        else:
            pkg_already_installed.append(file)
            for j in range(0, 2):
                dwn_link.pop(i)
                files.pop(i)
    '''
    remove double links
    '''
    dwn_link = set(dwn_link)
    '''
    download links if not exist or previously than server
    '''
    for link in dwn_link:
        print ("\n{0} Start --> \n{1}".format(colors.GREEN, colors.ENDC))
        os.system("wget -N %s" % link)
    print ("\n")
    '''
    build packages and install slackware packages
    '''
    template(78)
    if pkg_for_install == []:
        for pkg in filename_version:
            pkg_found(pkg)
        template(78)
    else:
        '''
        check for extra sources
        '''
        if results[0].startswith("extra"):
            extra_Num = int(results[0].replace("extra", ""))
            i = 0
            for i in range(len(files) / 2):
                if len(files) == extra_Num + 2:
                    script = files[0]
                    source = files[1]
                    extra = files[2:]
                    build_extra_pkg(script, source, extra)
                    binary = (tmp + pkg_for_install[i] + sbo_arch + sbo_tag + sbo_filetype).split()
                    pkg_upgrade(binary)
                    break
                else:
                    script = files[0]
                    source = files[1]
                    build_package(script, source)
                    binary = (tmp + pkg_for_install[i] + sbo_arch + sbo_tag + sbo_filetype).split()
                    pkg_upgrade(binary)
                    for j in range(0, 2):
                        files.pop(0)
        else:
            i = 0
            for i in range(len(files) / 2):
                script = files[0]
                source = files[1]
                build_package(script, source)
                binary = (tmp + pkg_for_install[i] + sbo_arch + sbo_tag + sbo_filetype).split()
                pkg_upgrade(binary)
                for j in range(0, 2):
                    files.pop(0)
        template(78)
        for pkg in pkg_for_install:
            if find_package(pkg, packages) != []:
                pkg_installed(pkg)
        for pkg in pkg_already_installed:
            if find_package(pkg, packages) != []:
                pkg_found(pkg)
        template(78)
    print # new line at end
