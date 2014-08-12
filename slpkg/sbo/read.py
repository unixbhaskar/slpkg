#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import getpass

from slpkg.messages import s_user
from slpkg.url_read import url_read
from slpkg.__metadata__ import slpkg_path

# create tmp directory if not exist
os.system("mkdir -p {0}readme/".format(slpkg_path))

def read_readme(sbo_url, name, site):
    '''
    Read SlackBuild README file
    '''
    s_user(getpass.getuser())
    readme = url_read(sbo_url + site)
    f = open("{0}readme/{1}.{2}".format(slpkg_path, name, site), "w")
    f.write(readme)
    f.close()

def read_info_slackbuild(sbo_url, name, site):
    '''
    Read info SlackBuild file
    '''
    s_user(getpass.getuser())
    info = url_read(sbo_url + name + site)
    f = open("{0}readme/{1}{2}".format(slpkg_path, name, site), "w")
    f.write(info)
    f.close()
