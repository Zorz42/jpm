from os import path, listdir, system

from httplib2 import Http

from globals import print_error, print_normal, print_debug, list_packages_print, installdir, metadatadir, choice, \
    abort, jpm_exit
from scripts.dep_tree import build_dep_tree
from scripts.install_package import install_package


def check_if_package_exists(package_name):
    h = Http()
    resp = h.request("https://jaclang.zorz.si/main-repository/metadatas/" + package_name + ".json", 'HEAD')
    return int(resp[0]['status']) < 400


def install(package_names):
    print_debug("Starting to install...")
    if listdir(installdir):
        system("rm " + installdir + "*")
    for package in package_names:
        if not check_if_package_exists(package):
            print_error("Package " + package + " does not exist.")
            jpm_exit(1)
        print_debug("Building dependency tree for " + package)
        if not path.isfile(installdir + package + ".json"):
            build_dep_tree(package)
    to_install = [x.split('.')[0] for x in listdir(installdir)]
    already_installed = [x.split('.')[0] for x in listdir(metadatadir)]
    to_install = [x for x in to_install if x not in already_installed]
    if not to_install:
        print_normal("Nothing to install!")
    else:
        print_normal("Following packages will be installed:")
        list_packages_print(to_install)
        if not choice():
            if listdir(installdir):
                system("rm " + installdir + "*")
            abort()
        print_debug(end='')
        for package in to_install:
            print_debug("Installing " + str(package) + " ... ", end='', flush=True)
            install_package(package, package not in package_names)
            print_debug("DONE")
    if listdir(installdir):
        system("rm " + installdir + "*")
    print_normal("Installed " + str(len(to_install)) + " packages.")
