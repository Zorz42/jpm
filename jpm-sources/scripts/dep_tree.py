from json import load, decoder
from os import path
from wget import download
from httplib2 import Http

from globals import print_error, jpm_exit, installdir
from scripts.verify import verify_package_json
from subprocess import check_output


def quit_incomplete(package_name):
    print_error(f"Package {package_name} is incomplete or damaged and therefore cannot be downloaded!")
    jpm_exit(0)


def check_if_package_exists(package_name):
    resp = Http().request(f"https://jaclang.zorz.si/main-repository/{package_name}/Latest.json", 'HEAD')
    return int(resp[0]['status']) < 400


def build_dep_tree(package_name):
    if path.isfile(f"{installdir}{package_name}.json"):
        return
    if not check_if_package_exists(package_name):
        print_error(f"Package {package_name} does not exist.")
        jpm_exit(1)
    download(f"https://jaclang.zorz.si/main-repository/{package_name}/Latest.json",
             f"{installdir}{package_name}.json", bar=None)
    with open(installdir + package_name + ".json") as info_file:
        try:
            info = load(info_file)
        except decoder.JSONDecodeError:
            quit_incomplete(package_name)
        if not verify_package_json(info):
            quit_incomplete(package_name)

        if info["Version"] == "pre-release":
            print_error(f"Package {package_name} is not released yet!")
            jpm_exit(0)

        supported_version = [int(x) for x in info["Supported Version"].split(".")]

        current_jaclang_version = str(check_output(["jaclang", "--version"])).split(" ")[1][:-3]
        current_jaclang_version = [int(x) for x in current_jaclang_version.split(".")[:-1]]

        if current_jaclang_version[0] != supported_version[0] or current_jaclang_version[1] < supported_version[1]:
            print_error(f"Package {package_name} is not compatible with your current version of jaclang! "
                        f"(package supported version: {'.'.join([str(x) for x in supported_version])}, "
                        f"jaclang version: {str(check_output(['jaclang', '--version'])).split(' ')[1][:-3]})")
            jpm_exit(0)
    for dependency in info['Dependencies']:
        build_dep_tree(dependency)
