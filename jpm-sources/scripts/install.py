from os import path, listdir, unlink, remove, mkdir, replace, popen
from json import load, dump, decoder
from shutil import rmtree
from tarfile import open as tar_open

from globals import choice, throwError, installdir, main_repository, libdir, removeFileIfExists, downloadFile, urlExists
from scripts.listPackages import listInstalledPackages, printPackages
from scripts.verify import verifyPackageJson, packageExists


def buildDepTree(package_name: str, dependency=False):
    # check if file has already been processed (circular dependencies)
    if path.isfile(f"{installdir}{package_name}.json"):
        return True

    # check if package exists
    if not urlExists(f"{main_repository}{package_name}/Latest.json"):
        throwError(f"Package {package_name} does not exist.")

    # download info file
    downloadFile(f"{main_repository}{package_name}/Latest.json", f"{installdir}{package_name}.json")

    # decode info file
    with open(f"{installdir}{package_name}.json") as info_file:
        try:
            info = load(info_file)
        except decoder.JSONDecodeError:
            throwError(f"Package {package_name} is damaged and therefore cannot be downloaded!")

    # verify info file
    if not verifyPackageJson(info, installed=False):
        throwError(f"Package {package_name} is incomplete and therefore cannot be downloaded!")

    # get current jaclang version and supported one
    supported_version = [int(x) for x in info["Supported Version"].split(".")]
    current_jaclang_version = popen("jaclang --version").read().split(" ")[1]
    current_jaclang_version = [int(x) for x in current_jaclang_version.split(".")[:-1]]

    # check if package supports current jaclang version
    if current_jaclang_version[0] != supported_version[0] or current_jaclang_version[1] < supported_version[1]:
        throwError(f"Package {package_name} is not compatible with your current version of jaclang!")

    # remove unnecessary dependencies to save characters in info file
    for dependency in info["Dependencies"].copy():
        if buildDepTree(dependency, dependency=True):
            info["Dependencies"].remove(dependency)

    # delete some unnecessary info in info file
    del info["Supported Version"]
    info["Type"] = "Dependency" if dependency else "Package"

    with open(f"{installdir}{package_name}.json", "w") as info_file:
        info_file.seek(0)
        dump(info, info_file, indent=4)
        info_file.write("\n")
        info_file.truncate()

    return False


def installPackage(package_name: str):
    print(f"Installing {package_name}")
    # load info file
    with open(f"{installdir}{package_name}.json") as info_file:
        info = load(info_file)

    # first remove file to be downloaded if it would be there for some reason
    removeFileIfExists(f"{libdir}{package_name}.tar.gz")

    # download archive
    downloadFile(f"{main_repository}{package_name}/Versions/{info['Version']}.tar.gz", f"{libdir}{package_name}.tar.gz")

    # make directory for the package and extract it
    mkdir(f"{libdir}{package_name}")
    with tar_open(f"{libdir}{package_name}.tar.gz", "r:gz") as tar_file:
        tar_file.extractall(path=libdir + package_name)

    # remove archive and replace optimized json file
    remove(f"{libdir}{package_name}.tar.gz")
    replace(f"{installdir}{package_name}.json", f"{libdir}{package_name}/Info.json")

    if not packageExists(package_name):
        throwError(f"Package {package_name} is not valid and cannot be installed.")
        rmtree(libdir + package_name)


def clearDirectory(dir_path: str):
    # clear contents of a directory
    for filename in listdir(dir_path):
        file_path = path.join(dir_path, filename)
        if path.isdir(file_path):
            rmtree(file_path)
        if path.isfile(file_path) or path.islink(file_path):
            unlink(file_path)


def install(package_names: set):
    # first clear install directory
    clearDirectory(installdir)

    # build dependency tree for all packages
    for package in package_names:
        if not path.isdir(f"{installdir}{package}"):
            buildDepTree(package)

    # remove already installed packages from he to install list
    package_names = {x[:-5] for x in listdir(installdir) if x.endswith(".json")}
    already_installed = listInstalledPackages()[0]
    package_names = {x for x in package_names if x not in already_installed}

    if not package_names:
        print("Nothing to install!")
    else:
        print("Following packages will be installed:")
        printPackages(package_names)
        if choice():
            for package in package_names:
                installPackage(package)
    clearDirectory(installdir)
