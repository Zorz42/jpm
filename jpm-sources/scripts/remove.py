from json import load
from os import path, remove
from shutil import rmtree

from globals import print_error, abort, choice, list_packages_print, libdir


def remove_packages(package_names, force=False):
    for package in package_names:
        if not path.isdir(libdir + package):
            print_error(f"Package {package} is not installed.")
            abort()
        with open(f"{libdir}{package}/Info.json") as file:
            metadata = load(file)
            if metadata['Type'] == 'Dependency' and not force:
                print_error(f"Package {package} is a dependency and is probably needed by other packages. "
                            "If you want to remove unused dependencies type 'jpm cleanup'.")
                abort()

    print("Following packages will be removed:")
    list_packages_print(package_names)
    if choice():
        for package_name in package_names:
            rmtree(libdir + package_name)
    else:
        abort()
    print(f"Removed {len(package_names)} packages.")
