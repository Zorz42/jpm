from os import path, listdir, unlink
from json import load, decoder
from wget import download
from subprocess import check_output
from shutil import rmtree
from requests import head, codes

from globals import choice, throw_error, installdir, main_repository
from scripts.installPackage import install_package
from scripts.listPackages import list_installed_packages, print_packages
from scripts.verify import verify_package_json


def build_dep_tree(package_name):
    if path.isfile(f"{installdir}{package_name}.json"):
        return
    if head(f"{main_repository}{package_name}/Latest.json").status_code != codes.ok:
        throw_error(f"Package {package_name} does not exist.")

    download(f"{main_repository}{package_name}/Latest.json",
             f"{installdir}{package_name}.json", bar=None)

    with open(installdir + package_name + ".json") as info_file:
        try:
            info = load(info_file)
        except decoder.JSONDecodeError:
            throw_error(f"Package {package_name} is damaged and therefore cannot be downloaded!")

    if not verify_package_json(info, installed=False):
        throw_error(f"Package {package_name} is incomplete and therefore cannot be downloaded!")

    supported_version = [int(x) for x in info["Supported Version"].split(".")]
    current_jaclang_version = str(check_output(["jaclang", "--version"])).split(" ")[1][:-3]
    current_jaclang_version = [int(x) for x in current_jaclang_version.split(".")[:-1]]

    if current_jaclang_version[0] != supported_version[0] or current_jaclang_version[1] < supported_version[1]:
        throw_error(f"Package {package_name} is not compatible with your current version of jaclang!")

    for dependency in info['Dependencies']:
        build_dep_tree(dependency)


def clear_directory(dir_path):
    for filename in listdir(dir_path):
        file_path = path.join(dir_path, filename)
        if path.isfile(file_path) or path.islink(file_path):
            unlink(file_path)
        elif path.isdir(file_path):
            rmtree(file_path)


def install(package_names):
    clear_directory(installdir)

    for package in package_names:
        if not path.isdir(f"{installdir}{package}"):
            build_dep_tree(package)

    to_install = [".".join(x.split(".")[:-1]) for x in listdir(installdir)]
    already_installed = list_installed_packages()[0]
    to_install = [x for x in to_install if x not in already_installed]

    if not to_install:
        print("Nothing to install!")
    else:
        print("Following packages will be installed:")
        print_packages(to_install)
        if choice():
            for package in to_install:
                install_package(package, package not in package_names)
    clear_directory(installdir)
