#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..pkg.build import *
from ..colors import colors
from ..pkg.find import find_package
from ..functions import s_user, get_file

from read import *
from greps import *
from search import sbo_search_pkg
from download import sbo_slackbuild_dwn

tmp = "/tmp/"
packages = "/var/log/packages/"

# SBo fietype binary packages
sbo_arch = "*"
sbo_tag = "?_SBo"
sbo_filetype = ".tgz"

def sbo_network(name):
    '''
    View SalckBuild package links, read or install them 
    from slackbuilds.org
    '''
    sbo_url = sbo_search_pkg(name)
    if sbo_url is None:
        print ("\n\n{}The {}`{}`{} not found{}\n".format(colors.RED, colors.CYAN,
                                                     name, colors.RED, colors.ENDC))
    else:
        sbo_req = sbo_requires_pkg(sbo_url, name)
        sbo_dwn = sbo_slackbuild_dwn(sbo_url, name)
        sbo_version = sbo_version_pkg(sbo_url, name)
        source_dwn = sbo_source_dwn(sbo_url, name)
        extra_dwn = " ".join(sbo_extra_dwn(sbo_url, name))
        sbo_name_len = len(name)
        sbo_url_len = (len(sbo_url) + sbo_name_len + 21)
        print ("\n\n+" + "=" * sbo_url_len)
        print ("| {}The {}`{}`{} found in --> {}".format(colors.GREEN, colors.CYAN,
                                                         name, colors.GREEN,
                                                         colors.ENDC + sbo_url))
        print ("+" + "=" * sbo_url_len)
        print ("| {}Download SlackBuild : {}{}".format(colors.GREEN,
                                                       colors.ENDC, sbo_dwn))
        print ("| {}Source Downloads : {}{}".format(colors.GREEN,
                                                    colors.ENDC, source_dwn))
        print ("| {}Extra Downloads : {}{}".format(colors.GREEN,
                                                   colors.ENDC, extra_dwn))
        print ("| {}Package requirements : {}{}".format(colors.YELLOW,
                                                        colors.ENDC, sbo_req))
        print ("+" + "=" * sbo_url_len)
        print (" {}R{}EADME               View the README file".format(colors.RED,
                                                                       colors.ENDC))
        print (" {}S{}lackBuild           View the SlackBuild file".format(colors.RED,
                                                                           colors.ENDC))
        print (" In{}f{}o                 View the Info file".format(colors.RED,
                                                                     colors.ENDC))
        print (" {}D{}ownload             Download this package".format(colors.RED,
                                                                        colors.ENDC))
        print (" {}B{}uild                Download and build".format(colors.RED,
                                                                     colors.ENDC))
        print (" {}I{}nstall              Download/Build/Install\n".format(colors.RED,
                                                                           colors.ENDC))
        while True:
            read = raw_input("_ ")
            if read == "D" or read == "d":
                print ("\n{}Start -->{}\n".format(colors.GREEN, colors.ENDC))
                os.system("wget -N " + sbo_dwn)
                os.system("wget -N " + source_dwn)
                if extra_dwn != "":
                    os.system("wget " + extra_dwn)
                break
            elif read == "R" or read == "r":
                site = "README"
                read_readme(sbo_url, name, site)
                os.system("less /tmp/slpkg/readme/{}.{}".format(name, site))
                os.remove("/tmp/slpkg/readme/{}.{}".format(name, site))
            elif read == "F" or read == "f":
                site = ".info"
                read_info_slackbuild(sbo_url, name, site)
                os.system("less /tmp/slpkg/readme/{}{}".format(name, site))
                os.remove("/tmp/slpkg/readme/{}{}".format(name, site))
            elif read == "S" or read == "s":
                site = ".SlackBuild"
                read_info_slackbuild(sbo_url, name, site)
                os.system("less /tmp/slpkg/readme/{}{}".format(name, site))
                os.remove("/tmp/slpkg/readme/{}{}".format(name, site))
            elif read == "B" or read == "b":
                s_user(getpass.getuser())
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
                    break
                build_package(script, source)
                break
            elif read == "I" or read == "i":
                s_user(getpass.getuser())
                pkg_for_install = name + "-" + sbo_version
                if find_package(pkg_for_install, packages) == []:
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
                        install_pkg = tmp + pkg_for_install + sbo_arch + sbo_tag + sbo_filetype
                        os.system("upgradepkg --install-new {}".format(install_pkg))
                        break
                    build_package(script, source)
                    install_pkg = tmp + pkg_for_install + sbo_arch + sbo_tag + sbo_filetype
                    os.system("upgradepkg --install-new {}".format(install_pkg))
                    break
                else:
                    print ("\n{}The package {}`{}`{} is arlready installed{}\n".format(
                            colors.YELLOW,
                            colors.CYAN, pkg_for_install, colors.YELLOW, colors.ENDC))
                    break
            else:
                break
