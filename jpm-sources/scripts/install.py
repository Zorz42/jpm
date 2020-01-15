import httplib2

from scripts.dep_tree import *
from scripts.install_package import *


def check_if_package_exists(package_name):
    h = httplib2.Http()
    resp = h.request("https://jaclang.zorz.si/main-repository/" + package_name + "/metadata.json", 'HEAD')
    return int(resp[0]['status']) < 400


def install(package_names):
    print_debug("Starting to install...")
    if os.listdir(installdir):
        os.system("rm " + installdir + "*")
    for package in package_names:
        if not check_if_package_exists(package):
            print_error("Package " + package + " does not exist.")
            jpm_exit(1)
        print_debug("Building dependency tree for " + package)
        if not os.path.isfile(installdir + package + ".json"):
            build_dep_tree(package)
    to_install = [x.split('.')[0] for x in os.listdir(installdir)]
    already_installed = [x.split('.')[0] for x in os.listdir(metadatadir)]
    to_install = [x for x in to_install if x not in already_installed]
    if not to_install:
        print_normal("Nothing to install!")
    else:
        print_normal("Following packages will be installed:")
        list_packages_print(to_install)
        if not choice():
            if os.listdir(installdir):
                os.system("rm " + installdir + "*")
            abort()
        print_debug(end="")
        for package in to_install:
            print_debug("Installing " + str(package) + " ... ", end='', flush=True)
            install_package(package, package not in package_names)
            print_debug("DONE")
    if os.listdir(installdir):
        os.system("rm " + installdir + "*")
    print_normal("Installed " + str(len(to_install)) + " packages.")
