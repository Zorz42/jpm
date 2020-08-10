from os import path, remove, mkdir
from sys import argv

from urllib.request import urlopen, Request
from urllib.error import HTTPError

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


def removeFileIfExists(file_path: str):
    if path.isfile(file_path):
        remove(file_path)


def downloadFile(url: str, file_destination: str):
    with urlopen(url) as f:
        html = f.read()
    with open(file_destination, "wb") as file:
        file.seek(0)
        file.write(html)
        file.truncate()


def urlExists(url: str):
    request = Request(url)
    request.get_method = lambda: 'HEAD'

    try:
        urlopen(request)
        return True
    except HTTPError:
        return False


def makeCacheDir():
    if not path.isdir(cachedir):
        mkdir(cachedir)


def printException(exception: Exception):
    print(f"\x1b[0;31m{exception}\x1b[0m")
    exit()
