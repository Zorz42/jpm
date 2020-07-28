from os import listdir, path

from globals import libdir


def printPackages(packages: list):
    for package in packages:
        print(package, end="     ")
    print()


def packageExists(package_name: str):
    return path.isdir(libdir + package_name)


def listInstalledPackages():
    to_remove, valid_packages = [], []
    for file in listdir(libdir):
        if packageExists(file):
            valid_packages.append(file)
        else:
            to_remove.append(file)
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
