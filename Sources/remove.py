from shutil import rmtree

from globals import choice, libdir, printWarning
from listPackages import printPackages, packageExists
from checkForUnusedPackages import checkForUnusedPackages


class PackageError(Exception):
    pass


def removePackages(package_names: set, force=False):
    # remove packages, force if remove dependencies too
    if not package_names:
        raise PackageError("Cannot remove nothing!")

    # first check if all packages exist
    for package in package_names:
        if not packageExists(package):
            raise PackageError(f"Package {package} is not installed.")

    # get all unused packages to be removed and all dependencies and ignore all packages that are being removed
    unused_packages, _, dependencies = checkForUnusedPackages(package_names)

    # add unused packages to remove list
    package_names.update(unused_packages)

    # do not remove dependencies if not force
    if not force:
        for dependency in dependencies:
            if dependency in package_names:
                printWarning(f"Other packages depend {dependency}, so it will not be removed!")
                package_names.remove(dependency)

    if not package_names:
        print("Nothing to remove!")
        return

    print("Following packages will be removed:")
    printPackages(package_names)

    if choice():
        for package_name in package_names:
            rmtree(libdir + package_name)
        print(f"Removed {len(package_names)} packages.")
