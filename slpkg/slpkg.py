#!/usr/bin/python
# -*- coding: utf-8 -*-


''' Utility to help package management in Slackware.
Slpkg is a terminal tool in order to easy use Slackware packages.


It's a quick and easy way to manage your packages in Slackware to a command.



usage: slpkg [-h] [-v] [-s script [source ...]] [-l all, sbo [all, sbo ...]]
             [-t] [-n] [-c] [-b] [-i  [...]] [-u  [...]] [-a  [...]]
             [-r  [...]] [-f  [...]] [-d  [...]]

Utility to help package management in Slackware

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         print version and exit
  -s script [source ...]
                        auto build package
  -l all, sbo [all, sbo ...]
                        list of installed packages
  -t                    tracking dependencies
  -n                    find from SBo repositority
  -c                    check if your package is up to date
  -b                    download, build & install pkg from SBo
  -i  [ ...]            install binary packages
  -u  [ ...]            install-upgrade packages with new
  -a  [ ...]            reinstall the same packages
  -r  [ ...]            remove packages
  -f  [ ...]            find if packages installed
  -d  [ ...]            display the contents of the packages

'''


import os
import re
import sys
import shutil
import tarfile
import getpass
import urllib2
import argparse
import subprocess


__author__ = "dslackw"
__version_info__ = (1, 5, 8)
__version__ = "{0}.{1}.{2}".format(*__version_info__)
__license__ = "GNU General Public License v3 (GPLv3)"
__email__ = "d.zlatanidis@gmail.com"


# grep computer architecture
uname = os.uname()
arch = (uname[4])

# SBo fietype binary packages for install
SBo_arch = "*"
SBo_tag = "?_SBo"
SBo_filetype = ".tgz"

# create tmp directory
os.system("mkdir -p /tmp/slpkg/readme/")

# path file record
packages = "/var/log/packages/"
tmp = "/tmp/"

# create dependencies list
dep_results = []
dep_links_results = []

# SlackBuilds repository link
SBo_url = "http://slackbuilds.org/repository/14.1/"

# SlackBuilds repository list
repository = [
    'academic',
    'business',
    'games',
    'ham',
    'misc',
    'office',
    'ruby',
    'accessibility',
    'desktop',
    'gis',
    'haskell',
    'multimedia',
    'perl',
    'system',
    'audio',
    'development',
    'graphics',
    'libraries',
    'network',
    'python'
]

class colors:
    '''
    Print out colors class
    '''
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    CYAN = "\x1b[36m"
    ENDC = "\x1b[0m"

def s_user(user):
    '''
    Check for root user
    '''
    if user != "root":
        print ("\n{}Must have {}`root`{} privileges ...{}\n".format(
                colors.RED, colors.GREEN, colors.RED, colors.ENDC))
        sys.exit()

def rmv_unused(name):
    '''
    Remove unused chars
    '''
    rmv = "><"
    for ch in rmv:
        name = name.replace(ch, "")
    return name

def get_file(link, char):
    '''
    Get filename from links
    '''
    i = 0
    results = []
    for file in range(len(link)):
        i -= 1
        results.append(link[i])
        if link[i] == char:
            break
    return ''.join(results[::-1]).replace('/', '').strip(' ')

def find_package(find_pkg, directory):
    '''
    Find installed packages
    '''
    results = []
    for file in os.listdir(directory):
        if file.startswith(find_pkg):
            results.append(file)
    return results

def url_read(name):
    '''
    Open url and read
    '''
    try:
        f = urllib2.urlopen(name)
        return f.read()
    except urllib2.URLError:
        print ("\nslpkg: error: connection refused")
        sys.exit()

def read_readme(SBo_url, name, site):
    '''
    Read SlackBuild README file
    '''
    s_user(getpass.getuser())
    readme = url_read((SBo_url + site).replace("repository", "slackbuilds"))
    file = open("/tmp/slpkg/readme/" + name + "." + site, "w")
    file.write(readme)
    file.close()

def read_info_slackbuild(SBo_url, name, site):
    '''
    Read .info SlackBuild file
    '''
    s_user(getpass.getuser())
    info = url_read((SBo_url + name + site).replace("repository", "slackbuilds"))
    file = open("/tmp/slpkg/readme/" + name + site, "w")
    file.write(info)
    file.close()

