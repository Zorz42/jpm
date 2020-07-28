from scripts.updateDatabase import updateDatabase
from scripts.checkForRepositoryConnection import checkRepConnection
from scripts.listPackages import printPackages


def listall():
    if checkRepConnection():
        updateDatabase()
    print("Listing all installable packages:")
    with open(f"/usr/local/share/jaclang-data/jpm-database.txt") as database:
        printPackages(database.read().split("\n"))
