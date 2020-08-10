from os import path, mkdir
from sys import argv

currentdir = path.split(path.abspath(path.realpath(argv[0])))[0] + "/"
jacdir = "/usr/local/Jac/"
libdir = f"{jacdir}Libraries/"
datadir = f"{jacdir}Data/"
cachedir = f"{jacdir}Caches/"
installdir = f"{cachedir}ToInstall/"

main_repository = "https://jaclang.zorz.si/main-repository/"


def choice():
    yes_options = ["Y", "YES"]
    no_options = ["N", "NO"]
    while True:
        print("Proceed? [y,n]: ", end="", flush=True)
        answer = input()
        if answer.upper() in yes_options:
            return True
        elif answer.upper() in no_options:
            return False


def makeCacheDir():
    if not path.isdir(cachedir):
        mkdir(cachedir)


def printException(exception: Exception):
    print(f"\x1b[1;31m{exception}\x1b[0m")
    exit()


def printWarning(warning: str):
    print(f"\x1b[1;33mWarning: {warning}\x1b[0m")
