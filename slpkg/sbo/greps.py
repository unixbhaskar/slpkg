#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from slpkg.url_read import url_read
from slpkg.__metadata__ import uname, arch

def sbo_source_dwn(sbo_url, name):
    '''
    Grep source downloads links
    '''
    read_info = url_read(sbo_url + name + ".info")
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
    Grep extra source downloads links
    '''
    read_info = url_read(sbo_url + name + ".info")
    extra = []
    for line in read_info.split():
        if line.endswith('"'):
            line = line[:-1].replace('"', '')
        if line.startswith('http'):
            extra.append(line)
        if line.startswith('ftp'):
            extra.append(line)
    return extra

def sbo_requires_pkg(sbo_url, name):
    '''
    Grep package requirements
    '''
    read_info = url_read(sbo_url + name + ".info")
    for line in read_info.splitlines():
        if line.startswith('REQUIRES="'):
            return line[10:-1]

def sbo_prgnam_pkg(sbo_url, name):
    '''
    Grep program name
    '''
    read_info = url_read(sbo_url + name + ".info")
    for line in read_info.splitlines():
        if line.startswith('PRGNAM="'):
            return line[8:-1]

def sbo_version_pkg(sbo_url, name):
    '''
    Grep package version
    '''
    read_info = url_read(sbo_url + name + ".info")
    for line in read_info.splitlines():
        if line.startswith('VERSION="'):
            return line[9:-1]
