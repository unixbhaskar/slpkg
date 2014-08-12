#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

from slpkg.colors import colors
from slpkg.functions import get_file
from slpkg.__metadata__ import tmp, pkg_path, slpkg_path, sp
from slpkg.__metadata__ import sbo_arch, sbo_tag, sbo_filetype, build_path
from slpkg.messages import s_user, pkg_not_found, pkg_found, view_sbo, template

from slpkg.pkg.build import build_package
from slpkg.pkg.find import find_package
from slpkg.pkg.manager import pkg_upgrade

from read import *
from greps import *
from search import sbo_search_pkg
from download import sbo_slackbuild_dwn

def sbo_network(name):
    '''
    View SlackBuild package, read or install them 
    from slackbuilds.org
    '''
    sys.stdout.write ("Reading package lists.")
    sbo_url = sbo_search_pkg(name)
    if sbo_url is None:
        sys.stdout.write (' Done\n')
        message = "From slackbuilds.org"
        bol, eol = "\n", "\n"
        pkg_not_found(bol, name, message, eol)
    else:
        sys.stdout.write (' Done\n')
        sbo_req = sbo_requires_pkg(sbo_url, name)
        sbo_dwn = sbo_slackbuild_dwn(sbo_url, name)
        sbo_version = sbo_version_pkg(sbo_url, name)
        source_dwn = sbo_source_dwn(sbo_url, name)
        extra_dwn = " ".join(sbo_extra_dwn(sbo_url, name))
        view_sbo(name, sbo_url, get_file(sbo_dwn, '/'), get_file(source_dwn, '/'),
                 ', '.join([get_file(extra_dwn, '/') for extra_dwn in extra_dwn.split()]),
                 sbo_req)
        while True:
            try:
                read = raw_input("_ ")
            except KeyboardInterrupt:
                print # new line at exit
                break
            if read == "D" or read == "d":
                print ("\n{0}Start -->{1}\n".format(colors.GREEN, colors.ENDC))
                os.system("wget -N {0} {1}".format(sbo_dwn, source_dwn))
                if extra_dwn:
                    for src in extra_dwn.split():
                        os.system("wget -N {0}".format(src))
                break
            elif read == "R" or read == "r":
                site = "README"
                read_readme(sbo_url, name, site)
                os.system("less {0}readme/{1}.{2}".format(slpkg_path, name, site))
                os.remove("{0}readme/{1}.{2}".format(slpkg_path, name, site))
            elif read == "F" or read == "f":
                site = ".info"
                read_info_slackbuild(sbo_url, name, site)
                os.system("less {0}readme/{1}{2}".format(slpkg_path, name, site))
                os.remove("{0}readme/{1}{2}".format(slpkg_path, name, site))
            elif read == "S" or read == "s":
                site = ".SlackBuild"
                read_info_slackbuild(sbo_url, name, site)
                os.system("less {0}readme/{1}{2}".format(slpkg_path, name, site))
                os.remove("{0}readme/{1}{2}".format(slpkg_path, name, site))
            elif read == "B" or read == "b":
                s_user(getpass.getuser())
                os.system("mkdir -p {0}".format(build_path))
                os.chdir(build_path)
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
                break
            elif read == "I" or read == "i":
                s_user(getpass.getuser())
                os.system("mkdir -p {0}".format(build_path))
                os.chdir(build_path)
                prgnam = sbo_prgnam_pkg(sbo_url, name)
                pkg_for_install = ("{0}-{1}".format(prgnam, sbo_version))
                if find_package(prgnam + sp, pkg_path) == []:
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
                    break
                else:
                    template(78)
                    pkg_found(''.join(find_package(prgnam + sp, pkg_path)))
                    template(78)
                    print # new line at end
                    break
            else:
                break
