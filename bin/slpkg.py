#!/usr/bin/python env python
# -*- coding: utf-8 -*-


import os
import sys
import argparse
import subprocess
from config import __version__


''' path file record '''
__packages__ = "/var/log/packages/"



''' this fuction return the path of the package '''
def find_package(find_pkg):
	find_pkg = subprocess.check_output(["find " +  __packages__ + " -name '{}*' 2> /dev/null".format(find_pkg)],shell=True)
	return find_pkg



''' main function '''
def main():
	description = "Utility to help package management in Slackware"
	parser = argparse.ArgumentParser(description=description)
        parser.add_argument("-v", "--verbose", help="print version and exit",
			    action="store_true")
	parser.add_argument("-s", "--slackbuild", help="auto build package",
                            type=str, nargs=2, metavar=('script','source'))
        parser.add_argument("-u", "--upgrade", help="install-upgrade package with new",
			    type=str, metavar=(''))
	parser.add_argument("-a", "--reinstall", help="reinstall the same package",
			    type=str, metavar=(''))
	parser.add_argument("-r", "--remove", help="remove package",
			    type=str, metavar=(''))
        parser.add_argument("-l", "--list", help="list of installed packages",
			    action="store_true")
	parser.add_argument("-f", "--find", help="find if package installed",
			    type=str, metavar=(''))
	parser.add_argument("-d", "--display", help="display the contents of the package",
			    type=str, metavar=(''))
	args = parser.parse_args()

	'''  print version and exit'''
        if args.verbose:
                print ("Version: {}".format(__version__))

	''' auto build package from slackbuild script '''
        if args.slackbuild:
                slack_script = args.slackbuild[0]
                source_tar = args.slackbuild[1]

                ''' remove file type from slackbuild script and store the name '''
                pkg_name = slack_script.replace(".tar.gz", "")
                if pkg_name != slack_script:
                        pass
                else:
                        pkg_name = slack_script.replace(".tar.bz2", "")

                path = subprocess.check_output(["pwd"], shell=True).replace("\n", "/")
                os.system("tar xvf {}{}".format(path, slack_script))
                os.system("cp {} {}".format(source_tar, pkg_name))
                os.chdir(path + pkg_name)
                os.system("sh {}{}{}".format(path, pkg_name + "/", pkg_name + ".SlackBuild"))

	''' upgrade package with new '''
        if args.upgrade:
		os.system("upgradepkg --install-new {}".format(args.upgrade))

	''' upgrade package with the same '''
	if args.reinstall:
		os.system("upgradepkg --reinstall {}".format(args.reinstall))

	''' uninstall package '''
	if args.remove:
		if find_package(args.remove) == "":
                        os.system("echo -e '\e[31mThe package is not found\e[39m'")
		else:
			os.system("echo -e '\e[93m!!! WARNING !!!\e[39m'")
			remove_pkg = raw_input("Are you sure to remove this package [y/n] ")
			if remove_pkg == "y" or remove_pkg == "Y":
				os.system("removepkg {}".format(args.remove))

	''' view list of installed packages '''
	if args.list:
		os.system("ls " + __packages__ + "* | more")

	''' find if package installed on your system '''
	if args.find:
		if find_package(args.find) == "":		
			os.system("echo -e '\e[31mThe package is not installed on your system\e[39m'")
		else:
			os.system("echo -e '\e[32mThe package is installed on your system\e[39m'")
	
	''' print the package contents '''
	if args.display:
		if find_package(args.display) == "":
			os.system("echo -e '\e[31mThe package is not found\e[39m'")
		else:
			os.system("cat {}".format(find_package(args.display)))
	''' fix null arguments '''
	if not any([args.verbose, args.upgrade, args.reinstall, args.slackbuild,
		 args.remove, args.list, args.find, args.display]):
		os.system("slpkg -h")


if __name__ == "__main__":
    main()
