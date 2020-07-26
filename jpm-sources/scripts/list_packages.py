from json import load
from os import listdir, path

from globals import list_packages_print, libdir
from scripts.verify import verify_package_json


def list_installed_packages():
    all_files = listdir(libdir)
    to_remove = []
    valid_packages = []
    for file in all_files:
        if path.isfile(libdir + file):
            to_remove.append(file)
        else:
            valid_packages.append(file)
    return valid_packages, to_remove


def list_packages():
    print("Listing all installed packages:")
    (installed_packages, to_remove) = list_installed_packages()
    for package in installed_packages:
        print(package)
    if to_remove:
        print("Following files/directories are invalid json files and do not belong here:")
        list_packages_print(to_remove)
        print("Type 'jpm cleanup' to remove them.")
