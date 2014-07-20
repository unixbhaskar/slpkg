#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from ..url_read import url_read
from ..__metadata__ import uname, arch

def sbo_source_dwn(sbo_url, name):
    '''
    Find source code link for download
    '''
    read_info = url_read((sbo_url + name + ".info").replace(
                          "repository", "slackbuilds"))
    if arch == "x86_64":
        for line in read_info.splitlines():
            if line.startswith('DOWNLOAD_x86_64='):
                if len(line) > 18:
                    return line[17:-1]
    for line in read_info.splitlines():
        if line.startswith('DOWNLOAD='):
            return line[10:-1]

def sbo_extra_dwn(sbo_url, name):
    '''
    Find exrtra source code link for download
    '''
    read_info = url_read((sbo_url + name + ".info").replace(
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

def sbo_requires_pkg(sbo_url, name):
    '''
    Search for package requirements
    '''
    read_info = url_read((sbo_url + name + ".info").replace(
                            "repository", "slackbuilds"))
    for line in read_info.splitlines():
        if line.startswith('REQUIRES="'):
            return line[10:-1]

def sbo_version_pkg(sbo_url, name):
    '''
    Find the version package from slackbuilds.org
    '''
    read_info = url_read((sbo_url + name + ".info").replace(
                            "repository", "slackbuilds"))
    for line in read_info.splitlines():
        if line.startswith('VERSION="'):
            return line[9:-1]
