import os
import sys

currentdir = os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0] + '/'
libdir = currentdir + "libsources/"
metadatadir = currentdir + "metadatas/"
installdir = currentdir + "to_install/"


def choice():
    yesOptions = ["Y", "YES"]
    noOptions = ["N", "NO"]
    while True:
        print_normal("Proceed?[y,n]:", end='', flush=True)
        answer = input()
        if answer.upper() in yesOptions:
            return True
        elif answer.upper() in noOptions:
            return False


def list_packages_print(package_list):
    for package in package_list:
        print_normal(package, end='     ')
    print_normal()


def abort():
    print_error("Aborting")
    jpm_exit(0)


def print_debug(text="", end="\n", flush=False):
    print("\x1b[1;30m" + text, end=end, flush=flush)


def print_normal(text="", end="\n", flush=False):
    print("\x1b[0m" + text, end=end, flush=flush)


def print_error(text="", end="\n", flush=False):
    print("\x1b[0;31m" + text, end=end, flush=flush)


def jpm_exit(exit_code):
    print_normal()
    exit(exit_code)
