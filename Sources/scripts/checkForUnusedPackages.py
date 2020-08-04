from json import load

from scripts.listPackages import listInstalledPackages
from globals import libdir

used_packages: set
infos: dict


def listDependencies(package_name: str):
    # walk through packages and their dependencies
    if package_name not in used_packages:
        used_packages.add(package_name)
        for package in infos[package_name]["Dependencies"]:
            listDependencies(package)


def checkForUnusedPackages(ignore: set):
    # lists unused dependencies, files to remove and all packages that are a dependency
    global used_packages, infos
    used_packages, infos = set(), {}

    installed_packages, to_remove = listInstalledPackages()
    dependencies = set()

    # collect all infos of installed packages
    for package in installed_packages:
        with open(f"{libdir}{package}/Info.json") as info_file:
            infos[package] = load(info_file)
            dependencies.update(infos[package]["Dependencies"])

    # get installed packages and packages
    installed_packages = [package for package in installed_packages if package not in ignore]
    packages = [package for package in installed_packages if infos[package]["Type"] == "Package"]

    for package in packages:
        listDependencies(package)

    return {x for x in installed_packages if x not in used_packages}, to_remove, dependencies
