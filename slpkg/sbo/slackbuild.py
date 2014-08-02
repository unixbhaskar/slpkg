#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import getpass
from slpkg.colors import colors
from slpkg.functions import get_file
from slpkg.messages import pkg_not_found, template, s_user
from slpkg.__metadata__ import tmp, sbo_arch, sbo_tag, sbo_filetype

from slpkg.pkg.build import build_package
from slpkg.pkg.manager import pkg_upgrade

from search import sbo_search_pkg
from download import sbo_slackbuild_dwn
from dependency import sbo_dependencies_pkg
from greps import sbo_prgnam_pkg, sbo_version_pkg, sbo_source_dwn, sbo_extra_dwn

def sbo_build(name):
    '''
    Download, build and upgrade packages with all
    dependencies
    '''
    s_user(getpass.getuser())
    print # new line at start
    template(78)
    print ("| Build dependencies tree for package {0}:".format(name))
    template(78)
    dependencies = sbo_dependencies_pkg(name)
    if dependencies == None:
        pass
    else:
        try:
            requires, extra = [], []
            requires.append(name)
            for pkg in dependencies:
                requires += pkg
            requires.reverse()
            print # new lines at start
            template(78)
            print ("| Start download, build and install packages:")
            template(78)
            for pkg in requires:
                sbo_url = sbo_search_pkg(pkg)
                prgnam = ("{0}-{1}".format(sbo_prgnam_pkg(sbo_url, pkg),
                                           sbo_version_pkg(sbo_url, pkg)))
                sbo_link = sbo_slackbuild_dwn(sbo_url, pkg)
                src_link = sbo_source_dwn(sbo_url, pkg) 
                ext_link = sbo_extra_dwn(sbo_url, pkg)
                script = get_file(sbo_link, '/')
                source = get_file(src_link, '/')
                os.system("wget -N {0} {1}".format(sbo_link, src_link))
                if ext_link:
                    for src in ext_link:
                        os.system("wget -N {0}".format(src))
                        extra.append(get_file(src, '/'))
                build_package(script, source, extra)
                binary = (tmp + prgnam + sbo_arch + sbo_tag + sbo_filetype).split()
                pkg_upgrade(binary)
        except KeyboardInterrupt:
            print # new line at exit
            sys.exit()