def SBo_search_pkg(name):
    '''
    Find SlackBuilds packages links from repository slackbuilds.org
    '''
    search_name = re.escape(name)
    search_name = ">" + search_name + "<"
    toolbar_width = len(repository)
    sys.stdout.write("Searching `" + name + "` from slackbuilds.org .%s " %
                    (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))
    for kind in repository:
        sys.stdout.write(".")
        sys.stdout.flush()
        SBo_url_sub = SBo_url + kind + "/"
        find_SBo = re.findall(search_name, url_read(SBo_url_sub))
        find_SBo = rmv_unused(" ".join(find_SBo))
        if name in find_SBo:
            return SBo_url_sub + name + "/"

def SBo_slackbuild_dwn(SBo_url, name):
    '''
    Find SlackBuilds packages links for download
    '''
    SBo_url = SBo_url.replace(name + "/", name + ".tar.gz")
    return SBo_url.replace("repository", "slackbuilds")

def SBo_source_dwn(SBo_url, name):
    '''
    Find source code link for download
    '''
    read_info = url_read((SBo_url + name + ".info").replace(
                          "repository", "slackbuilds"))
    if arch == "x86_64":
        for line in read_info.splitlines():
            if line.startswith('DOWNLOAD_x86_64='):
                if len(line) > 18:
                    return line[17:-1]
    for line in read_info.splitlines():
        if line.startswith('DOWNLOAD='):
            return line[10:-1]

def SBo_extra_dwn(SBo_url, name):
    '''
    Find exrtra source code link for download
    '''
    read_info = url_read((SBo_url + name + ".info").replace(
                          "repository", "slackbuilds"))
    results = []
    for line in read_info.splitlines():
        if line.startswith(' '):
            line = line[:-1].replace(" ", "")
        if line.startswith('http'):
            results.append(line)
        if line.startswith('ftp'):
            results.append(line)
    return results

def SBo_requires_pkg(SBo_url, name):
    '''
    Search for package requirements
    '''
    read_info = url_read((SBo_url + name + ".info").replace(
                            "repository", "slackbuilds"))
    for line in read_info.splitlines():
        if line.startswith('REQUIRES="'):
            return line[10:-1]

def SBo_dependencies_pkg(name):
    '''
    Search for package dependecies
    '''
    if name != "%README%":
        SBo_url = SBo_search_pkg(name)
        if SBo_url is None:
            print ("\n\n{}The {}'{}'{} not found{}\n".format(
                    colors.RED, colors.CYAN, name, colors.RED,
                    colors.ENDC))
        else:
            SBo_req = SBo_requires_pkg(SBo_url, name)
            dependencies = SBo_req.split()
            if dependencies != []:
                dep_results.append(dependencies)
            for line in dependencies:
                print
                SBo_dependencies_pkg(line)
            return dep_results

def SBo_dependencies_links_pkg(name):
    '''
    Search for packages dependecies links
    '''
    if name != "%README%":
        SBo_url = SBo_search_pkg(name)
        if SBo_url is None:
            print ("\n\n{}The {}`{}`{} not found{}\n".format(
                    colors.RED, colors.CYAN, name, colors.RED,
                    colors.ENDC))
        else:
            version = ("@" + SBo_version_pkg(SBo_url, name)).split()
            SBo_dwn = SBo_slackbuild_dwn(SBo_url, name).split()
            source_dwn = SBo_source_dwn(SBo_url, name).split()
            extra_dwn = SBo_extra_dwn(SBo_url, name)
            SBo_req = SBo_requires_pkg(SBo_url, name).split()
            if extra_dwn != []:
                flag = ("extra" + str(len(extra_dwn))).split()
                dep_links_results.append(flag)
            dep_links_results.append(extra_dwn)
            dep_links_results.append(version)
            dep_links_results.append(source_dwn)
            dep_links_results.append(SBo_dwn)
            if SBo_req != []:
                dep_links_results.append(SBo_req)
            for line in SBo_req:
                print
                SBo_dependencies_links_pkg(line)
            return dep_links_results

