#!/usr/bin/python
# -*- coding: utf-8 -*-

# slackbuild.py file is part of slpkg.

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Utility for easy management packages in Slackware

# https://github.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys

from slpkg.toolbar import status
from slpkg.init import initialization
from slpkg.downloader import Download
from slpkg.__metadata__ import (tmp, pkg_path, build_path,
                                log_path, lib_path, sp)

from slpkg.colors import RED, GREEN, GREY, YELLOW, CYAN, ENDC
from slpkg.messages import (pkg_found, template, build_FAILED,
                            pkg_not_found)

from slpkg.pkg.find import find_package
from slpkg.pkg.build import BuildPackage
from slpkg.pkg.manager import PackageManager

from greps import SBoGrep
from compressed import SBoLink
from search import sbo_search_pkg
from dependency import sbo_dependencies_pkg


class SBoInstall(object):

    def __init__(self, name):
        self.name = name
        sys.stdout.write("{0}Reading package lists ...{1}".format(GREY, ENDC))
        sys.stdout.flush()
        initialization()
        self.UNST = ["UNSUPPORTED", "UNTESTED"]
        self.dependencies_list = sbo_dependencies_pkg(name)

    def start(self):
        '''
        Download, build and install or upgrade packages
        with all dependencies if version is greater than
        that established.
        '''
        try:
            if self.dependencies_list or sbo_search_pkg(self.name) is not None:
                requires = one_for_all(self.name, self.dependencies_list)
                dependencies = remove_dbs(requires)
                # sbo versions = idata[0]
                # package arch = idata[1]
                # package sum = idata[2]
                # sources = idata[3]
                idata = installing_data(dependencies, self.UNST)
                sys.stdout.write("{0}Done{1}\n".format(GREY, ENDC))
                # count upgraded = cnt[0]
                # count installed = cnt[1]
                (PKG_COLOR, count) = pkg_colors_tag(self.name, idata[0], 0, 0)
                print("\nThe following packages will be automatically "
                      "installed or upgraded")
                print("with new version:\n")
                top_view()
                print("Installing:")
                ARCH_COLOR = arch_colors_tag(self.UNST, idata[1])
                view_packages(PKG_COLOR, self.name, idata[0][-1], ARCH_COLOR,
                              idata[1][-1])
                print("Installing for dependencies:")
                for dep, ver, dep_arch in zip(dependencies[:-1], idata[0][:-1],
                                              idata[1][:-1]):
                    (DEP_COLOR, count) = pkg_colors_tag(dep, ver, count[0],
                                                        count[1])
                    ARCH_COLOR = arch_colors_tag(self.UNST, dep)
                    view_packages(DEP_COLOR, dep, ver, ARCH_COLOR, dep_arch)
                # insstall message = msg[0]
                # upgraded message = msg[1]
                # total message = msg[2]
                msg = msgs(dependencies, count[1], count[0])
                print("\nInstalling summary")
                print("=" * 79)
                print("{0}Total {1} {2}.".format(GREY, len(dependencies),
                                                 msg[2]))
                print("{0} {1} will be installed, {2} allready installed and "
                      "{3} {4}".format(count[1], msg[0], idata[2], count[0],
                                       msg[1]))
                print("will be upgraded.{0}\n".format(ENDC))
                read = arch_support(idata[3], self.UNST, idata[2], dependencies)
                if read == "Y" or read == "y":
                    # installs = b_ins[0]
                    # upgraded = b_ins[1]
                    # versions = b_ins[2]
                    b_ins = build_install(dependencies, idata[0], idata[1])
                    reference(count[1], msg[0], count[0], msg[1],
                              b_ins[0], b_ins[2], b_ins[1])
                    write_deps(self.name, dependencies)
            else:
                count_installed = count_uninstalled = 0
                # sbo matching = mdata[0]
                # sbo version = mdata1]
                # package arch = mdata[2]
                mdata = matching_data(self.name, self.UNST)
                sys.stdout.write("{0}Done{1}\n".format(GREY, ENDC))
                if mdata[0]:
                    print("\nPackages with name matching [ {0}{1}{2} ]"
                          "\n".format(CYAN, self.name, ENDC))
                    top_view()
                    print("Matching:")
                    for match, ver, march in zip(mdata[0], mdata[1], mdata[2]):
                        if find_package(match + sp + ver, pkg_path):
                            view_packages(GREEN, match, ver, "", march)
                            count_installed += 1
                        else:
                            view_packages(RED, match, ver, "", march)
                            count_uninstalled += 1
                    # insstall message = msg[0]
                    # uninstall message = msg[1]
                    # total message = msg[2]
                    msg = msgs(mdata[0], count_installed, count_uninstalled)
                    print("\nInstalling summary")
                    print("=" * 79)
                    print("{0}Total found {1} matching {2}.".format(
                        GREY, len(mdata[0]), msg[2]))
                    print("{0} installed {1} and {2} uninstalled {3}.{4}"
                          "\n".format(count_installed, msg[0],
                                      count_uninstalled, msg[1], ENDC))
                else:
                    pkg_not_found("\n", self.name, "No matching", "\n")
        except KeyboardInterrupt:
            print   # new line at exit
            sys.exit()


