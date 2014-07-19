#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import getpass

from ..pkg.build import *
from ..colors import colors
from ..pkg.find import find_package
from ..functions import s_user, get_file

from search import sbo_search_pkg
from download import sbo_slackbuild_dwn
from greps import sbo_source_dwn, sbo_extra_dwn, sbo_version_pkg

tmp = "/tmp/"
packages = "/var/log/packages/"

# computer architecture
uname = os.uname()
arch = (uname[4])

# SBo fietype binary packages
sbo_arch = "*"
sbo_tag = "?_SBo"
sbo_filetype = ".tgz"

def sbo_check(name):
    '''
    Check if packages is up to date from slackbuilds.org
    '''
    sbo_file = " ".join(find_package(name, packages))
    if sbo_file == "":
        print ("\n {}The package {}`{}`{} not found on your system{}\n".format(colors.RED,
                colors.CYAN, name, colors.RED, colors.ENDC))
    else:
        sbo_url = sbo_search_pkg(name)
        if sbo_url is None:
            print ("\n\n{}The {}`{}`{} not found{}\n".format(colors.RED, colors.CYAN, name,
                                                             colors.RED, colors.ENDC))
        else:
            sbo_version = sbo_version_pkg(sbo_url, name)
            sbo_dwn = sbo_slackbuild_dwn(sbo_url, name)
            source_dwn = sbo_source_dwn(sbo_url, name)
            extra_dwn = " ".join(sbo_extra_dwn(sbo_url, name))
            name_len = len(name)
            arch_len = len(arch)
            sbo_file = sbo_file[name_len + 1:-arch_len - 7]
            if sbo_version > sbo_file:
                print ("\n\n{} New version is available !!!{}".format(colors.YELLOW,
                                                                      colors.ENDC))
                print ("+" + "=" * 50)
                print ("| {} {}".format(name, sbo_version))
                print ("+" + "=" * 50)
                print
                read = raw_input("Would you like to install ? [Y/y] ")
                if read == "Y" or read == "y":
                    s_user(getpass.getuser())
                    pkg_for_install = name + "-" + sbo_version
                    script = get_file(sbo_dwn, "/")
                    source = get_file(source_dwn, "/")
                    print ("\n{}Start -->{}\n".format(colors.GREEN, colors.ENDC))
                    os.system("wget -N " + sbo_dwn)
                    os.system("wget -N " + source_dwn)
                    extra = []
                    if extra_dwn != "":
                        os.system("wget -N " + extra_dwn)
                        extra_dwn = extra_dwn.split()
                        for link in extra_dwn:
                            extra.append(get_file(link, "/"))
                            build_extra_pkg(script, source, extra)
                            install_pkg = tmp + pkg_for_install + sbo_arch + sbo_tag + \
                                          sbo_filetype
                            os.system("upgradepkg --install-new {}".format(install_pkg))
                            sys.exit()
                    build_package(script, source)
                    install_pkg = tmp + pkg_for_install + sbo_arch + sbo_tag + sbo_filetype
                    os.system("upgradepkg --install-new {}".format(install_pkg))
                print
            else:
                print ("\n\n{}Your package is up to date{}\n".format(colors.GREEN, colors.ENDC))