def SBo_version_pkg(SBo_url, name):
    '''
    Find the version package from slackbuilds.org
    '''
    read_info = url_read((SBo_url + name + ".info").replace(
                            "repository", "slackbuilds"))
    for line in read_info.splitlines():
        if line.startswith('VERSION="'):
            return line[9:-1]

def build_extra_pkg(script, source, extra):
    '''
    Build package with extra source
    '''
    pkg_name = script.replace(".tar.gz", "")
    path = subprocess.check_output(["pwd"], shell=True).replace("\n", "/")
    try:
        tar = tarfile.open(script)
        tar.extractall()
        tar.close()
        shutil.copy2(source, pkg_name)
        for es in extra:
            shutil.copy2(es, pkg_name)
        os.chdir(path + pkg_name)
        os.system("sh {}{}{}".format(path, pkg_name + "/", pkg_name + ".SlackBuild"))
    except (OSError, IOError):
        print ("\n{}Wrong file name, Please try again...{}\n".format(
                colors.RED, colors.ENDC))

def build_package(script, source):
    '''
    Build package with source
    '''
    pkg_name = script.replace(".tar.gz", "")
    path = subprocess.check_output(["pwd"], shell=True).replace("\n", "/")
    try:
        tar = tarfile.open(script)
        tar.extractall()
        tar.close()
        shutil.copy2(source, pkg_name)
        os.chdir(path + pkg_name)
        os.system("sh {}{}{}".format(path, pkg_name + "/", pkg_name + ".SlackBuild"))
        os.chdir(path)
    except (OSError, IOError):
        print ("\n{}Wrong file name, Please try again...{}\n".format(
                colors.RED, colors.ENDC))

def pkg_version():
    '''
    Print version, license and email
    '''
    print ("Version : {}".format(__version__))
    print ("Licence : {}".format(__license__))
    print ("Email   : {}".format(__email__))

def pkg_slackbuild(name):
    '''
    Select build package for build with extra source or not
    '''
    s_user(getpass.getuser())
    if len(name) == 2:
        build_package(name[0], name[1])
    elif len(name) > 2:
        build_extra_pkg(name[0], name[1], name[2:])
    else:
        print ("\n{}Must enter at least two arguments{}\n".format(
                colors.RED, colors.ENDC))

def pkg_list(name):
    '''
    List with the installed packages
    '''
    if "all" in name:
        print
        os.chdir(packages)
        os.system("ls * | more")
        print
    if "sbo" in name:
        print
        os.chdir(packages)
        os.system("ls * | grep 'SBo' | more")
        print

def pkg_tracking(name):
    '''
    Find dependecies from package and print all
    '''
    dependencies = SBo_dependencies_pkg(name)
    if dependencies is None:
        pass
    elif dependencies == []:
        print ("\n\n{}No dependencies\n{}".format(colors.GREEN, colors.ENDC))
    else:
        pkg_len = len(name) + 18
        print ("\n\n+" + "=" * pkg_len)
        print ("| {}`{}` {}dependencies :{}".format(colors.CYAN, name,
                                                    colors.YELLOW, colors.ENDC))
        print ("+" + "=" * pkg_len)
        dependencies.reverse()
        print (" |")
        for i in range(len(dependencies)):
            found = " --", str(len(dependencies[i])), " ".join(dependencies[i])
            print (" |")
            print " ".join(found)
        print

