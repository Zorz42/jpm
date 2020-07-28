from os import listdir

from globals import libdir
from scripts.verify import packageExists


def printPackages(packages: list):
    # pretty print packages
    for package in packages:
        print(package, end="     ")
    print()


def listInstalledPackages():
    # list all valid packages and invalid files/directories
    to_remove, valid_packages = [], []
    for package in listdir(libdir):
        if packageExists(package):
            valid_packages.append(package)
        else:
            to_remove.append(package)
    return valid_packages, to_remove


def listPackages():
    installed_packages, to_remove = listInstalledPackages()
    if installed_packages:
        print(f"Listing {len(installed_packages)} installed packages:")
        printPackages(installed_packages)
    else:
        print(f"No packages installed.")
    if to_remove:
        print("Following files/directories do not belong into the jaclang-libraries directory:")
        printPackages(to_remove)
        print("Type \"jpm cleanup\" to remove them.")