def one_for_all(name, dependencies):
    '''
    Create one list for all packages
    '''
    requires = []
    requires.append(name)
    for pkg in dependencies:
        requires += pkg
    requires.reverse()
    return requires


def remove_dbs(requires):
    '''
    Remove double dependencies
    '''
    dependencies = []
    for duplicate in requires:
        if duplicate not in dependencies:
            dependencies.append(duplicate)
    return dependencies


def installing_data(dependencies, support):
    '''
    Create two lists one for package version and one
    for package arch
    '''
    package_sum = 0
    sbo_versions, package_arch = [], []
    for pkg in dependencies:
        version = SBoGrep(pkg).version()
        sbo_versions.append(version)
        sources = SBoGrep(pkg).source()
        package_arch.append(select_arch(sources, support))
        sbo_package = ("{0}-{1}".format(pkg, version))
        if find_package(sbo_package, pkg_path):
            package_sum += 1
    return [sbo_versions, package_arch, package_sum, sources]


def pkg_colors_tag(name, sbo_versions, count_upg, count_ins):
    '''
    Tag with color green if package already installed,
    color yellow for packages to upgrade and color red
    if not installed. Also if package arch is UNSUPPORTED
    tag with color red and if UNTESTED with color yellow.
    '''
    # check if 'sbo_versions' is list if true
    # then get last package from list is master package
    # if false 'sbo_version' is a string
    if isinstance(sbo_versions, list):
        sbo_versions = sbo_versions[-1]
    master_pkg = ("{0}-{1}".format(name, sbo_versions))
    if find_package(master_pkg, pkg_path):
        color = GREEN
    elif find_package(name + sp, pkg_path):
        color = YELLOW
        count_upg += 1
    else:
        color = RED
        count_ins += 1
    return color, [count_upg, count_ins]


def arch_colors_tag(support, package_arch):
    '''
    Arch color tag
    '''
    color = ""
    if support[0] in package_arch[-1]:
        color = RED
    elif support[1] in package_arch[-1]:
        color = YELLOW
    return color


def top_view():
    '''
    View top template
    '''
    template(78)
    print("{0}{1}{2}{3}{4}{5}{6}".format(
        "| Package", " " * 30,
        "Version", " " * 10,
        "Arch", " " * 9,
        "Repository"))
    template(78)


def view_packages(*args):
    '''
    View slackbuild packages with version and arch
    '''
    print(" {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(
        args[0], args[1], ENDC,
        " " * (38-len(args[1])), args[2],
        " " * (17-len(args[2])), args[3], args[4], ENDC,
        " " * (13-len(args[4])), "SBo"))


def msgs(packages, count_ins, count_uni):
    '''
    Print singular plural
    '''
    total_msg = ins_msg = uns_msg = "package"
    if len(packages) > 1:
        total_msg = total_msg + "s"
    if count_ins > 1:
        ins_msg = ins_msg + "s"
    if count_uni > 1:
        uns_msg = uns_msg + "s"
    return [ins_msg, uns_msg, total_msg]


def arch_support(source, support, package_sum, dependencies):
    '''
    Check if package supported or tested by arch
    before proceed to install.
    Exit if all packages already installed
    '''
    if source in support:
        print("{0}The package {1}{2}\n".format(RED, source, ENDC))
        read = ""
    elif package_sum == len(dependencies):
        read = ""
    else:
        read = raw_input("Do you want to continue [Y/n]? ")
    return read


def create_build_path():
    '''
    Create build directory if not exists
    '''
    if not os.path.exists(build_path):
        os.mkdir(build_path)


