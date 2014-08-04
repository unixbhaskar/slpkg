#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import getpass
from slpkg.colors import colors
from slpkg.functions import get_file
from slpkg.__metadata__ import tmp, pkg_path, build_path, sp
from slpkg.__metadata__ import sbo_arch, sbo_tag, sbo_filetype, arch
from slpkg.messages import pkg_not_found, pkg_found, template, s_user

from slpkg.pkg.find import find_package 
from slpkg.pkg.build import build_package
from slpkg.pkg.manager import pkg_upgrade

from search import sbo_search_pkg
from download import sbo_slackbuild_dwn
from dependency import sbo_dependencies_pkg
from greps import sbo_source_dwn, sbo_extra_dwn
from greps import sbo_prgnam_pkg, sbo_version_pkg

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
    dependencies_list = sbo_dependencies_pkg(name)
    if dependencies_list == None:
        pass
    else:
        try:
            os.system("mkdir -p {0}".format(build_path))
            os.chdir(build_path)
            requires, dependencies, extra = [], [], []
            requires.append(name)
            for pkg in dependencies_list:
                requires += pkg
            requires.reverse()
            for duplicate in requires:
                if duplicate not in dependencies:
                    dependencies.append(duplicate)
            print # new lines at start
            template(78)
            print ("| Start download, build and install packages:")
            template(78)
            for pkg in dependencies:
                sbo_url = sbo_search_pkg(pkg)
                sbo_version = sbo_version_pkg(sbo_url, pkg)
                sbo_file = "".join(find_package(pkg + sp, pkg_path))
                sbo_file_version = sbo_file[len(pkg) + 1:-len(arch) - 7]
                if sbo_version > sbo_file_version:
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
                    build_package(script, source, extra, build_path)
                    binary = ("{0}{1}{2}{3}{4}".format(
                               tmp, prgnam, sbo_arch, sbo_tag, sbo_filetype).split())
                    pkg_upgrade(binary)
                else:
                    template(78)
                    pkg_found(pkg)
                    template(78)
            print # new line at end
        except KeyboardInterrupt:
            print # new line at exit
            sys.exit()
