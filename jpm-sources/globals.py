from os import path
from sys import argv

currentdir = path.split(path.abspath(path.realpath(argv[0])))[0] + '/'
libdir = "/usr/local/share/jaclang-libraries/"
datadir = "/usr/local/share/jaclang-data/"
installdir = currentdir + "to-install/"


def choice():
    yes_options = ["Y", "YES"]
    no_options = ["N", "NO"]
    while True:
        print("Proceed?[y,n]: ", end='', flush=True)
        answer = input()
        if answer.upper() in yes_options:
            return True
        elif answer.upper() in no_options:
            return False


def list_packages_print(package_list):
    for package in package_list:
        print(package, end='     ')
    print()


def abort():
    print_error("Aborting")
    jpm_exit(0)


def print_error(text="", end="\n", flush=False):
    print("\x1b[0;31m" + str(text), end=end, flush=flush)


def jpm_exit(exit_code):
    print("\x1b[0m")
    exit(exit_code)
