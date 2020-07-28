from time import time
from os import stat

from globals import datadir
from scripts.updateDatabase import updateDatabase
from scripts.checkForRepositoryConnection import checkRepConnection
from scripts.listPackages import printPackages


def listall():
    if time() - stat(f"{datadir}newestjaclangversion.txt").st_ctime >= 86400 and checkRepConnection():
        updateDatabase()
    print("Listing all installable packages:")
    with open(f"/usr/local/share/jaclang-data/jpm-database.txt") as database:
        printPackages(database.read().split("\n"))
