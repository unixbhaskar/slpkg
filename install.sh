#!/bin/sh

# Copyright 2014 Dimitris Zlatanidis Greece-Orestiada
# All rights reserved.
#
# Redistribution and use of this script, with or without modification, is
# permitted provided that the following conditions are met:
#
# 1. Redistributions of this script must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
#  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO
#  EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

PRGNAM=slpkg
VERSION=${VERSION:-2.0.3}
TAG=${TAG:-_dsw}

cd ..
# Installation script.
# With this script allows you to install the slpkg as a package SlackBuild.
# Select archive to copy in slackbuild directory
# support wget download.
if [ -f $PRGNAM-$VERSION.zip ]; then
    cp $PRGNAM-$VERSION.zip $PRGNAM-$VERSION/slackbuild
    cd $PRGNAM-$VERSION/slackbuild
    chmod +x $PRGNAM.SlackBuild
    ./$PRGNAM.SlackBuild
    rm $PRGNAM-$VERSION.zip 
elif [ -f v$VERSION.zip ]; then
    cp v$VERSION.zip $PRGNAM-$VERSION/slackbuild
    cd $PRGNAM-$VERSION/slackbuild
    chmod +x $PRGNAM.SlackBuild
    ./$PRGNAM.SlackBuild
    rm v$VERSION.zip
elif [ -f $PRGNAM-$VERSION.tar.gz ]; then
    cp $PRGNAM-$VERSION.tar.gz $PRGNAM-$VERSION/slackbuild
    cd $PRGNAM-$VERSION/slackbuild
    chmod +x $PRGNAM.SlackBuild
    ./$PRGNAM.SlackBuild
    rm $PRGNAM-$VERSION.tar.gz
else
    cp v$VERSION.tar.gz $PRGNAM-$VERSION/slackbuild
    cd $PRGNAM-$VERSION/slackbuild
    chmod +x $PRGNAM.SlackBuild
    ./$PRGNAM.SlackBuild
    rm v$VERSION.tar.gz 
fi
# install or upgrade with new version
upgradepkg --install-new /tmp/$PRGNAM-$VERSION-*$TAG.tgz
