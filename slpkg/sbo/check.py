#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import getpass

from ..pkg.build import *
from ..pkg.find import find_package
from ..pkg.manager import pkg_upgrade

from ..colors import colors
from ..functions import get_file
from ..__metadata__ import sbo_arch, sbo_tag, sbo_filetype
from ..__metadata__ import __prog__, tmp, packages, uname, arch
from ..messages import file_not_found, pkg_not_found, s_user, template

from search import sbo_search_pkg
from download import sbo_slackbuild_dwn
from greps import sbo_source_dwn, sbo_extra_dwn, sbo_version_pkg

def sbo_check(name):
    '''
    Check if packages is up to date from slackbuilds.org
    '''
    sbo_file = " ".join(find_package(name, packages))
    if sbo_file == "":
        file_not_found(name)
    else:
        sbo_url = sbo_search_pkg(name)
        if sbo_url is None:
            pkg_not_found(name)
        else:
            sbo_version = sbo_version_pkg(sbo_url, name)
            sbo_dwn = sbo_slackbuild_dwn(sbo_url, name)
            source_dwn = sbo_source_dwn(sbo_url, name)
            extra_dwn = " ".join(sbo_extra_dwn(sbo_url, name))
            sbo_file = sbo_file[len(name) + 1:-len(arch) - 7]
            if sbo_version > sbo_file:
                print ("\n")
                print ("New version is available:")
                template(78)
                print ("| {0}: package: {1} {2} --> {3} {4}".format(
                        __prog__, name, sbo_file,  name, sbo_version))
                template(78)
                print
                read = raw_input("Would you like to install ? [Y/y] ")
                if read == "Y" or read == "y":
                    s_user(getpass.getuser())
                    pkg_for_install = name + "-" + sbo_version
                    script = get_file(sbo_dwn, "/")
                    source = get_file(source_dwn, "/")
                    print ("\n{0} Start --> {1} \n".format(colors.GREEN, colors.ENDC))
                    os.system("wget -N " + sbo_dwn)
                    os.system("wget -N " + source_dwn)
                    extra = []
                    if extra_dwn != "":
                        os.system("wget -N " + extra_dwn)
                        extra_dwn = extra_dwn.split()
                        for link in extra_dwn:
                            extra.append(get_file(link, "/"))
                            build_extra_pkg(script, source, extra)
                            binary = (tmp + pkg_for_install + sbo_arch + sbo_tag + sbo_filetype).split()
                            pkg_upgrade(binary)
                            sys.exit()
                    build_package(script, source)
                    binary = (tmp + pkg_for_install + sbo_arch + sbo_tag + sbo_filetype).split()
                    pkg_upgrade(binary)
                print
            else:
                print ("\n\n{0}: package: {1} is up to date\n".format(__prog__, name))
