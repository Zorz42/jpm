from os import path, listdir, system

from globals import list_packages_print, installdir, choice, abort, libdir
from scripts.dep_tree import build_dep_tree
from scripts.install_package import install_package


def install(package_names):
    if listdir(installdir):
        system(f"rm {installdir}*")

    for package in package_names:
        if not path.isdir(f"{installdir}{package}"):
            build_dep_tree(package)
    to_install = [".".join(x.split(".")[:-1]) for x in listdir(installdir)]
    already_installed = [x for x in listdir(libdir)]
    to_install = [x for x in to_install if x not in already_installed]

    if not to_install:
        print("Nothing to install!")
    else:
        print("Following packages will be installed:")
        list_packages_print(to_install)
        if not choice():
            if listdir(installdir):
                system(f"rm {installdir}*")
            abort()
        for package in to_install:
            install_package(package, package not in package_names)
    if listdir(installdir):
        system(f"rm {installdir}*")
