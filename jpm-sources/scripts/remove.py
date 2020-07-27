from json import load
from os import path
from shutil import rmtree

from globals import throw_error, choice, libdir
from scripts.listPackages import print_packages


def remove_packages(package_names, force=False):
    if not package_names:
        throw_error("Cannot remove nothing!")
    for package in package_names:
        if not path.isdir(libdir + package):
            throw_error(f"Package {package} is not installed.")
        with open(f"{libdir}{package}/Info.json") as file:
            metadata = load(file)
            if not force and metadata['Type'] == "Dependency":
                throw_error(f"Package {package} is needed by other packages.")

    print("Following packages will be removed:")
    print_packages(package_names)
    if choice():
        for package_name in package_names:
            rmtree(libdir + package_name)
        print(f"Removed {len(package_names)} packages.")
