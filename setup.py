#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

from slpkg import __version__, __email__, __author__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='slpkg',
    packages=['slpkg', 'slpkg/sbo', 'slpkg/pkg', 'slpkg/slack'],
    scripts=['bin/slpkg'],
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

if 'install' in sys.argv:
    man_path = "/usr/man/man8/"
    os.system("mkdir -p {}".format(man_path))
    if os.path.exists(man_path):
        print("Installing man pages")
        man_page = "man/slpkg.8"
        shutil.copy2(man_page, man_path)
        os.chmod(man_path, int('444', 8))

