#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import tarfile
import subprocess

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