def SBo_network(name):
    '''
    View SalckBuild package links, read or install them 
    from slackbuilds.org
    '''
    SBo_url = SBo_search_pkg(name)
    if SBo_url is None:
        print ("\n\n{}The {}`{}`{} not found{}\n".format(colors.RED, colors.CYAN,
                                                     name, colors.RED, colors.ENDC))
    else:
        SBo_req = SBo_requires_pkg(SBo_url, name)
        SBo_dwn = SBo_slackbuild_dwn(SBo_url, name)
        SBo_version = SBo_version_pkg(SBo_url, name)
        source_dwn = SBo_source_dwn(SBo_url, name)
        extra_dwn = " ".join(SBo_extra_dwn(SBo_url, name))
        SBo_name_len = len(name)
        SBo_url_len = (len(SBo_url) + SBo_name_len + 21)
        print ("\n\n+" + "=" * SBo_url_len)
        print ("| {}The {}`{}`{} found in --> {}".format(colors.GREEN, colors.CYAN,
                                                         name, colors.GREEN,
                                                         colors.ENDC + SBo_url))
        print ("+" + "=" * SBo_url_len)
        print ("| {}Download SlackBuild : {}{}".format(colors.GREEN,
                                                       colors.ENDC, SBo_dwn))
        print ("| {}Source Downloads : {}{}".format(colors.GREEN,
                                                    colors.ENDC, source_dwn))
        print ("| {}Extra Downloads : {}{}".format(colors.GREEN,
                                                   colors.ENDC, extra_dwn))
        print ("| {}Package requirements : {}{}".format(colors.YELLOW,
                                                        colors.ENDC, SBo_req))
        print ("+" + "=" * SBo_url_len)
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
                os.system("wget -N " + SBo_dwn)
                os.system("wget -N " + source_dwn)
                if extra_dwn != "":
                    os.system("wget " + extra_dwn)
                break
            elif read == "R" or read == "r":
                site = "README"
                read_readme(SBo_url, name, site)
                os.system("less /tmp/slpkg/readme/{}.{}".format(name, site))
                os.remove("/tmp/slpkg/readme/{}.{}".format(name, site))
            elif read == "F" or read == "f":
                site = ".info"
                read_info_slackbuild(SBo_url, name, site)
                os.system("less /tmp/slpkg/readme/{}{}".format(name, site))
                os.remove("/tmp/slpkg/readme/{}{}".format(name, site))
            elif read == "S" or read == "s":
                site = ".SlackBuild"
                read_info_slackbuild(SBo_url, name, site)
                os.system("less /tmp/slpkg/readme/{}{}".format(name, site))
                os.remove("/tmp/slpkg/readme/{}{}".format(name, site))
            elif read == "B" or read == "b":
                s_user(getpass.getuser())
                script = get_file(SBo_dwn, "/")
                source = get_file(source_dwn, "/")
                print ("\n{}Start -->{}\n".format(colors.GREEN, colors.ENDC))
                os.system("wget -N " + SBo_dwn)
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
                pkg_for_install = name + "-" + SBo_version
                if find_package(pkg_for_install, packages) == []:
                    script = get_file(SBo_dwn, "/")
                    source = get_file(source_dwn, "/")
                    print ("\n{}Start -->{}\n".format(colors.GREEN, colors.ENDC))
                    os.system("wget -N " + SBo_dwn)
                    os.system("wget -N " + source_dwn)
                    extra = []
                    if extra_dwn != "":
                        os.system("wget -N " + extra_dwn)
                        extra_dwn = extra_dwn.split()
                        for link in extra_dwn:
                            extra.append(get_file(link, "/"))
                        build_extra_pkg(script, source, extra)
                        install_pkg = tmp + pkg_for_install + SBo_arch + SBo_tag + SBo_filetype
                        os.system("upgradepkg --install-new {}".format(install_pkg))
                        break
                    build_package(script, source)
                    install_pkg = tmp + pkg_for_install + SBo_arch + SBo_tag + SBo_filetype
                    os.system("upgradepkg --install-new {}".format(install_pkg))
                    break
                else:
                    print ("\n{}The package {}`{}`{} is arlready installed{}\n".format(
                            colors.YELLOW,
                            colors.CYAN, pkg_for_install, colors.YELLOW, colors.ENDC))
                    break
            else:
                break

