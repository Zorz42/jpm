from os import path, listdir, unlink
from json import load, dump, decoder
from wget import download
from subprocess import check_output
from shutil import rmtree
from requests import head, codes

from globals import choice, throwError, installdir, main_repository
from scripts.installPackage import installPackage
from scripts.listPackages import listInstalledPackages, printPackages
from scripts.verify import verifyPackageJson


def buildDepTree(package_name, dependency=False):
    if path.isfile(f"{installdir}{package_name}.json"):
        return True
    if head(f"{main_repository}{package_name}/Latest.json").status_code != codes.ok:
        throwError(f"Package {package_name} does not exist.")

    download(f"{main_repository}{package_name}/Latest.json",
             f"{installdir}{package_name}.json", bar=None)

    with open(f"{installdir}{package_name}.json", "r") as info_file:
        try:
            info = load(info_file)
        except decoder.JSONDecodeError:
            throwError(f"Package {package_name} is damaged and therefore cannot be downloaded!")

    if not verifyPackageJson(info, installed=False):
        throwError(f"Package {package_name} is incomplete and therefore cannot be downloaded!")

    supported_version = [int(x) for x in info["Supported Version"].split(".")]
    current_jaclang_version = str(check_output(["jaclang", "--version"])).split(" ")[1][:-3]
    current_jaclang_version = [int(x) for x in current_jaclang_version.split(".")[:-1]]

    if current_jaclang_version[0] != supported_version[0] or current_jaclang_version[1] < supported_version[1]:
        throwError(f"Package {package_name} is not compatible with your current version of jaclang!")

    for dependency in info["Dependencies"].copy():
        if buildDepTree(dependency, dependency=True):
            info["Dependencies"].remove(dependency)

    del info["Supported Version"]
    info["Type"] = "Dependency" if dependency else "Package"

    with open(f"{installdir}{package_name}.json", "w") as info_file:
        info_file.seek(0)
        dump(info, info_file, indent=4)
        info_file.write("\n")
        info_file.truncate()

    return False


def clearDirectory(dir_path):
    for filename in listdir(dir_path):
        file_path = path.join(dir_path, filename)
        if path.isfile(file_path) or path.islink(file_path):
            unlink(file_path)
        elif path.isdir(file_path):
            rmtree(file_path)


def install(package_names):
    clearDirectory(installdir)

    for package in package_names:
        if not path.isdir(f"{installdir}{package}"):
            buildDepTree(package)

    to_install = [".".join(x.split(".")[:-1]) for x in listdir(installdir)]
    already_installed = listInstalledPackages()[0]
    to_install = [x for x in to_install if x not in already_installed]

    if not to_install:
        print("Nothing to install!")
    else:
        print("Following packages will be installed:")
        printPackages(to_install)
        if choice():
            for package in to_install:
                installPackage(package)
    clearDirectory(installdir)
