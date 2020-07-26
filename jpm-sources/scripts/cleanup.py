from json import load
from os import path, remove
from shutil import rmtree

from globals import print_debug, print_normal, abort, list_packages_print, choice
from scripts.list_packages import list_installed_packages
from scripts.remove import remove_packages

used_packages = []
metadatas = {}


def list_dependencies(package_name):
    if package_name not in used_packages:
        used_packages.append(package_name)
        if 'dependencies' not in metadatas.keys():
            for package in metadatas[package_name]['dependencies']:
                list_dependencies(package)


def cleanup():
    print_debug("Starting cleanup")
    print_debug("Getting installed packages ... ", end='', flush=True)
    (installed_packages, to_remove) = list_installed_packages()
    print_debug("DONE")
    print_debug("Getting metadatas of installed packages ... ", end='', flush=True)
    for package in installed_packages:
        with open(metadatadir + package + ".json") as file:
            metadatas[package] = load(file)
    print_debug("DONE")
    print_debug("Listing dependencies and packages ... ", end='', flush=True)
    dependencies = []
    packages = []
    for package in installed_packages:
        if metadatas[package]['type'] == 'package':
            packages.append(package)
        else:
            dependencies.append(package)
    print_debug("DONE")
    print_debug("Listing unused packages ... ", end='', flush=True)
    for package in packages:
        list_dependencies(package)
    unused_packages = [x for x in installed_packages if x not in used_packages]
    print_debug("DONE")
    if not unused_packages:
        print_normal("All packages are being used.")
    else:
        remove_packages(unused_packages, True)
    if to_remove:
        print_normal(
            "Following files/directories are not valid packages and thus do not belong here, so they will be deleted:")
        list_packages_print(to_remove)
        if choice():
            for file in to_remove:
                if path.isfile(metadatadir + file):
                    remove(metadatadir + file)
                else:
                    rmtree(metadatadir + file)
            print_normal("Removed " + str(len(to_remove)) + " files/directories.")
        else:
            abort()
