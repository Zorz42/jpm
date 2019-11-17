from globals import *
from scripts.install_bar import *
from scripts.dep_tree import *
from scripts.install_package import *
import httplib2

def check_if_package_exists(package_name):
    h = httplib2.Http()
    resp = h.request("https://jaclang.zorz.si/main-repository/" + package_name + "/metadata.json", 'HEAD')
    return int(resp[0]['status']) < 400

def install(package_names):
    print("Starting to install...")
    if(os.listdir(installdir) != []):
        os.system("rm " + installdir + "*")
    for package in package_names:
        if not check_if_package_exists(package):
            print("\x1b[0;31mPackage " + package + " does not exist.")
            exit(1)
        print("Building dependency tree for " + package)
        if not os.path.isfile(installdir + package + ".json"):
            build_dep_tree(package)
    to_install = [x.split('.')[0] for x in os.listdir(installdir)]
    already_installed = [x.split('.')[0] for x in os.listdir(metadatadir)]
    to_install = [x for x in to_install if x not in already_installed]
    if to_install == []:
        print("\x1b[0mNothing to install!")
    else:
        print("\x1b[0mFollowing packages will be installed:")
        list_packages_print(to_install)
        if not choice():
            print("\x1b[0;31mAborting")
            if os.listdir(installdir) != []:
                os.system("rm " + installdir + "*")
            exit(0)
        print("\x1b[1;30m", end='')
        for package in to_install:
            print("Installing " + package + " ... ", end='', flush=True)
            install_package(package, package not in package_names)
            print("DONE")
    if os.listdir(installdir) != []:
        os.system("rm " + installdir + "*")
    print("\x1b[0mInstalled " + str(len(to_install)) + " packages.")
