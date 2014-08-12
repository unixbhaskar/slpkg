#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import getpass

from slpkg.colors import colors
from slpkg.functions import get_file
from slpkg.__metadata__ import tmp, pkg_path, build_path, sp
from slpkg.messages import pkg_not_found, pkg_found, template, s_user
from slpkg.__metadata__ import sbo_arch, sbo_tag, sbo_filetype, arch, log_path

from slpkg.pkg.find import find_package 
from slpkg.pkg.build import build_package
from slpkg.pkg.manager import pkg_upgrade

from search import sbo_search_pkg
from file_size import server_file_size
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
    sys.stdout.write ('Building dependency tree.')
    dependencies_list = sbo_dependencies_pkg(name)
    sys.stdout.write(' Done')
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
            print ('The following packages will be automatically installed or upgraded with new version:\n')
            print ('  ' + ' '.join(dependencies))
            read = raw_input("\nDo you want to continue [Y/n]? ")
            if read == "Y" or read == "y":
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
                        pkg_found(pkg, sbo_file_version)
                        template(78)
            '''
            Write dependencies in a log file into directory '/var/log/slpkg/dep/'
            '''
            os.system("mkdir -p {0}dep/".format(log_path))
            if find_package(name, log_path + "dep/"):
                os.remove("{0}dep/{1}".format(log_path, name))
            if len(dependencies) > 1:
                f = open("{0}dep/{1}".format(log_path, name), "w")
                for dep in dependencies:
                    f.write(dep + "\n")
                f.close()
        except KeyboardInterrupt:
            print # new line at exit
            sys.exit()