def SBo_check(name):
    '''
    Check if packages is up to date from slackbuilds.org
    '''
    SBo_file = " ".join(find_package(name, packages))
    if SBo_file == "":
        print ("\n {}The package {}`{}`{} not found on your system{}\n".format(colors.RED,
                colors.CYAN, name, colors.RED, colors.ENDC))
    else:
        SBo_url = SBo_search_pkg(name)
        if SBo_url is None:
            print ("\n\n{}The {}`{}`{} not found{}\n".format(colors.RED, colors.CYAN, name,
                                                             colors.RED, colors.ENDC))
        else:
            SBo_version = SBo_version_pkg(SBo_url, name)
            SBo_dwn = SBo_slackbuild_dwn(SBo_url, name)
            source_dwn = SBo_source_dwn(SBo_url, name)
            extra_dwn = " ".join(SBo_extra_dwn(SBo_url, name))
            name_len = len(name)
            arch_len = len(arch)
            SBo_file = SBo_file[name_len + 1:-arch_len - 7]
            if SBo_version > SBo_file:
                print ("\n\n{} New version is available !!!{}".format(colors.YELLOW,
                                                                      colors.ENDC))
                print ("+" + "=" * 50)
                print ("| {} {}".format(name, SBo_version))
                print ("+\n" + "=" * 50)
                print
                read = raw_input("Would you like to install ? [Y/y] ")
                if read == "Y" or read == "y":
                    s_user(getpass.getuser())
                    pkg_for_install = name + "-" + SBo_version
                    script = get_file(SBo_dwn, "/")
                    source = get_file(source_dwn, "/")
                    print ("\n{}Start -->{}\n".format(colors.GREEN, colors.ENDC))
                    os.system("wget -N " + SBo_dwn)
                    os.system("wget -N " + source_dwn)
                    extra = []
                    if extra_dwn != "":
                        os.system("wget -N " + extra_dwn)
                        extra_dwn = extra_dwn.split()
                        for link in extra_dwn:
                            extra.append(get_file(link, "/"))
                            build_extra_pkg(script, source, extra)
                            install_pkg = tmp + pkg_for_install + SBo_arch + SBo_tag + \
                                          SBo_filetype
                            os.system("upgradepkg --install-new {}".format(install_pkg))
                            sys.exit()
                    build_package(script, source)
                    install_pkg = tmp + pkg_for_install + SBo_arch + SBo_tag + SBo_filetype
                    os.system("upgradepkg --install-new {}".format(install_pkg))
                print
            else:
                print ("\n\n{}Your package is up to date{}\n".format(colors.GREEN, colors.ENDC))

