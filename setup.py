#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='slpkg',
    py_modules=['slpkg'],
    version='0.0.3',
    description="Python tool to manage Slackware packages",
    keywords=["slpkg", "upgrade", "install", "remove", "view", "slackpkg", "tool"],
    author="dslackw",
    author_email="d.zlatanidis@gmail.com",
    url="https://github.com/dslackw/slpkg",
    download_url="https://github.com/dslackw/slpkg/archive/v0.0.3.tar.gz",
    scripts=['bin/slpkg'],
    package_data={"": ["LICENSE", "README.rst", "CHANGELOG"]},
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 0 - Alpha",
        "Topic :: Internet :: Utilities"],
    long_description=open("README.rst").read()
)
