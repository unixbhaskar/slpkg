#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import getpass
from slpkg.messages import s_user
from slpkg.url_read import url_read
from slpkg.__metadata__ import slpkg_path

# create tmp directory if not exist
os.system("mkdir -p /tmp/readme/")

def read_readme(sbo_url, name, site):
    '''
    Read SlackBuild README file
    '''
    s_user(getpass.getuser())
    readme = url_read((sbo_url + site).replace("repository", "slackbuilds"))
    file = open("{0}readme/{1}.{2}".format(slpkg_path, name, site), "w")
    file.write(readme)
    file.close()

def read_info_slackbuild(sbo_url, name, site):
    '''
    Read info SlackBuild file
    '''
    s_user(getpass.getuser())
    info = url_read((sbo_url + name + site).replace("repository", "slackbuilds"))
    file = open("{0}readme/{1}{2}".format(slpkg_path, name, site), "w")
    file.write(info)
    file.close()
