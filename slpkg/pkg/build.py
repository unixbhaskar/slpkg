#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import tarfile
import subprocess

from slpkg.messages import pkg_not_found

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
        os.system("sh {0}{1}{2}".format(path, pkg_name + "/", pkg_name + ".SlackBuild"))
    except (OSError, IOError):
        pkg_not_found(pkg='', message="Wrong file")

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
        os.system("sh {0}{1}{2}".format(path, pkg_name + "/", pkg_name + ".SlackBuild"))
        os.chdir(path)
    except (OSError, IOError):
        pkg_not_found(pkg='', message="Wrong file")
