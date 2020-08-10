from listPackages import listInstalledPackages
from globals import libdir
from util import loadInfo

dependencies: set
used_packages: set
infos: dict


def listDependencies(package_name: str):
    # walk through packages and their dependencies
    if package_name not in used_packages and package_name in infos.keys():
        used_packages.add(package_name)
        for package in infos[package_name]["Dependencies"]:
            dependencies.add(package)
            listDependencies(package)


def checkForUnusedPackages(ignore: set):
    # lists unused dependencies, files to remove and all packages that are a dependency
    global dependencies, used_packages, infos
    dependencies, used_packages, infos = set(), set(), {}

    installed_packages, to_remove = listInstalledPackages()
    installed_packages = installed_packages - ignore

    # collect all infos of installed packages
    for package in installed_packages:
        infos[package] = loadInfo(f"{libdir}{package}/Info.json")
        if infos[package]["Type"] == "Package":
            listDependencies(package)

    return installed_packages - used_packages, to_remove, dependencies
