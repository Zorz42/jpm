from os import path, listdir, mkdir, replace, popen, system
from json import decoder
from shutil import rmtree

from globals import choice, installdir, main_repository, libdir, jacdir, printWarning, makeCacheDir, printException
from listPackages import listInstalledPackages, printPackages
from verify import verifyPackageJson, packageExists
from util import writeInfo, loadInfo, extractTar, HTTPError, downloadFile


class DependencyError(Exception):
    pass


def buildDepTree(package_name: str, dependency=False):
    # check if file has already been processed (circular dependencies)
    if path.isfile(f"{installdir}{package_name}.json"):
        return

    # download info file
    try:
        downloadFile(f"{main_repository}{package_name}/Latest.json", f"{installdir}{package_name}.json")
    except HTTPError:
        raise DependencyError(f"Package '{package_name}' does not exist.")

    # load info file
    try:
        info = loadInfo(f"{installdir}{package_name}.json")
    except decoder.JSONDecodeError:
        raise DependencyError(f"Package '{package_name}' is damaged and therefore cannot be downloaded!")

    # verify info file
    if not verifyPackageJson(info, installed=False):
        raise DependencyError(f"Package '{package_name}' is incomplete and therefore cannot be downloaded!")

    # get current jaclang version and supported one
    supported_version = [int(x) for x in info["Supported Version"].split(".")]
    current_version = popen(f"{jacdir}Binaries/jaclang --version").read().split(" ")[1]
    current_version = [int(x) for x in current_version.split(".")[:-1]]

    # check if package supports current jaclang version
    if current_version[0] != supported_version[0] or current_version[1] < supported_version[1]:
        raise DependencyError(f"Package '{package_name}' is not compatible with your current version of jaclang!")

    del info["Supported Version"]
    info["Type"] = "Dependency" if dependency else "Package"

    for dependency_ in info["Dependencies"]:
        buildDepTree(dependency_, dependency=True)

    writeInfo(info, f"{installdir}{package_name}.json")


def installPackage(package_name: str):
    print(f"Installing {package_name}")

    info = loadInfo(f"{installdir}{package_name}.json")

    # download archive
    downloadFile(f"{main_repository}{package_name}/Versions/{info['Version']}.tar.gz", f"{libdir}{package_name}.tar.gz")

    # make directory for the package and extract it
    extractTar(f"{libdir}{package_name}.tar.gz", libdir + package_name, remove_tar=True)

    # replace optimized json file
    replace(f"{installdir}{package_name}.json", f"{libdir}{package_name}/Info.json")

    if not packageExists(package_name):
        printWarning(f"Package '{package_name}' does not seem to be valid.")

    # compile library
    system(f"{jacdir}Binaries/jacmake {libdir}{package_name}")
    rmtree(f"{libdir}{package_name}/Sources")


def install(package_names: set):
    makeCacheDir()
    if path.isdir(installdir):
        rmtree(installdir)
    mkdir(installdir)

    # build dependency tree for all packages
    try:
        for package in package_names:
            if not path.isdir(f"{installdir}{package}"):
                buildDepTree(package)
    except DependencyError as e:
        printException(e)

    # remove already installed packages from he to install list
    package_names = {x[:-5] for x in listdir(installdir) if x.endswith(".json")}
    already_installed = listInstalledPackages()[0]
    package_names = {x for x in package_names if x not in already_installed}

    if package_names:
        print("Following packages will be installed:")
        printPackages(package_names)
        if choice():
            for package in package_names:
                installPackage(package)
    else:
        print("Nothing to install!")
