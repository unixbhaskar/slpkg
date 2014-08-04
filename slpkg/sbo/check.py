#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import getpass
from slpkg.pkg.build import *
from slpkg.pkg.find import find_package
from slpkg.pkg.manager import pkg_upgrade

from slpkg.colors import colors
from slpkg.functions import get_file
from slpkg.messages import pkg_not_found, s_user, template
from slpkg.__metadata__ import tmp, pkg_path, uname, arch, sp
from slpkg.__metadata__ import sbo_arch, sbo_tag, sbo_filetype, build_path

from search import sbo_search_pkg
from download import sbo_slackbuild_dwn
from greps import sbo_source_dwn, sbo_extra_dwn, sbo_prgnam_pkg, sbo_version_pkg

def sbo_check(name):
    '''
    Check for new package updates
    '''
    sbo_file = "".join(find_package(name + sp, pkg_path))
    if sbo_file == "":
        message = "Not installed"
        bol, eol = "\n", "\n"
        pkg_not_found(bol, name, message, eol)
    else:
        print ("\nSearch for package {0} from slackbuilds.org:\n".format(name))
        sbo_url = sbo_search_pkg(name)
        if sbo_url is None:
            message = "From slackbuilds.org"
            bol, eol = "", "\n"
            pkg_not_found(bol, name, message, eol)
        else:
            sbo_version = sbo_version_pkg(sbo_url, name)
            sbo_dwn = sbo_slackbuild_dwn(sbo_url, name)
            source_dwn = sbo_source_dwn(sbo_url, name)
            extra_dwn = sbo_extra_dwn(sbo_url, name)
            sbo_file_version = sbo_file[len(name) + 1:-len(arch) - 7]
            if sbo_version > sbo_file_version:
                print ("\n{0}New version is available:{1}".format(
                        colors.YELLOW, colors.ENDC))
                template(78)
                print ("| Package: {0} {1} --> {2} {3}".format(
                        name, sbo_file_version,  name, sbo_version))
                template(78)
                print # new line at start
                read = raw_input("Would you like to install ? [Y/y] ")
                if read == "Y" or read == "y":
                    s_user(getpass.getuser())
                    os.system("mkdir -p {0}".format(build_path))
                    os.chdir(build_path)
                    prgnam = sbo_prgnam_pkg(sbo_url, name)
                    pkg_for_install = ("{0}-{1}".format(prgnam, sbo_version))
                    script = get_file(sbo_dwn, "/")
                    source = get_file(source_dwn, "/")
                    print ("\n{0}Start -->{1}\n".format(colors.GREEN, colors.ENDC))
                    os.system("wget -N {0} {1}".format(sbo_dwn, source_dwn))
                    extra = []
                    if extra_dwn:
                        for src in extra_dwn.split():
                            os.system("wget -N {0}".format(src))
                            extra.append(get_file(src, "/"))
                    build_package(script, source, extra, build_path)
                    binary = ("{0}{1}{2}{3}{4}".format(
                               tmp, pkg_for_install, sbo_arch, sbo_tag, sbo_filetype).split())
                    pkg_upgrade(binary)                     
            else:
                print ("\nPackage {0} is up to date\n".format(
                       "".join(find_package(name + sp, pkg_path))))
