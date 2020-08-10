from json import load

from listPackages import listInstalledPackages
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
    dependencies = set()

    installed_packages, to_remove = listInstalledPackages()

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

    unused_packages = {x for x in installed_packages if x not in used_packages}
    unused_packages.update(ignore)

    return unused_packages, to_remove, [dep for dep in dependencies if dep not in unused_packages]
