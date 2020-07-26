from os import path, listdir, system

from httplib2 import Http

from globals import print_error, print_normal, print_debug, list_packages_print, installdir, choice, \
    abort, jpm_exit, libdir
from scripts.dep_tree import build_dep_tree
from scripts.install_package import install_package


def check_if_package_exists(package_name):
    resp = Http().request(f"https://jaclang.zorz.si/main-repository/{package_name}/Info.json", 'HEAD')
    return int(resp[0]['status']) < 400


def install(package_names):
    print_debug("Installing...")
    if listdir(installdir):
        system(f"rm {installdir}*")

    for package in package_names:
        if not check_if_package_exists(package):
            print_error(f"Package {package} does not exist.")
            jpm_exit(1)
        print_debug(f"Building dependency tree for {package}")
        if not path.isdir(f"{installdir}{package}"):
            build_dep_tree(package)

    to_install = [".".join(x.split(".")[:-1]) for x in listdir(installdir)]
    already_installed = [x for x in listdir(libdir)]
    to_install = [x for x in to_install if x not in already_installed]

    if not to_install:
        print_normal("Nothing to install!")
    else:
        print_normal("Following packages will be installed:")
        list_packages_print(to_install)
        if not choice():
            if listdir(installdir):
                system(f"rm {installdir}*")
            abort()
        print_debug(end='')
        for package in to_install:
            print_debug(f"Installing {str(package)} ... ", end='', flush=True)
            install_package(package, package not in package_names)
            print_debug("DONE")
    if listdir(installdir):
        system(f"rm {installdir}*")
    print_normal(f"Installed {len(to_install)} packages.")
