#!/usr/bin/python
# -*- coding: utf-8 -*-


from slpkg.colors import colors
from slpkg.functions import get_file
from slpkg.__metadata__ import tmp, packages
from slpkg.__metadata__ import sbo_arch, sbo_tag, sbo_filetype
from slpkg.messages import s_user, pkg_not_found, pkg_found, view_sbo, template

from slpkg.pkg.build import *
from slpkg.pkg.find import find_package
from slpkg.pkg.manager import pkg_upgrade

from read import *
from greps import *
from search import sbo_search_pkg
from download import sbo_slackbuild_dwn

def sbo_network(name):
    '''
    View SalckBuild package links, read or install them 
    from slackbuilds.org
    '''
    sbo_url = sbo_search_pkg(name)
    if sbo_url is None:
        pkg_not_found(name, message="Can't find")
    else:
        sbo_req = sbo_requires_pkg(sbo_url, name)
        sbo_dwn = sbo_slackbuild_dwn(sbo_url, name)
        sbo_version = sbo_version_pkg(sbo_url, name)
        source_dwn = sbo_source_dwn(sbo_url, name)
        extra_dwn = " ".join(sbo_extra_dwn(sbo_url, name))
        view_sbo(name, sbo_url, sbo_dwn, source_dwn, extra_dwn, sbo_req)
        while True:
            read = raw_input("_ ")
            if read == "D" or read == "d":
                print ("\n{0}Start -->{1}\n".format(colors.GREEN, colors.ENDC))
                os.system("wget -N " + sbo_dwn)
                os.system("wget -N " + source_dwn)
                if extra_dwn != "":
                    os.system("wget " + extra_dwn)
                break
            elif read == "R" or read == "r":
                site = "README"
                read_readme(sbo_url, name, site)
                os.system("less /tmp/slpkg/readme/{0}.{1}".format(name, site))
                os.remove("/tmp/slpkg/readme/{}.{}".format(name, site))
            elif read == "F" or read == "f":
                site = ".info"
                read_info_slackbuild(sbo_url, name, site)
                os.system("less /tmp/slpkg/readme/{0}{1}".format(name, site))
                os.remove("/tmp/slpkg/readme/{0}{1}".format(name, site))
            elif read == "S" or read == "s":
                site = ".SlackBuild"
                read_info_slackbuild(sbo_url, name, site)
                os.system("less /tmp/slpkg/readme/{0}{1}".format(name, site))
                os.remove("/tmp/slpkg/readme/{0}{1}".format(name, site))
            elif read == "B" or read == "b":
                s_user(getpass.getuser())
                script = get_file(sbo_dwn, "/")
                source = get_file(source_dwn, "/")
                print ("\n{0}Start -->{1}\n".format(colors.GREEN, colors.ENDC))
                os.system("wget -N " + sbo_dwn)
                os.system("wget -N " + source_dwn)
                extra = []
                if extra_dwn != "":
                    os.system("wget -N " + extra_dwn)
                    extra_dwn = extra_dwn.split()
                    for link in extra_dwn:
                        extra.append(get_file(link, "/"))
                    build_extra_pkg(script, source, extra)
                    break
                build_package(script, source)
                break
            elif read == "I" or read == "i":
                s_user(getpass.getuser())
                pkg_for_install = name + "-" + sbo_version
                if find_package(pkg_for_install, packages) == []:
                    script = get_file(sbo_dwn, "/")
                    source = get_file(source_dwn, "/")
                    print ("\n{0}Start -->{1}\n".format(colors.GREEN, colors.ENDC))
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
                        break
                    build_package(script, source)
                    binary = (tmp + pkg_for_install + sbo_arch + sbo_tag + sbo_filetype).split()
                    pkg_upgrade(binary)
                    break
                else:
                    template(78)
                    pkg_found(''.join(find_package(name, packages)))
                    template(78)
                    break
            else:
                break
