#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, shutil

from distutils.core import setup
from bin.config import __version__, __author__, __homepage__, __email__

setup(
    name='slpkg',
    py_modules=['slpkg'],
    version = __version__,
    description = "Python tool to manage Slackware packages",
    keywords = ["slackware", "slpkg", "upgrade", "install", "remove",
		 "view", "slackpkg", "tool"],
    author = __author__,
    author_email = __email__,
    url = __homepage__,
    download_url = __homepage__,
    scripts=['runner'],
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
        man_page = "man/slpkg.8.gz"
        shutil.copy2(man_page, man_path)
        os.chmod(man_path, int('444', 8))
