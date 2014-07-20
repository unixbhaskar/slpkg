#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import getpass

from ..messages import s_user
from ..url_read import url_read

# create tmp directory
os.system("mkdir -p /tmp/slpkg/readme/")

def read_readme(sbo_url, name, site):
    '''
    Read SlackBuild README file
    '''
    s_user(getpass.getuser())
    readme = url_read((sbo_url + site).replace("repository", "slackbuilds"))
    file = open("/tmp/slpkg/readme/" + name + "." + site, "w")
    file.write(readme)
    file.close()

def read_info_slackbuild(sbo_url, name, site):
    '''
    Read .info SlackBuild file
    '''
    s_user(getpass.getuser())
    info = url_read((sbo_url + name + site).replace("repository", "slackbuilds"))
    file = open("/tmp/slpkg/readme/" + name + site, "w")
    file.write(info)
    file.close()