def SBo_build(name):
    '''
    Download, build packages and install or upgrade with all
    dependecies
    '''
    s_user(getpass.getuser())
    dependencies_links = SBo_dependencies_links_pkg(name)
    '''
    create one list for all
    '''
    if dependencies_links is None:
        sys.exit()
    elif dependencies_links != []:
        results = []
        for i in range(len(dependencies_links)):
            for j in range(len(dependencies_links[i])):
                results.append(dependencies_links[i][j])
    '''
    grep only links from list
    '''
    dwn_link = []
    for link in results:
        if link.startswith('http'):
            dwn_link.append(link)
        if link.startswith('ftp'):
            dwn_link.append(link)
    '''
    grep the version
    '''
    version = []
    for ver in results:
        if ver.startswith("@"):
            ver = ver.replace("@", "")
            version.append(ver)
    '''
    upside-down lists
    '''
    version .reverse()
    dwn_link.reverse()
    '''
    get tar archives from link
    '''
    files = []
    for i in range(len(dwn_link)):
        files.append(get_file(dwn_link[i], "/"))
    '''
    removes archive type and store the package name
    '''
    filename = []
    y = 0
    for i in range(len(files) / 2):
        if files[y].endswith("tar.gz"):
            file = files[y]
            file = file[:-7]
            filename.append(file)
            y += 2
    '''
    link sbo filename with version to create package installation
    '''
    filename_version = []
    for i in range(len(filename)):
        filename_version.append(filename[i] + "-" + version[i])
    '''
    remove links and files if packages already installed
    and keep lists for report
    '''
    i = 0
    pkg_for_install = []
    pkg_already_installed = []
    for file in filename_version:
        if find_package(file, packages) == []:
            i += 2
            pkg_for_install.append(file)
        else:
            pkg_already_installed.append(file)
            for j in range(0, 2):
                dwn_link.pop(i)
                files.pop(i)
    '''
    remove double links
    '''
    dwn_link = set(dwn_link)
    '''
    download links if not exist or previously than server
    '''
    for link in dwn_link:
        print ("\n{}Start --> \n{}".format(colors.GREEN, colors.ENDC))
        os.system("wget -N {}".format(link))
    print ("\n")
    '''
    build packages and install slackware packages
    '''
    if pkg_for_install == []:
        for pkg in filename_version:
            print ("{}The package {}`{}`{} is already installed{}".format(colors.YELLOW,
                    colors.CYAN, pkg, colors.YELLOW, colors.ENDC))
    else:
        '''
        check for extra sources
        '''
        if results[0].startswith("extra"):
            extra_Num = int(results[0].replace("extra", ""))
            i = 0
            for i in range(len(files) / 2):
                if len(files) == extra_Num + 2:
                    script = files[0]
                    source = files[1]
                    extra = files[2:]
                    build_extra_pkg(script, source, extra)
                    install_pkg = tmp + pkg_for_install[i] + SBo_arch + SBo_tag + SBo_filetype
                    os.system("upgradepkg --install-new {}".format(install_pkg))
                    break
                else:
                    script = files[0]
                    source = files[1]
                    build_package(script, source)
                    install_pkg = tmp + pkg_for_install[i] + SBo_arch + SBo_tag + SBo_filetype
                    os.system("upgradepkg --install-new {}".format(install_pkg))
                    for j in range(0, 2):
                        files.pop(0)
        else:
            i = 0
            for i in range(len(files) / 2):
                script = files[0]
                source = files[1]
                build_package(script, source)
                install_pkg = tmp + pkg_for_install[i] + SBo_arch + SBo_tag + SBo_filetype
                os.system("upgradepkg --install-new {}".format(install_pkg))
                for j in range(0, 2):
                    files.pop(0)
        for pkg in pkg_for_install:
            if find_package(pkg, packages) != []:
                print ("{}The package {}`{}`{} was installed{}".format(colors.GREEN,colors.CYAN,
                        pkg, colors.GREEN, colors.ENDC))
        for pkg in pkg_already_installed:
            if find_package(pkg, packages) != []:
                print ("{}The package {}`{}`{} is arlready installed{}".format(colors.YELLOW,
                        colors.CYAN, pkg, colors.YELLOW, colors.ENDC))
    print

def pkg_install(name):
    '''
    Install Slackware binary packages
    '''
    s_user(getpass.getuser())
    for i in range(len(name)):
        try:
            print subprocess.check_output('installpkg %s' % name[i], shell=True)
        except subprocess.CalledProcessError:
            print ("\n{}Cannot install {}`{}`{} file not found\n{}".format(colors.RED,
                    colors.CYAN, name[i], colors.RED, colors.ENDC))

def pkg_upgrade(name):
    '''
    Upgrade Slackware binary packages
    '''
    s_user(getpass.getuser())
    for i in range(len(name)):
        try:
            print subprocess.check_output('upgradepkg --install-new %s' % name[i], shell=True)
        except subprocess.CalledProcessError:
            print ("\n{}Cannot install {}`{}`{} file not found\n{}".format(colors.RED,
                    colors.CYAN, name[i], colors.RED, colors.ENDC))

def pkg_reinstall(name):
    '''
    Reinstall Slackware binary packages
    '''
    s_user(getpass.getuser())
    for i in range(len(name)):
        try:
            print subprocess.check_output('upgradepkg --reinstall %s' % name[i], shell=True)
        except subprocess.CalledProcessError:
            print ("\n{}Cannot install {}`{}`{} file not found\n{}".format(colors.RED,
                    colors.CYAN, name[i], colors.RED, colors.ENDC))

