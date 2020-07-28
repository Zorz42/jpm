from os import path
from shutil import rmtree

from globals import throwError, choice, libdir
from scripts.listPackages import printPackages
from scripts.checkForUnusedPackages import checkForUnusedPackages


def removePackages(package_names: set, force=False):
    if not package_names:
        throwError("Cannot remove nothing!")

    for package in package_names:
        if not path.isdir(libdir + package):
            throwError(f"Package {package} is not installed.")

    unused_packages, _, dependencies = checkForUnusedPackages(package_names)

    if not force:
        for dependency in dependencies:
            if dependency in package_names:
                package_names.remove(dependency)
    package_names += unused_packages

    if not package_names:
        print("Nothing to remove!")
        return

    print("Following packages will be removed:")
    printPackages(list(package_names))

    if choice():
        for package_name in package_names:
            rmtree(libdir + package_name)
        print(f"Removed {len(package_names)} packages.")