def dwn_sources(sources):
    '''
    Download sources and return filenames
    '''
    filename = []
    for src in sources:
        # get file from source
        filename.append(src.split("/")[-1])
        Download(build_path, src).start()
    return filename


def search_in_tmp(prgnam):
    '''
    Search for binarys packages in /tmp directory
    '''
    binary = []
    for search in find_package(prgnam, tmp):
        if "_SBo" in search:
            binary.append(search)
    return binary


def build_install(dependencies, sbo_versions, packages_arch):
    '''
    Searches the package name and version in /tmp to
    install. If find two or more packages e.g. to build
    tag 2 or 3 will fit most
    '''
    installs, upgraded, versions = [], [], []
    create_build_path()
    os.chdir(build_path)
    for pkg, ver, ar in zip(dependencies, sbo_versions, packages_arch):
        prgnam = ("{0}-{1}".format(pkg, ver))
        sbo_file = "".join(find_package(prgnam, pkg_path))
        if sbo_file:
            sbo_file_version = sbo_file[len(pkg) + 1:-len(ar) - 7]
            template(78)
            pkg_found(pkg, sbo_file_version)
            template(78)
        else:
            sbo_url = sbo_search_pkg(pkg)
            sbo_link = SBoLink(sbo_url).tar_gz()
            src_link = SBoGrep(pkg).source().split()
            script = sbo_link.split("/")[-1]
            Download(build_path, sbo_link).start()
            sources = dwn_sources(src_link)
            BuildPackage(script, sources, build_path).build()
            binary_list = search_in_tmp(prgnam)
            try:
                binary = (tmp + max(binary_list)).split()
            except ValueError:
                build_FAILED(sbo_url, prgnam)
                sys.exit()
            if find_package(pkg + sp, pkg_path):
                print("{0}[ Upgrading ] --> {1}{2}".format(GREEN, ENDC, pkg))
                upgraded.append(pkg)
            else:
                print("{0}[ Installing ] --> {1}{2}".format(GREEN, ENDC, pkg))
            PackageManager(binary).upgrade()
            installs.append(pkg)
            versions.append(ver)
    return [installs, upgraded, versions]


def reference(*args):
    '''
    Reference list with packages installed
    and upgraded
    '''
    template(78)
    print("| Total {0} {1} installed and {2} {3} upgraded".format(
        args[0], args[1], args[2], args[3]))
    template(78)
    for pkg, ver in zip(args[4], args[5]):
        installed = ("{0}-{1}".format(pkg, ver))
        if find_package(installed, pkg_path):
            if pkg in args[5]:
                print("| Package {0} upgraded successfully".format(installed))
            else:
                print("| Package {0} installed successfully".format(installed))
        else:
            print("| Package {0} NOT installed".format(installed))
    template(78)


def write_deps(name, dependencies):
    '''
    Write dependencies in a log file
    into directory `/var/log/slpkg/dep/`
    '''
    if find_package(name + sp, pkg_path):
        dep_path = log_path + "dep/"
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        if not os.path.exists(dep_path):
            os.mkdir(dep_path)
        if os.path.isfile(dep_path + name):
            os.remove(dep_path + name)
        if len(dependencies[:-1]) > 0:
            with open(dep_path + name, "w") as f:
                for dep in dependencies[:-1]:
                    f.write(dep + "\n")
                f.close()


def matching_data(name, support):
    '''
    Open and read SLACKBUILD.TXT file and store matching
    packages
    '''
    sbo_matching, sbo_versions, packages_arch = [], [], []
    toolbar_width, index = 3, 0
    with open(lib_path + "sbo_repo/SLACKBUILDS.TXT", "r") as SLACKBUILDS_TXT:
        for line in SLACKBUILDS_TXT:
            if line.startswith("SLACKBUILD NAME: "):
                sbo_name = line[17:].strip()
                if name in sbo_name:
                    index += 1
                    toolbar_width = status(index, toolbar_width, 4)
                    sbo_matching.append(sbo_name)
                    sbo_versions.append(SBoGrep(sbo_name).version())
                    sources = SBoGrep(sbo_name).source()
                    packages_arch.append(select_arch(sources, support))
        SLACKBUILDS_TXT.close()
    return [sbo_matching, sbo_versions, packages_arch]


def select_arch(src, support):
    '''
    Looks if sources unsupported or untested
    from arch else select arch
    '''
    arch = os.uname()[4]
    if arch.startswith("i") and arch.endswith("86"):
        arch = "i486"
    for item in support:
        if item in src:
            arch = item
    return arch
