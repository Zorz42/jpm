from json import load, decoder

from wget import download

from globals import print_error, jpm_exit, installdir
from scripts.verify import verify_package_json


def quit_incomplete(package_name):
    print_error(f"Package {package_name} is incomplete or damaged and therefore cannot be downloaded!")
    jpm_exit(0)


def build_dep_tree(package_name):
    download(f"https://jaclang.zorz.si/main-repository/{package_name}/Info.json",
             installdir + package_name + ".json", bar=None)
    with open(installdir + package_name + ".json") as info_file:
        try:
            metadata = load(info_file)
        except decoder.JSONDecodeError:
            quit_incomplete(package_name)
        if not verify_package_json(metadata, package_name):
            quit_incomplete(package_name)

        dependency_list = metadata['Dependencies']
    for dependency in dependency_list:
        build_dep_tree(dependency)
