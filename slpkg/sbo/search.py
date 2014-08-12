#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys

from slpkg.colors import colors
from slpkg.url_read import url_read
from slpkg.functions import get_file
from slpkg.__metadata__ import slpkg_path

from slpkg.pkg.find import find_package

from slpkg.slack.slack_version import slack_ver

from file_size import server_file_size, local_file_size

def sbo_search_pkg(name):
    '''
    Find SlackBuilds packages from slackbuilds.org
    '''
    try:
        sbo_location = []
        os.system("mkdir -p {0}{1}".format(slpkg_path, "sbo_repo/"))
        sbo_url = ("http://slackbuilds.org/slackbuilds/{0}/".format(slack_ver()))
        '''
        Read SLACKBUILDS.TXT from slackbuilds.org and write in /tmp/slpkg/sbo_repo/
        directory if not exist
        '''
        if find_package("SLACKBUILDS.TXT", slpkg_path + "sbo_repo/") == []:
            print ("\nslpkg initialization ...")
            SLACKBUILDS_TXT = url_read((
                "http://slackbuilds.org/slackbuilds/{0}/SLACKBUILDS.TXT".format(slack_ver())))
            ChangeLog_txt = url_read((
                "http://slackbuilds.org/slackbuilds/{0}/ChangeLog.txt".format(slack_ver())))
            sbo = open("{0}sbo_repo/SLACKBUILDS.TXT".format(slpkg_path), "w")
            sbo.write(SLACKBUILDS_TXT)
            sbo.close()
            log = open("{0}sbo_repo/ChangeLog.txt".format(slpkg_path), "w")
            log.write(ChangeLog_txt)
            log.close()
        '''
        We take the size of ChangeLog.txt from the server and locally
        '''
        server = int(''.join(server_file_size(sbo_url + "ChangeLog.txt")))
        local = int(local_file_size(slpkg_path + "sbo_repo/ChangeLog.txt"))
        '''
        If the two files differ in size delete and replaced with new
        '''
        if server != local:
            os.remove("{0}sbo_repo/{1}".format(slpkg_path, "SLACKBUILDS.TXT"))
            os.remove("{0}sbo_repo/{1}".format(slpkg_path, "ChangeLog.txt"))
            print ("\nNEWS in ChangeLog.txt, slpkg initialization ...")
            SLACKBUILDS_TXT = url_read((
                "http://slackbuilds.org/slackbuilds/{0}/SLACKBUILDS.TXT".format(slack_ver())))
            ChangeLog_txt = url_read((
                "http://slackbuilds.org/slackbuilds/{0}/ChangeLog.txt".format(slack_ver())))
            sbo = open("{0}sbo_repo/SLACKBUILDS.TXT".format(slpkg_path), "w")
            sbo.write(SLACKBUILDS_TXT)
            sbo.close()
            log = open("{0}sbo_repo/ChangeLog.txt".format(slpkg_path), "w")
            log.write(ChangeLog_txt)
            log.close()
        '''
        Search for package path from SLACKBUILDS.TXT file
        '''
        for line in open(slpkg_path + "sbo_repo/SLACKBUILDS.TXT", "r"):
            if line.startswith('SLACKBUILD LOCATION'):
                sbo_location.append(line.replace('SLACKBUILD LOCATION: ./', ''))
        for location in sbo_location:
            location = location.replace('\n', '')
            if get_file(location, '/') == name:
                return sbo_url + location.replace(name, '') + name + "/"
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()
