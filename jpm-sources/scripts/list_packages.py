from json import load
from os import listdir

from globals import print_normal, list_packages_print, metadatadir
from scripts.verify import verify_package_json


def list_installed_packages():
    all_files = listdir(metadatadir)
    to_remove = []
    for file in all_files:
        if len(file.split('.')) < 2:
            to_remove.append(file)
        elif file.split('.')[1] != 'json' or len(file.split('.')) != 2:
            to_remove.append(file)
        else:
            with open(metadatadir + file) as metafile:
                if not verify_package_json(load(metafile), file.split('.')[0], False):
                    to_remove.append(file)
    return [x.split('.')[0] for x in all_files if x not in to_remove], to_remove


def list_packages():
    print_normal("Listing all installed packages:")
    (installed_packages, to_remove) = list_installed_packages()
    for package in installed_packages:
        print_normal(package)
    if to_remove:
        print_normal("Following files/directories are invalid json files and do not belong here:")
        list_packages_print(to_remove)
        print_normal("Type 'jpm cleanup' to remove them.")
