#!/usr/bin/python
# -*- coding: utf-8 -*-

# setup.py file is part of slpkg.

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Utility for easy management packages in Slackware

# https://github.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import gzip
import shutil

from slpkg import __version__, __email__, __author__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="slpkg",
    packages=["slpkg", "slpkg/sbo", "slpkg/pkg", "slpkg/slack"],
    scripts=["bin/slpkg"],
    version=__version__,
    description="Python tool to manage Slackware packages",
    keywords=["slackware", "slpkg", "upgrade", "install", "remove",
              "view", "slackpkg", "tool", "build"],
    author=__author__,
    author_email=__email__,
    url="https://github.com/dslackw/slpkg",
    package_data={"": ["LICENSE", "README.rst", "CHANGELOG"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Unix Shell",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Archiving :: Packaging",
        "Topic :: System :: Software Distribution",
        "Topic :: Utilities"],
    long_description=open("README.rst").read()
    )

# install man page and blacklist configuration
# file if not exists.
if "install" in sys.argv:
    man_path = "/usr/man/man8/"
    os.system("mkdir -p {0}".format(man_path))
    if os.path.exists(man_path):
        man_page = "man/slpkg.8"
        gzip_man = "man/slpkg.8.gz"
        print("Installing man pages")
        f_in = open(man_page, "rb")
        f_out = gzip.open(gzip_man, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        shutil.copy2(gzip_man, man_path)
        os.chmod(man_path, int("444", 8))
    conf_path = "/etc/slpkg/"
    if not os.path.exists(conf_path):
        os.system("mkdir -p {0}".format(conf_path))
        print("Installing blacklist configuration file")
        black_file = "conf/blacklist"
        shutil.copy2(black_file, conf_path)
