#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import getpass
import tarfile

from slpkg.messages import pkg_not_found, s_user

def build_package(script, source, extra, path):
    '''
    Build package from source
    '''
    s_user(getpass.getuser())
    pkg_name = script.replace(".tar.gz", "")
    try:
        tar = tarfile.open(script)
        tar.extractall()
        tar.close()
        shutil.copy2(source, pkg_name)
        for src in extra:
            shutil.copy2(src, pkg_name)
        os.chdir(path + pkg_name)
        os.system("sh {0}.SlackBuild".format(pkg_name))
        os.chdir(path)
    except (OSError, IOError):
        message = "Wrong file"
        bol, eol, pkg = "\n", "\n", ""
        pkg_not_found(bol, pkg, message, eol)
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