def pkg_remove(name):
    '''
    Unistall Slackware binary packages
    '''
    s_user(getpass.getuser())
    pkg = []
    for i in range(len(name)):
        if find_package(name[i], packages) == []:
            print ("{}The package {}`{}`{} not found{}".format(colors.CYAN, colors.ENDC,
                    name[i], colors.CYAN, colors.ENDC))
        else:
            pkg.append(name[i])
    if pkg == []:
        sys.exit()
    print ("These package(s) will be deleted:")
    count = []
    for i in range(len(name)):
        pkg = find_package(name[i], packages)
        if pkg != []:
            print colors.RED + '\n'.join(pkg) + colors.ENDC
            count.append(pkg)
    sum_pkgs = 0
    for i in range(len(count)):
        sum_pkgs += len(count[i])
    if sum_pkgs > 1:
        print ("{} packages matching".format(sum_pkgs))
        print ("Perhaps you need to specify the package")
        print ("Example: slpkg -r pip-1.5.6")
    remove_pkg = raw_input("Are you sure to remove this package(s) [Y/y] ")
    if remove_pkg == "y" or remove_pkg == "Y":
        results_removed = []
        not_found = []
        for i in range(len(name)):
            if find_package(name[i], packages) == []:
                not_found.append(name[i])
            else:
                os.system("removepkg {}".format(name[i]))
                results_removed.append(name[i])
        print
        for file in results_removed:
            if find_package(file, packages) == []:
                print ("{}The package {}`{}`{} removed{}".format(colors.YELLOW,
                        colors.CYAN, file,colors.YELLOW, colors.ENDC))
        for file in not_found:
            print ("{}The package {}`{}`{} not found{}".format(colors.RED, colors.CYAN,
                    file, colors.RED, colors.ENDC))
    print

def pkg_find(name):
    '''
    Find installed Slackware packages
    '''
    print
    for i in range(len(name)):
        if find_package(name[i], packages) == []:
            print ("{}The package {}`{}`{} not found{}".format(colors.RED, colors.CYAN,
                    name[i], colors.RED, colors.ENDC))
        else:
            print (colors.GREEN + "found --> " + colors.ENDC + "\n".join(find_package(
                   name[i], packages)))
    print

def pkg_display(name):
    '''
    Print the Slackware packages contents
    '''
    print
    for i in range(len(name)):
        if find_package(name[i], packages) == []:
            print ("{}The package {}`{}`{} not found{}".format(colors.RED, colors.CYAN,
                    name[i], colors.RED, colors.ENDC))
        else:
            os.system("cat {}{}".format(packages, "\n".join(find_package(name[i], packages))))
    print


def main():
    description = "Utility to help package management in Slackware"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-v", "--verbose", help="print version and exit",
                        action="store_true")
    parser.add_argument("-a", help="auto build package",
                        type=str, nargs="+", metavar=('script', 'source'))
    parser.add_argument("-l", help="list of installed packages", nargs="+", 
                        choices="all sbo".split(), metavar=('all, sbo'))
    parser.add_argument("-t", help="tracking dependencies",
                        type=str, metavar=(''))
    parser.add_argument("-n", help="find from SBo repositority",
                        type=str, metavar=(''))
    parser.add_argument("-c", help="check if your package is up to date",
                        type=str, metavar=(''))
    parser.add_argument("-s", help="download, build & install pkg from SBo",
                        type=str, metavar=(''))
    parser.add_argument("-i", help="install binary packages",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-u", help="install-upgrade packages with new",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-o", help="reinstall the same packages",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-r", help="remove packages",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-f", help="find if packages installed",
                        type=str, nargs="+", metavar=(''))
    parser.add_argument("-d", help="display the contents of the packages",
                        type=str, nargs="+", metavar=(''))
    args = parser.parse_args()
    if args.verbose:
        pkg_version()
    if args.a:
        pkg_slackbuild(args.a)
    if args.l:
        pkg_list(args.l)
    if args.t:
        pkg_tracking(args.t)
    if args.n:
        SBo_network(args.n)
    if args.c:
        SBo_check(args.c)
    if args.s:
        SBo_build(args.s)
    if args.i:
        pkg_install(args.i)
    if args.u:
        pkg_upgrade(args.u)
    if args.o:
        pkg_reinstall(args.o)
    if args.r:
        pkg_remove(args.r)
    if args.f:
        pkg_find(args.f)
    if args.d:
        pkg_display(args.d)
    if not any([args.verbose,
                args.s,
                args.t,
                args.c,
                args.n,
                args.o,
                args.i,
                args.u,
                args.a,
                args.r,
                args.l,
                args.f,
                args.d]):
        os.system("slpkg -h")

if __name__ == "__main__":
    main()
