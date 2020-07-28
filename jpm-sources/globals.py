from os import path, remove
from sys import argv

from httplib2 import Http

currentdir = path.split(path.abspath(path.realpath(argv[0])))[0] + "/"
libdir = "/usr/local/share/jaclang-libraries/"
datadir = "/usr/local/share/jaclang-data/"
installdir = currentdir + "to-install/"
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


def throwError(text="", end="\n", flush=False):
    print(f"\x1b[0;31m{text}\x1b[0m", end=end, flush=flush)
    exit()


def removeFileIfExists(file_path: str):
    if path.isfile(file_path):
        remove(file_path)


def downloadFile(url: str, file_destination: str):
    response, content = Http().request(url)
    if response.status == 200:
        with open(file_destination, "wb") as file:
            file.write(content)
    else:
        print(f"Warning: {url} could not be downloaded!")
