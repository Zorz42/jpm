from os import listdir, path

from globals import libdir


def printPackages(package_list):
    for package in package_list:
        print(package, end='     ')
    print()


def listInstalledPackages():
    all_files = listdir(libdir)
    to_remove = []
    valid_packages = []
    for file in all_files:
        if path.isfile(libdir + file):
            to_remove.append(file)
        else:
            valid_packages.append(file)
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
        print("Type 'jpm cleanup' to remove them.")
