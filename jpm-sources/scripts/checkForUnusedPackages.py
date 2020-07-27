from json import load

from scripts.listPackages import listInstalledPackages
from globals import libdir

used_packages: list
infos: dict


def listDependencies(package_name):
    if package_name not in used_packages:
        used_packages.append(package_name)
        for package in infos[package_name]["Dependencies"]:
            listDependencies(package)


def checkForUnusedPackages(ignore):
    global used_packages, infos
    used_packages, infos = list(), dict()

    installed_packages, to_remove = listInstalledPackages()
    dependencies = set()

    for package in installed_packages:
        with open(f"{libdir}{package}/Info.json") as file:
            infos[package] = load(file)
            dependencies.update(infos[package]["Dependencies"])

    installed_packages = [package for package in installed_packages if package not in ignore]
    packages = [package for package in installed_packages if infos[package]["Type"] == "Package"]

    for package in packages:
        listDependencies(package)

    return [x for x in installed_packages if x not in used_packages], to_remove, dependencies
