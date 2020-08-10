from time import time
from os import stat, path
from urllib.request import urlopen

from globals import cachedir, main_repository
from checkForRepositoryConnection import checkRepConnection
from listPackages import printPackages


def listUrlDir(url: str):
    # parse url files
    with urlopen(url) as f:
        html = f.read().decode("utf-8")
    package_names = []
    for line in html.split("\n"):
        if line.startswith("<tr>") and "alt=\"[DIR]\"" in line:
            package_names.append(line[line.find("href") + 6:].partition("\"")[0][:-1])
    return package_names


def listall():
    if not path.isfile(f"{cachedir}jpm-database.txt") or \
            time() - stat(f"{cachedir}jpm-database.txt").st_ctime >= 86400 and checkRepConnection():
        with open(f"{cachedir}jpm-database.txt", "w") as database:
            database.write("\n".join(listUrlDir(main_repository)))
    print("Listing all installable packages:")
    with open(f"{cachedir}jpm-database.txt") as database:
        printPackages(database.read().split("\n"))
