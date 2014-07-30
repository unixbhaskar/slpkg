#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import getpass
import tarfile
import subprocess

from slpkg.messages import pkg_not_found, s_user

def build_package(script, source, extra):
    '''
    Build package with source
    '''
    s_user(getpass.getuser())
    pkg_name = script.replace(".tar.gz", "")
    path = subprocess.check_output(["pwd"], shell=True).replace("\n", "/")
    try:
        tar = tarfile.open(script)
        tar.extractall()
        tar.close()
        shutil.copy2(source, pkg_name)
        for src in extra:
            shutil.copy2(src, pkg_name)
        os.chdir(path + pkg_name)
        os.system("sh {0}{1}{2}".format(path, pkg_name + "/", pkg_name + ".SlackBuild"))
        os.chdir(path)
    except (OSError, IOError):
        message = "Wrong file"
        bol, eol, pkg = "\n", "\n", ""
        pkg_not_found(bol, pkg, message, eol)

