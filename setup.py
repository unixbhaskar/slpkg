#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

from distutils.core import setup
from slpkg import __version__, __email__, __author__


setup(
    name='slpkg',
    packages=['slpkg'],
    scripts=['bin/slpkg'],
    version=__version__,
    description="Python tool to manage Slackware packages",
    keywords=["slackware", "slpkg", "upgrade", "install", "remove",
              "view", "slackpkg", "tool"],
    author=__author__,
    author_email=__email__,
    url="https://github.com/dslackw/slpkg",
    package_data={"": ["LICENSE", "README.rst", "CHANGELOG"]},
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 3 - Alpha",
        "Topic :: Intersetup.pynet :: Utilities"],
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
