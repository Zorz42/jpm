from json import load, decoder

from wget import download

from globals import print_error, jpm_exit, installdir
from scripts.verify import verify_package_json


def build_dep_tree(package_name):
    dependency_list = []
    download("https://jaclang.zorz.si/main-repository/metadatas/" + package_name + ".json",
             installdir + package_name + ".json", bar=None)
    with open(installdir + package_name + ".json") as metafile:
        try:
            metadata = load(metafile)
        except decoder.JSONDecodeError:
            print_error("Package " + package_name + " is not valid!")
            jpm_exit(0)
        if 'dependencies' in metadata.keys():
            dependency_list = metadata['dependencies']
        if not verify_package_json(metadata, package_name):
            print_error("Package " + package_name + " is not valid!")
            jpm_exit(0)
    for dependency in dependency_list:
        build_dep_tree(dependency)
