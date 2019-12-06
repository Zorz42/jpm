import json
import wget

from globals import *
from scripts.verify import *


def build_dep_tree(package_name):
    dependency_list = []
    wget.download("https://jaclang.zorz.si/main-repository/" + package_name + "/metadata.json",
                  installdir + package_name + ".json", bar=None)
    with open(installdir + package_name + ".json") as metafile:
        try:
            metadata = json.load(metafile)
        except:
            print("\x1b[0;31mPackage " + package_name + " is not valid!")
            exit(0)
        if 'dependencies' in metadata.keys():
            dependency_list = metadata['dependencies']
        if not verify_package_json(metadata, package_name):
            print("\x1b[0;31mPackage " + package_name + " is not valid!")
            exit(0)
    for dependency in dependency_list:
        build_dep_tree(dependency)
